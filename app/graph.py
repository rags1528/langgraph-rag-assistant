from langgraph.graph import StateGraph, END
from app.state import GraphState
from app.retriever import retriever

# Query Rewrite Node
def rewrite_query(state):

    question = state["question"]

    print("\n--- QUERY REWRITE NODE ---")
    print("Question:", question)

    rewritten_question = question

    return {
        "rewritten_question": rewritten_question,
        "retries": state.get("retries", 0) + 1
    }

# Retrieval Node
def retrieve(state):

    question = state["rewritten_question"]

    print("\n--- RETRIEVAL NODE ---")
    print("Retrieving documents...")

    docs = retriever.invoke(question)

    print("Retrieved Docs:", len(docs))

    return {
        "documents": docs
    }

# Document Grading Node
def grade_documents(state):

    question = state["question"]

    docs = state["documents"]

    filtered_docs = []

    print("\n--- DOCUMENT GRADING NODE ---")

    for doc in docs:

        print("Checking document relevance...")

        content = doc.page_content.lower()

        if any(word in content for word in question.lower().split()):
            filtered_docs.append(doc)

    print("Relevant Docs:", len(filtered_docs))

    return {
        "filtered_docs": filtered_docs
    }

# Routing Logic
def decide_to_generate(state):

    filtered_docs = state["filtered_docs"]

    retries = state["retries"]

    if len(filtered_docs) > 0:
        return "generate"

    if retries >= 2:
        return "generate"

    return "rewrite"

# Generation Node
def generate(state):

    question = state["question"]

    docs = state["filtered_docs"]

    print("\n--- GENERATION NODE ---")
    print("Generating final answer...")

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    sources = []

    for doc in docs:
        source = doc.metadata.get("source", "Unknown")
        sources.append(source)

    answer = f"""
Question:
{question}

Answer:
Based on the retrieved documents:

{context}

Sources:
{list(set(sources))}
"""

    return {
        "generation": answer
    }

# Build Graph
workflow = StateGraph(GraphState)

workflow.add_node("rewrite", rewrite_query)
workflow.add_node("retrieve", retrieve)
workflow.add_node("grade", grade_documents)
workflow.add_node("generate", generate)

workflow.set_entry_point("rewrite")

workflow.add_edge("rewrite", "retrieve")
workflow.add_edge("retrieve", "grade")

workflow.add_conditional_edges(
    "grade",
    decide_to_generate,
    {
        "rewrite": "rewrite",
        "generate": "generate"
    }
)

workflow.add_edge("generate", END)

graph = workflow.compile()
