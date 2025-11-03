"""
rag_agent.py

Main orchestration logic for the Docs-to-Answers RAG Assistant.
Determines query type (FAQ or Budget), retrieves context, and generates responses.

Dependencies:
- retriever.py for document and product retrieval
- llm.py for answer generation
"""

import re
import inflect
from app.retriever import retrieve_faq, load_products_csv, generate_budget
from app.llm import generate_answer

p = inflect.engine()

def is_budget_query(query: str) -> bool:
    return "budget for" in query.lower()

def extract_product_list(query: str) -> list:
    match = re.search(r"budget for (.+)", query.lower())
    if not match:
        return []

    items = match.group(1)
    items = items.replace(" and ", ",")  # Normalize 'and' to comma
    parsed_items = []
    for item in items.split(","):
        item = item.strip()
        qty_match = re.match(r"(\d+)\s+(.*)", item)
        if qty_match:
            quantity = int(qty_match.group(1))
            name = qty_match.group(2).strip()
        else:
            quantity = 1
            name = item

        singular_name = p.singular_noun(name) or name
        parsed_items.append((singular_name, quantity))
    return parsed_items

def ask(query: str) -> str:
    if is_budget_query(query):
        product_list = extract_product_list(query)
        products_db = load_products_csv("data/products.csv")
        budget = generate_budget(product_list, products_db)

        lines = []
        for item, price in budget["found"].items():
            lines.append(f"{item}: ${price:.2f}")
        lines.append(f"Total: ${budget['total']:.2f}")

        if budget["not_found"]:
            lines.append("\nThe following items were not found:")
            for item in budget["not_found"]:
                lines.append(f"- {item}")

        return "\n".join(lines)
    else:
        retrieved = retrieve_faq(query)
        answer = generate_answer(retrieved, query)
        return answer
