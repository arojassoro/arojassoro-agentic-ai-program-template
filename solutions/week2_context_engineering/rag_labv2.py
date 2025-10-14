import requests
import json
import chromadb
import argparse

# --- CLI Argument Parsing ---
parser = argparse.ArgumentParser(description="RAG FAQ Assistant")
parser.add_argument("--k", type=int, default=2, help="Number of top results to retrieve from ChromaDB")
parser.add_argument("--no-context", action="store_true", help="Disable context retrieval from ChromaDB")
args = parser.parse_args()

# --- 1. Configuration ---
OLLAMA_ENDPOINT = "http://localhost:11434/api"
OLLAMA_CONFIG = {
    "model": "llama3",
    "stream": False,
}
CHROMA_DB_PATH = "./chroma_db"
COLLECTION_NAME = "faq_collection"

# --- 2. Knowledge Base ---
# In a real-world scenario, this would come from a file, database, or API.
FAQ_DATA = [
    {"id": "faq1", "question": "What is the return policy?", "answer": "You can return any item within 30 days of purchase for a full refund."},
    {"id": "faq2", "question": "How do I track my order?", "answer": "Once your order has shipped, you will receive an email with a tracking number."},
    {"id": "faq3", "question": "Do you ship internationally?", "answer": "Yes, we ship to most countries worldwide. Shipping costs may vary."},
    {"id": "faq4", "question": "How can I contact customer support?", "answer": "You can reach our customer support team via email at support@example.com or by calling our toll-free number."},
    {"id": "faq5", "question": "What payment methods do you accept?", "answer": "We accept all major credit cards, PayPal, and Apple Pay."},
    {"id": "faq6", "question": "Can I change my shipping address?", "answer": "If your order has not yet shipped, you can contact customer support to update your shipping address."},
    {"id": "faq7", "question": "What are your business hours?", "answer": "Our customer support is available Monday to Friday, from 9 AM to 5 PM EST."},
    {"id": "faq8", "question": "Do you offer gift wrapping?", "answer": "Yes, we offer gift wrapping for an additional fee. You can select this option at checkout."},
    {"id": "faq9", "question": "How do I use a discount code?", "answer": "You can apply your discount code in the 'Promo Code' box at checkout."},
    {"id": "faq10", "question": "What if my item is damaged?", "answer": "If your item arrives damaged, please contact customer support immediately for a replacement or refund."}
]

# --- 3. ChromaDB Setup ---
client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
collection = client.get_or_create_collection(name=COLLECTION_NAME)

# --- 4. Helper Functions ---

def get_embedding(text):
    """
    Generates an embedding for the given text using the Ollama API.
    """
    try:
        response = requests.post(
            f"{OLLAMA_ENDPOINT}/embeddings",
            json={"model": OLLAMA_CONFIG["model"], "prompt": text}
        )
        response.raise_for_status()
        return response.json()["embedding"]
    except requests.exceptions.RequestException as e:
        print(f"Error getting embedding: {e}")
        return None

def index_knowledge_base():
    """
    Indexes the knowledge base into ChromaDB.
    """
    print("Indexing knowledge base...")
    for item in FAQ_DATA:
        # We are embedding the questions to find similar user queries.
        embedding = get_embedding(item["question"])
        if embedding:
            collection.add(
                ids=[item["id"]],
                embeddings=[embedding],
                documents=[item["answer"]],  # Store the answer as the document
                metadatas=[{"question": item["question"]}]
            )
    print("Indexing complete.")


def query_rag_agent(user_query, k, use_context=True):
    print(f"\n--- Querying for: '{user_query}' with k={k}, use_context={use_context} ---")

    retrieved_context = ""
    source_ids = []

    if use_context:
        query_embedding = get_embedding(user_query)
        if not query_embedding:
            return "Sorry, I couldn't process your query."

        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=k,
            include=["documents", "metadatas"]
        )

        for i, (doc, metadata, doc_id) in enumerate(zip(
            results['documents'][0],
            results['metadatas'][0],
            results['ids'][0]
        ), start=1):
            retrieved_context += f"\n--- Section {i} (Source: {doc_id}) ---\n{doc}\n"
            source_ids.append(doc_id)

        if not retrieved_context:
            retrieved_context = "No relevant information found."
    else:
        retrieved_context = "No context provided. Answer based only on the user query."

    print(f"Retrieved context: {retrieved_context}")

    # 3. Construct the prompt for the LLM
    prompt = f"""
    You are a helpful FAQ assistant. A user has asked the following question:
    '{user_query}'

    Here is some context that might be relevant:
    '{retrieved_context}'

    Based on this context, please provide a clear and concise answer. If the context is not relevant, say so.
    
    At the end of your answer, include a list of the source FAQ IDs used in the format: [faq1, faq2]
    """

    # 4. Send the prompt to the LLM
    try:
        response = requests.post(
            f"{OLLAMA_ENDPOINT}/generate",
            json={"prompt": prompt, **OLLAMA_CONFIG}
        )
        response.raise_for_status()
        model_answer = json.loads(response.text)["response"]
        return f"{model_answer}\n\nSources: {source_ids if use_context else '[]'}"
    except requests.exceptions.RequestException as e:
        return f"Error communicating with the model: {e}"

# --- 5. Main Execution ---
if __name__ == "__main__":
    # Check if the collection is empty before indexing   
    if collection.count() == 0 and not args.no_context:
        index_knowledge_base()
    elif not args.no_context:
        print("Knowledge base is already indexed.")


    # --- Test Queries ---
    test_queries = [
        "How can I return a product?",
        "What's the process for tracking my package?",
        "Do you ship to Canada?",
        "What are the support hours?",
        "Can I pay with Bitcoin?" # A question not in the knowledge base
    ]

    for query in test_queries:
        answer = query_rag_agent(query, args.k, use_context=not args.no_context)
        print(f"Answer: {answer}")
