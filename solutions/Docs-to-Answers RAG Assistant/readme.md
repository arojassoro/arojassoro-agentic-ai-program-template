# Docs-to-Answers RAG Assistant for Hardware Store

A mini Retrieval-Augmented Generation (RAG) assistant designed for a hardware. It answers frequently asked questions from markdown documents and generates budgets based on a CSV file of products and prices.

## Project Overview
This assistant uses local LLMs and embeddings to:
- Ingest and index markdown documents (FAQs)
- Retrieve relevant context using ChromaDB
- Generate grounded answers using Ollama
- Parse budget queries and calculate totals from a product CSV
- Expose both CLI and HTTP API interfaces

## Tech Stack
- LLM (chat): llama3:8b via Ollama
- Embeddings: nomic-embed-text via Ollama
- Vector DB: ChromaDB (local persistence)
- Agent runtime: Custom logic (Agno integration optional)
- API: FastAPI + Uvicorn
- CLI: Python argparse
- Language: Python 3.13

## Data Sources
- data/faqs.md: Markdown file with frequently asked questions
- data/products.csv: Product list with names, categories, and prices

## Features
- FAQ Retrieval: Answers questions using embedded markdown chunks
- Budget Calculation: Parses quantities and plural forms from queries
- Citations: Answers include source and chunk references
- CLI Interface: Ask questions via command line
- HTTP API: Ask questions via /ask endpoint

## How to Run
1. Install dependencies
   pip install -r requirements.txt
   ollama pull llama3:8b
   ollama pull nomic-embed-text

2. Ingest documents
   python -c "from app.retriever import ingest_faq_documents; ingest_faq_documents('data')"

3. Run CLI
   python cli.py --query "Do you accept credit cards?"
   python cli.py --query "I want a budget for 1 hammer and 5 nails"

4. Run API
   uvicorn app.main:app --reload

5. Test API
   curl --get --data-urlencode "query=I want the budget for 2 hammers, 5 nails" http://localhost:8000/ask

## Mini-Missions Completed
- Hello RAG: Ingested markdown and queried
- CLI and HTTP API working
- Citations included in answers
- Quantity and plural handling in budget
- Model swap and chunk tuning optional
- Agnos AI integration optional

## Screencast Checklist
1. Show ingestion of markdown files
2. Ask a question via CLI
3. Ask a question via HTTP API
4. Demonstrate quantity and plural matching improvement

## Tradeoffs and Notes
- Ollama is used locally for both chat and embeddings
- ChromaDB provides fast local vector search
- Agnos AI orchestration can be added for modularity
- Plural normalization improves budget accuracy
- FastAPI makes the assistant easily integrable