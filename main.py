"""
A simple RAG application for answering questions about home workouts using LangChain, Chroma, and OpenAI.
Run with: python main.py --serve

"""
from typing import Dict, List
import os
import argparse

def load_secrets(keys: List[str]) -> Dict[str, str]:
    """Load secret values quickly with minimal imports."""
    # Local imports to keep startup lightweight
    env_values: Dict[str, str] = {k: os.getenv(k) for k in keys}
    # Fast-path: if all keys already in environment, return immediately
    if all(env_values.get(k) for k in keys):
        return env_values

    env_path = os.path.join(os.getcwd(), ".env")
    values = env_values.copy()

    # Only attempt to load .env if a .env file exists and some keys are missing
    if any(not v for v in values.values()) and os.path.exists(env_path):
        try:
            from dotenv import load_dotenv

            load_dotenv(env_path)
        except Exception as e:
            raise ImportError(
                "python-dotenv is required for local development. Install it with: pip install python-dotenv"
            ) from e
        # Re-read environment after loading .env
        values = {k: os.getenv(k) for k in keys}

    # Check for missing keys and provide helpful error for local development
    missing = [k for k, v in values.items() if not v]
    if missing:
        env_file_help = (
            f"Missing keys: {', '.join(missing)}.\n\n"
            "Create a .env file in the project root with:\n"
            + "\n".join([f"{key}=YOUR_VALUE_HERE" for key in missing])
        )
        raise ValueError(env_file_help)

    # Only set variables that are not already present to avoid overwriting runtime config
    for key, value in values.items():
        if value and os.getenv(key) is None:
            os.environ[key] = value

    return values


