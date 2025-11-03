"""
retriever.py

Manages document ingestion, chunking, embedding, and retrieval using ChromaDB.
Also handles loading product data from CSV and generating budgets.

Responsibilities:
- Ingest markdown FAQ documents into ChromaDB with chunking and embeddings
- Retrieve relevant document chunks based on user queries
- Load product data from CSV for budget calculations
- Generate budget summaries based on user-specified materials

Usage:
- Call `ingest_faq_documents(data_dir)` to ingest markdown files
- Call `retrieve_faq(query)` to retrieve relevant chunks
- Call `load_products_csv(csv_path)` to load product data
- Call `generate_budget(product_list, products_db)` to calculate total cost

Dependencies:
- ChromaDB with duckdb+parquet persistence
- Ollama embedding model (e.g., nomic-embed-text) must be available

Example:
    ingest_faq_documents("data")
    results = retrieve_faq("Do you offer delivery?")
    products = load_products_csv("data/products.csv")
    budget = generate_budget(["hammer", "paint (1L)"], products)
"""

import os
import csv
from typing import List, Dict
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
import inflect

CHUNK_SIZE = 300
CHUNK_OVERLAP = 50

# Initialize ChromaDB client
client = chromadb.PersistentClient(path="./vector_store/chromadb")

# Embedding function using Ollama
embedding_fn = embedding_functions.OllamaEmbeddingFunction(
    model_name="nomic-embed-text"
)

# Create or get collection
collection = client.get_or_create_collection(
    name="faqs",
    embedding_function=embedding_fn
)

# -------------------------------
# Part A: Markdown ingestion
# -------------------------------
def load_markdown_files(data_dir: str) -> List[Dict]:
    docs = []
    for filename in os.listdir(data_dir):
        if filename.endswith(".md"):
            path = os.path.join(data_dir, filename)
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
                docs.append({"source": filename, "text": text})
    return docs

def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> List[str]:
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

def ingest_faq_documents(data_dir: str):
    docs = load_markdown_files(data_dir)
    for doc in docs:
        chunks = chunk_text(doc["text"])
        for i, chunk in enumerate(chunks):
            collection.add(
                documents=[chunk],
                metadatas=[{"source": doc["source"], "chunk": i}],
                ids=[f"{doc['source']}_chunk_{i}"]
            )
    client.persist()
    print("FAQ ingestion complete.")

def retrieve_faq(query: str, k: int = 5):
    results = collection.query(query_texts=[query], n_results=k)
    return results

# -------------------------------
# Part B: Product CSV ingestion
# -------------------------------
p = inflect.engine()

def load_products_csv(csv_path: str) -> Dict[str, Dict]:
    products = {}
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name = row["product_name"].strip().lower()
            products[name] = {
                "category": row["category"],
                "price": float(row["price"])
            }
    return products

def generate_budget(product_list: List[tuple], products_db: Dict[str, Dict]) -> Dict:
    found_items = {}
    not_found_items = []
    total = 0.0

    # Normalize product DB keys to singular form
    normalized_db = {
        p.singular_noun(name) or name: data
        for name, data in products_db.items()
    }

    for name, quantity in product_list:
        singular_name = p.singular_noun(name) or name
        key = singular_name.lower()

        if quantity == 1:
            display_name = singular_name
        else:
            display_name = p.plural(singular_name)

        item_label = f"{quantity} {display_name}"

        if key in normalized_db:
            price = normalized_db[key]["price"]
            item_total = price * quantity
            found_items[item_label] = item_total
            total += item_total
        else:
            not_found_items.append(item_label)

    return {
        "found": found_items,
        "not_found": not_found_items,
        "total": total
    }
