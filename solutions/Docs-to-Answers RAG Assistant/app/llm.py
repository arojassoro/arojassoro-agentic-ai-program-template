"""
llm.py

Handles interaction with the local Ollama LLM for generating answers based on retrieved context.

Responsibilities:
- Format and send prompts to Ollama's chat model (e.g., llama3:8b)
- Incorporate retrieved document chunks into the prompt
- Return grounded answers with citations (e.g., source#chunk)

Usage:
- Call `generate_answer(context_chunks, question)` with retrieved context and user query
- Ensure Ollama is running locally and the required model is pulled

Dependencies:
- Ollama must be installed and running on localhost:11434
- Requires the model specified in CHAT_MODEL to be available via Ollama

Example:
    from app.llm import generate_answer
    answer = generate_answer(retrieved_chunks, "What is your return policy?")
"""
import requests

OLLAMA_BASE_URL = "http://localhost:11434"
CHAT_MODEL = "llama3:8b"

def generate_answer(context_chunks: list, question: str) -> str:
    """
    Sends a prompt to Ollama's chat model with retrieved context and user question.
    Returns the generated answer.
    """
    context_text = "\n\n".join([
        f"[{meta['source']}#{meta['chunk']}] {doc}"
        for doc, meta in zip(context_chunks['documents'][0], context_chunks['metadatas'][0])
    ])

    prompt = f"""
You are a helpful assistant for a hardware store. Use ONLY the provided context to answer the question.
IMPORTANT: You must use the provided context. If the answer is found in the context, include the citation (source#chunk).
If the answer is not in the context, say "I don't know based on the provided information."
When requesting to sell a product that is not in the context say "We don't sell productname."
When asked for a price of a product that is not in the context say "We don't sell productname."
Do not assume the store have products that are not in the context.
Include citations in the format (source#chunk) when using retrieved content.

Context:
{context_text}

Question:
{question}

IMPORTANT: If you use any information from the context, you MUST include the citation (source#chunk).
"""
    
    response = requests.post(
        f"{OLLAMA_BASE_URL}/api/chat",
        json={
            "model": CHAT_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False  # This ensures the response is a single JSON object
        }
    )

    if response.status_code == 200:
        response_text = response.json()["message"]["content"]
        # Enforce citation
        if "(source#" not in response_text.lower():
            response_text = "I don't know based on the provided information."
        return response_text

    else:
        return f"Error: {response.status_code} - {response.text}"