from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Request Model
class QueryRequest(BaseModel):
    question: str

# Feedback Model
class FeedbackRequest(BaseModel):
    feedback: str
    comment: str = ""

# Root Endpoint
@app.get("/")
def root():

    return {
        "message": "RAG assistant API is running",
        "endpoints": ["/query", "/documents", "/feedback", "/ingest"]
    }

# Query Endpoint
@app.post("/query")
def query_rag(request: QueryRequest):

    from app.graph import graph

    response = graph.invoke({
        "question": request.question,
        "retries": 0
    })

    return {
        "answer": response["generation"]
    }

# Documents Endpoint
@app.get("/documents")
def get_documents():

    return {
        "documents": [
            "fastapi_docs.md",
            "langgraph_docs.md",
            "chromadb_docs.md"
        ]
    }

# Feedback Endpoint
@app.post("/feedback")
def feedback(data: FeedbackRequest):

    return {
        "message": "Feedback received successfully"
    }

# Ingest Endpoint
@app.post("/ingest")
def ingest_documents():

    return {
        "message": "Documents ingestion endpoint"
    }
