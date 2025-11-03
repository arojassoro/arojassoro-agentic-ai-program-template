"""
main.py

FastAPI interface for the Docs-to-Answers RAG Assistant.

Endpoints:
- GET /ask?query=your-question
- POST /ask with JSON body: { "query": "your-question" }

Usage:
    uvicorn app.main:app --reload
"""

from fastapi import FastAPI, Request, Query
from fastapi.responses import JSONResponse
from app.rag_agent import ask

app = FastAPI(title="Hardware Store RAG Assistant")

@app.get("/ask")
async def ask_get(query: str = Query(..., description="Your question or budget request")):
    response = ask(query)
    return JSONResponse(content={"query": query, "response": response})

@app.post("/ask")
async def ask_post(request: Request):
    data = await request.json()
    query = data.get("query", "")
    response = ask(query)
    return JSONResponse(content={"query": query, "response": response})