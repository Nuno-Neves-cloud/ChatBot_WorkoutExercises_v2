# RAG - v5 Build

**All features from v4 Build:**
- Refactored code structure
- Conversation Memory
- Parent Document Retriever

**NEW IN v5 Build:**
- **Multi-Query Retrieval**: Generate query variations for better coverage
- **FlashRank Reranking**: Cross-encoder reranking for better relevance

## Install Dependencies
%pip install "langchain==0.3.27" -qqq
%pip install "langchain-community==0.3.31" -qqq
%pip install "langchain-openai==0.3.35" -qqq
%pip install "langchain-chroma==0.2.6" -qqq
%pip install pypdf -qqq
%pip install gradio -qqq
#--------------------------------------------------------------------------------
# NEW IN v5 Build: Install FlashRank for reranking
#--------------------------------------------------------------------------------
%pip install flashrank -qqq

# RAG - v5 Build

**All features from v4 Build:**
- Refactored code structure
- Conversation Memory
- Parent Document Retriever

**NEW IN v5 Build:**
- **Multi-Query Retrieval**: Generate query variations for better coverage
- **FlashRank Reranking**: Cross-encoder reranking for better relevance

## Install Dependencies
%pip install "langchain==0.3.27" -qqq
%pip install "langchain-community==0.3.31" -qqq
%pip install "langchain-openai==0.3.35" -qqq
%pip install "langchain-chroma==0.2.6" -qqq
%pip install pypdf -qqq
%pip install gradio -qqq
#--------------------------------------------------------------------------------
# NEW IN v5 Build: Install FlashRank for reranking
#--------------------------------------------------------------------------------
%pip install flashrank -qqq

## Configuration

The project uses a `load_secrets` function to securely load API keys and configuration values. It first attempts to load from Google Colab's secret storage, and falls back to loading from a local `.env` file for development. Required secrets include Chroma database credentials and OpenAI API key.

## Global Variables

The system initializes several key components:
- **Version Management**: Tracks the current build version (v5)
- **Embeddings Model**: Uses OpenAI's text-embedding-3-small for document vectorization
- **LLM**: Employs GPT-4o-mini for main inference and GPT-3.5-turbo for classification tasks
- **Vector Database**: Connects to Chroma Cloud with the specified collection for document storage
- **Base Retriever**: Configured to retrieve top 5 similar documents by default

## Ingestion Pipeline

The ingestion process handles PDF document processing with the following steps:

1. **Document Loading**: Loads PDF files from URLs or local paths using PyPDFLoader
2. **Topic Detection**: Automatically identifies the document's primary topic (e.g., 'bitcoin', 'ethereum') using LLM analysis
3. **Text Preprocessing**: Cleans raw PDF text by removing extra whitespace, standalone page numbers, and formatting artifacts
4. **Document Chunking**: Splits documents into manageable chunks (1000 characters with 200 character overlap) for better retrieval
5. **Metadata Enrichment**: Adds topic information and other metadata to each document chunk
6. **Vector Storage**: Stores processed chunks in the Chroma vector database for later retrieval

The system can ingest multiple documents, such as the Bitcoin whitepaper and Ethereum documentation.

## Inference Process

The inference pipeline implements advanced retrieval-augmented generation with conversation memory:

### RAG Chain
Creates a conversational AI assistant specialized in cryptocurrency whitepapers. The chain:
- Maintains conversation context across turns
- Provides clear, concise answers (2-3 paragraphs max)
- Uses only provided document context
- Handles follow-up questions by referencing previous context

### Chat History Formatting
Processes conversation history to maintain context while managing token limits:
- Limits to recent 5 conversation turns
- Formats messages for LLM consumption
- Balances relevance with cost/performance constraints

### Multi-Query Retrieval + Reranking (NEW IN v5)
Implements state-of-the-art retrieval techniques:

**Multi-Query Approach:**
- Generates multiple query variations using LLM
- Searches vector database with each variation
- Combines and deduplicates results for broader coverage

**FlashRank Reranking:**
- Uses cross-encoder model to score document relevance
- Reranks retrieved documents by semantic similarity to original query
- Returns top 4 most relevant documents

**Trade-offs:** Higher quality for complex queries but increased latency and cost due to additional LLM calls.

## Gradio Demo

Provides a web-based chat interface for interacting with the RAG system:
- **Title**: "Crypto RAG Assistant (v5)"
- **Features**: Conversation memory, multi-query retrieval, and FlashRank reranking
- **Example Questions**: Includes sample queries about Bitcoin, blockchain technology, and cryptocurrency concepts
- **Deployment**: Launches with public sharing enabled for easy access