def build_app(serve: bool = True):
    """Builds application objects and optionally launches the Gradio demo."""
    # Import heavy libraries only when needed
    from langchain_openai import ChatOpenAI, OpenAIEmbeddings
    from langchain_chroma import Chroma
    from langchain.retrievers import ParentDocumentRetriever
    from langchain.storage import InMemoryStore
    from langchain.text_splitter import RecursiveCharacterTextSplitter

    # Load secrets
    secrets = load_secrets(["CHROMA_API_KEY", "CHROMA_TENANT", "CHROMA_DATABASE", "OPENAI_API_KEY"])  # may raise

    # Vector DB collection name
    COLLECTION_NAME = f"home_workout_database"

    # Embeddings Model
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    # LLM
    llm = ChatOpenAI(model="gpt-4o-mini")

    # Classification LLM
    classification_llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    # Vector Database
    vectorstore = Chroma(
        embedding_function=embeddings,
        collection_name=COLLECTION_NAME,
        chroma_cloud_api_key=secrets["CHROMA_API_KEY"],
        tenant=secrets["CHROMA_TENANT"],
        database=secrets["CHROMA_DATABASE"],
    )

    # Base retriever from vectorstore
    base_retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

    # Utility functions from notebook converted below
    import re

    def clean_text(text: str) -> str:
        text = re.sub(r"\s+", " ", text)
        text = re.sub(r"(?<=\.)\s*\d+\s*$", "", text)
        return text.strip()

    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser

    def detect_document_topic(documents: list) -> str:
        topic_detection_template = ChatPromptTemplate.from_template(
            """
            Analyze the following document content and determine its primary topic.

            Document content:
            {content}

            Based on this content, what is the primary topic? Answer with a single word or short phrase (e.g., 'home exercises', 'workout').

            Primary topic:
            """
        )

        topic_detection_chain = topic_detection_template | classification_llm | StrOutputParser()

        sample_content = ""
        for doc in documents[:3]:
            sample_content += doc.page_content + "\n\n"

        sample_content = sample_content[:4000]

        detected_topic = topic_detection_chain.invoke({"content": sample_content}).strip().lower()

        return detected_topic

    from langchain.document_loaders import PyPDFLoader

    def ingest_documents(document_path: str):
        print("-" * 80)
        print("STARTING INGESTION PIPELINE")
        print("-" * 80)

        print("\n[1/6] Loading file...")
        loader = PyPDFLoader(document_path)
        documents = loader.load()
        print(f"✓ Loaded {len(documents)} pages from file")

        print(f"\n[2/6] Auto-detecting document topic...")
        detected_topic = detect_document_topic(documents)
        print(f"✓ Topic auto-detected: '{detected_topic}'")

        print(f"\n[3/6] Applying text preprocessing...")
        for doc in documents:
            doc.page_content = clean_text(doc.page_content)
        print(f"✓ Cleaned {len(documents)} pages")

        print(f"\n[4/6] Splitting documents into chunks...")
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
        chunks = text_splitter.split_documents(documents)
        print(f"✓ Split {len(chunks)} chunks")

        print(f"\n[5/6] Enriching documents with metadata...")
        for chunk in chunks:
            chunk.metadata.update({"topic": detected_topic})
        print(f"✓ Metadata enriched for all documents")

        print(f"\n[6/6] ParentDocumentRetriever processing...")
        base_retriever.add_documents(chunks)
        print(f"✓ Stored")

        return len(chunks), detected_topic

    from langchain_core.prompts import ChatPromptTemplate as _ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser as _StrOutputParser

    def create_rag_chain():
        rag_template = _ChatPromptTemplate.from_template(
            """
            You are a personal trainer answering questions about home workout exercises.

            Use the conversation history and provided documents to answer the current question.

            Conversation History:
            {history}

            Documents:
            {context}

            Current Question: {query}

            Answer:
            """
        )

        rag_chain = rag_template | llm | _StrOutputParser()
        return rag_chain

    def format_chat_history(history: list, max_turns: int = 5) -> str:
        if not history:
            return "No previous conversation."
        recent_history = history[-(max_turns * 2):]
        formatted = []
        for message in recent_history:
            role = message["role"].capitalize()
            content = message["content"]
            formatted.append(f"{role}: {content}")
        return "\n".join(formatted)

    # Multi-query inference function
    from langchain.retrievers.multi_query import MultiQueryRetriever
    from langchain.retrievers import ContextualCompressionRetriever
    from langchain_community.document_compressors import FlashrankRerank

    def inference(query: str, chat_history: list = None) -> str:
        print("=" * 80)
        print("RUNNING MULTI-QUERY INFERENCE")
        print("=" * 80)

        formatted_history = format_chat_history(chat_history, max_turns=5)

        multiquery_retriever = MultiQueryRetriever.from_llm(retriever=base_retriever, llm=llm)
        compressor = FlashrankRerank(top_n=4)
        compression_retriever = ContextualCompressionRetriever(base_compressor=compressor, base_retriever=multiquery_retriever)

        results = compression_retriever.invoke(query)

        context = "\n\n".join([doc.page_content for doc in results])

        response = create_rag_chain().invoke({"context": context, "query": query, "history": formatted_history})
        print("\n" + "=" * 80)
        print("INFERENCE COMPLETE")
        print("=" * 80)
        return response

    # Gradio interface
    def chat_inference(message, history):
        return inference(query=message, chat_history=history)

    # Only import Gradio when serving
    if serve:
        import gradio as gr

        demo = gr.ChatInterface(
            fn=chat_inference,
            title="ChatBot for Home Workouts",
            description="Ask questions about home workout exercises.",
            examples=[
                "What exercises can I do at home?",
                "How often should I workout?",
                "What are some good cardio exercises?",
                "How do I build muscle at home?",
            ],
        )

        demo.launch(share=False, debug=False)

    # Expose objects for external import/testing
    return {
        "ingest_documents": ingest_documents,
        "inference": inference,
        "clean_text": clean_text,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--serve", action="store_true", help="Launch Gradio demo")
    parser.add_argument("--ingest", action="store_true", help="Run ingestion on bundled files")
    args = parser.parse_args()

    app = build_app(serve=args.serve)

    if args.ingest:
        # Default ingest files in ./files if present
        bundle = [
            os.path.join("files", f) for f in os.listdir("files") if f.lower().endswith(".pdf")
        ] if os.path.isdir("files") else []
        if not bundle:
            print("No PDF files found in ./files to ingest.")
        for p in bundle:
            print(f"Ingesting {p}...")
            app["ingest_documents"](p)


if __name__ == "__main__":
    main()
