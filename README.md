LangGraph RAG Technical Documentation Assistant

A Retrieval-Augmented Generation (RAG) based technical documentation assistant built using LangGraph, FastAPI, and ChromaDB.

This project was developed as part of the AI/ML Engineer Intern Take-Home Assignment.

Project Overview

This application allows users to ask questions related to technical documentation such as:

LangGraph
FastAPI
ChromaDB

The system retrieves relevant document chunks from a vector database and generates answers based on the retrieved content.

The project uses a graph-based workflow built using LangGraph StateGraph.

Features
Query processing workflow using LangGraph
Document retrieval using ChromaDB
Document relevance filtering
Conditional routing and retry logic
FastAPI REST API
Technical document ingestion pipeline
Source references in responses
Technologies Used
Component	Technology
Backend API	FastAPI
Workflow Engine	LangGraph
Vector Database	ChromaDB
Embeddings	HuggingFace Sentence Transformers
LLM Provider	Groq
Language	Python 3.11
Why These Technologies Were Chosen
LangGraph

LangGraph was chosen because the assignment required a graph-based workflow with conditional routing and retry handling.

It helps in building:

multi-step workflows
retry mechanisms
state management
conditional execution flows
ChromaDB

ChromaDB was used because it is:

lightweight
easy to run locally
suitable for RAG applications
beginner friendly

It stores embeddings and performs semantic similarity search.

FastAPI

FastAPI was used to build REST APIs because:

it is fast
simple to use
provides automatic Swagger documentation
supports request validation using Pydantic
Groq

Groq was used because it provides:

fast inference
free API access
easy integration with LangChain
Workflow Architecture

The application follows this workflow:

User Question
      ↓
Query Analysis
      ↓
Document Retrieval
      ↓
Document Grading
      ↓
Conditional Routing
      ↓
Answer Generation
LangGraph Workflow Nodes
1. Query Analysis Node

This node prepares the user query before retrieval.

In the current implementation, the original question is passed directly into retrieval while maintaining a modular structure for future query rewriting improvements.

2. Retrieval Node

This node retrieves the most relevant document chunks from ChromaDB using vector similarity search.

The top relevant chunks are returned along with metadata.

3. Document Grading Node

This node checks whether the retrieved documents are relevant to the user's question.

The current implementation uses simple keyword relevance matching to filter unrelated documents.

If no relevant documents are found, the workflow retries retrieval using conditional routing.

4. Generation Node

The final answer is generated using the retrieved document chunks and returned along with source references.

Conditional Routing Logic

The workflow uses conditional edges in LangGraph.

If relevant documents are found:

→ Proceed to answer generation

If no relevant documents are found:

→ Retry retrieval

A retry count is maintained in the graph state.

State Management

The graph state stores:

user question
rewritten question
retrieved documents
filtered documents
generated answer
retry count

This allows information to flow between nodes.

Document Ingestion Pipeline

The ingestion pipeline performs the following steps:

Loads documents from the docs/ folder
Splits documents into chunks
Generates embeddings
Stores embeddings inside ChromaDB
Chunking Strategy

The project uses:

RecursiveCharacterTextSplitter

Configuration used:

chunk_size = 500
chunk_overlap = 100
Reason for this strategy

Technical documentation often contains connected explanations and API references.

Chunk overlap helps preserve context between chunks while retrieval.

Embedding Model

The following embedding model was used:

sentence-transformers/all-MiniLM-L6-v2
Reason

This model is:

lightweight
fast
suitable for small RAG systems
free to use
API Endpoints
POST /query

Accepts a user question and returns an answer with sources.

Example:

{
  "question": "What is LangGraph?"
}
POST /ingest

Used for document ingestion.

GET /documents

Returns the list of indexed documents.

POST /feedback

Accepts user feedback.

Example:

{
  "feedback": "good",
  "comment": "Helpful answer"
}
Project Structure
rag-assistant/
│
├── app/
│   ├── main.py
│   ├── graph.py
│   ├── state.py
│   ├── retriever.py
│   ├── ingest.py
│   ├── prompts.py
│   └── utils.py
│
├── docs/
├── chroma_db/
├── requirements.txt
├── README.md
├── .env.example
└── .gitignore
Setup Instructions
1. Clone Repository
git clone <repository_url>
cd rag-assistant
2. Create Virtual Environment
Windows
python -m venv venv
venv\Scripts\activate
Mac/Linux
python3 -m venv venv
source venv/bin/activate
3. Install Dependencies
pip install -r requirements.txt
4. Add API Key

Create .env file:

GROQ_API_KEY=your_api_key_here
5. Ingest Documents
python app/ingest.py
6. Run FastAPI Server
uvicorn app.main:app --reload
7. Open Swagger UI
http://127.0.0.1:8000/docs
Example Questions
What is LangGraph?
How does FastAPI request validation work?
What is ChromaDB used for?
What are conditional edges in LangGraph?
Challenges Faced

Some challenges faced during development:

retrieving relevant document chunks
filtering unrelated chunks
handling retry logic
structuring the LangGraph workflow
Assumptions Made
The project focuses on mandatory assignment requirements
The document corpus is small
ChromaDB running locally is sufficient for this assignment
What I Would Improve With More Time

If given more time, I would improve:

advanced query rewriting
better document grading
hallucination detection
conversation memory
frontend UI
web search fallback
References
Official LangGraph Resources
LangGraph Agentic RAG Tutorial
Adaptive RAG Tutorial
LangGraph CRAG Notebook
Other References
FastAPI Documentation
Chroma Documentation
Sentence Transformers
Conclusion

This project demonstrates a RAG-based technical documentation assistant using LangGraph and FastAPI.

The implementation focuses on:

graph-based workflows
retrieval pipelines
conditional routing
document grading
simple and maintainable architecture

The project successfully satisfies the mandatory requirements of the assignment.