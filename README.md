# Code For All\_ | AI for Programmers (Python)

## Course Overview

- Five-weeks course.
- Each week is thought for three 2-hour sessions, leaving a flexible hour on the last session of each week.

## Course Structure

### Week 1: AI Fundamentals & Large Language Models

AI history, machine learning paradigms, neural networks, transformer architecture, LLM internals (tokenization, embeddings, generation), OpenAI API.

### Week 2: Prompt Engineering, LangChain & Vector Databases

Prompt anatomy and techniques, LangChain framework (chains, components), vector databases, embeddings, similarity search, complete RAG implementation.

### Week 3: RAG - Iterative Build

Build complete RAG system across three iterations: v1 (foundation, ingestion, retrieval), v2 (LLM integration, UI), v3 (multi-document, preprocessing, metadata filtering). Each day builds on previous day's solution.

### Week 4: Advanced RAG Strategies & Evaluation

Code refactoring, conversation memory, parent-child retrieval, multi-query expansion, cross-encoder reranking, RAGAS evaluation framework (Faithfulness, Answer Relevancy, Context Precision, Context Recall).

### Week 5: AI Agents & Fine-tuning

AI agent fundamentals, LangChain tools and ReAct pattern, building custom agents, OpenAI fine-tuning API, preparing training data, when to use fine-tuning vs RAG vs prompt engineering.

## Week-Specific Guides

- [Week 1 Guide](week_1/README.md) - Sessions, notebooks, objectives
- [Week 2 Guide](week_2/README.md) - Sessions, notebooks, objectives
- [Week 3 Guide](week_3/README.md) - Sessions, notebooks, objectives, development flow
- [Week 4 Guide](week_4/README.md) - Sessions, notebooks, objectives, version progression
- [Week 5 Guide](week_5/README.md) - Sessions, notebooks, objectives, agents and fine-tuning

## Using These Notebooks

**Private Repository**: Direct "Open in Colab" links won't work.

**Process**:

1. Download `.ipynb` file from GitHub (click file → Raw → Save as)
2. Upload to [Google Colab](https://colab.research.google.com/) (File → Upload notebook)

## Local Development Setup

To run notebooks locally on your machine (instead of Colab), follow these steps:

### 1. Create Virtual Environment

```bash
python3 -m venv .venv
```

### 2. Activate Virtual Environment

**On macOS/Linux:**

```bash
source .venv/bin/activate
```

**On Windows:**

```bash
.venv\Scripts\activate
```

### 3. Upgrade pip

```bash
python -m pip install -U pip
```

### 4. Install Jupyter Kernel Support

```bash
pip install ipykernel jupyter
```

### 5. Register Kernel with Jupyter (Optional but Recommended)

Register your virtual environment as a named Jupyter kernel:

```bash
python -m ipykernel install --user --name=ai-programmers-python --display-name "Python (ai-programmers-python)"
```

This makes it easier to select the correct kernel in VS Code or Jupyter Notebook/Lab.

### 6. Install Environment Variable Support (for .env files)

```bash
pip install python-dotenv
```

### 7. Create .env File

Create a `.env` file in the project root with your API keys:

```env
# Required for all weeks
OPENAI_API_KEY=your_openai_key_here

# Week 2 - LangChain observability (optional)
LANGCHAIN_API_KEY=your_langchain_key_here
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com (if this url doesn't work check your organization url)
LANGCHAIN_PROJECT=your_project_name

# Week 2 - Vector database (Day 3 exercise)
PINECONE_API_KEY=your_pinecone_key_here

# Weeks 3-4 - Chroma vector database
CHROMA_API_KEY=your_chroma_key_here
CHROMA_TENANT=your_chroma_tenant_here
CHROMA_DATABASE=your_chroma_database_here
```

### 8. Using the Environment

- **In VS Code**:
  - Open a notebook file
  - Click the kernel selector in the top-right (or use Command Palette: "Select Kernel")
  - Choose the Python interpreter from `.venv/bin/python` (VS Code auto-detects it)
  - Or select "Python (ai-programmers-python)" if you completed step 5
- **In Standalone Jupyter Notebook/Lab**:
  - If you completed step 5: Select "Python (ai-programmers-python)" from the kernel dropdown
  - If you skipped step 5: Activate the venv, then run `jupyter notebook` from within the activated environment
- **Installing packages**: Each notebook installs its required packages via `%pip install` commands. You can also install them manually in the activated environment.

## Setup Instructions

### Required API Keys (Colab Secrets)

Students must add these in Colab (key icon in left sidebar → Add new secret):

**Required for all weeks:**

- `OPENAI_API_KEY` - All weeks
  - **Note**: Week 5 Day 1 (fine-tuning) requires billing-enabled account with fine-tuning access

**Week 2:**

- `LANGCHAIN_API_KEY` - Day 2 (for LangSmith observability, optional)
- `LANGCHAIN_TRACING_V2` - Day 2 (set to "true" for LangSmith tracing, optional)
- `LANGCHAIN_ENDPOINT` - Day 2 (LangSmith endpoint, optional)
- `LANGCHAIN_PROJECT` - Day 2 (LangSmith project name, optional)
- `PINECONE_API_KEY` - Day 3 (exercise notebook)

**Weeks 3-4:**

- `CHROMA_API_KEY` - All RAG notebooks
- `CHROMA_TENANT` - All RAG notebooks
- `CHROMA_DATABASE` - All RAG notebooks

### Uploading Files to Colab

If notebooks require additional files:

1. Download from `assets/` folder (if present)
2. In Colab: folder icon in left sidebar → Upload to session storage
3. Note: Files are temporary (deleted when session ends)

## Notebook Pattern

Most days include:

- Main notebook (concept instruction)
- CFU notebook (check for understanding exercises)
- Solution notebook (reference)
