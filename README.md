# Home Workouts Chatbot

Home Workouts Chatbot is a retrieval-augmented generation (RAG) project that builds a personal fitness assistant from workout documents. It ingests PDF workout guides, stores them in a vector database, and serves a conversational chatbot that answers home exercise questions with context from the ingested materials.

## What this project does

- Loads and preprocesses workout PDFs from the `files/` folder.
- Detects the topic of each document to enrich metadata.
- Splits text into retrievable chunks and stores them in Chroma.
- Uses OpenAI embeddings and chat models to build a RAG-based workout assistant.
- Supports follow-up questions and conversational context.
- Includes a Gradio demo for an interactive trainer-style chat interface.

## Key features

- **Home workout focus**: Built around exercise guides and training manuals.
- **Document ingestion pipeline**: Cleans, chunks, and indexes PDF content.
- **Retrieval-enhanced answers**: Uses relevant text passages to answer questions accurately.
- **Conversation memory**: Keeps recent chat history to handle follow-up queries.
- **Trainer demo**: Provides a user interface for asking workout questions interactively.

## Setup

Install the required Python packages before running the notebook:

```bash
pip install "langchain==0.3.27"
pip install "langchain-community==0.3.31"
pip install "langchain-openai==0.3.35"
pip install "langchain-chroma==0.2.6"
pip install pypdf
pip install gradio
pip install flashrank
```

## Configuration

The notebook loads secrets using a helper function that reads environment variables or a `.env` file. Required secrets:

- `CHROMA_API_KEY`
- `CHROMA_TENANT`
- `CHROMA_DATABASE`
- `OPENAI_API_KEY`

## How to use

1. Open `HomeWorkoutsChatbot.ipynb`.
2. Run the dependency installation and configuration cells.
3. Ingest the workout PDF files from `files/`.
4. Create the RAG chain and launch the Gradio demo.
5. Ask workout-related questions like:
   - "How do I perform a goblet squat at home?"
   - "What are the best stretching exercises after a leg workout?"
   - "Give me a home-friendly upper body routine."

## Files

- `HomeWorkoutsChatbot.ipynb`: Main notebook containing the ingestion, retrieval, and Gradio demo flow.
- `files/100-workouts-vol1.pdf`, `files/100-workouts-vol2.pdf`, `files/100-workouts-vol3.pdf`, `files/100-workouts-vol4.pdf`: Example workout documents used for ingestion.

## Notes

- The assistant is designed to answer questions using only the ingested workout documents.
- If a question cannot be answered from the available content, it should indicate that the information is not available.
- The project is ideal for prototyping a fitness-focused chatbot using RAG techniques.
