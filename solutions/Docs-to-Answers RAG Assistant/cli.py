"""
cli.py

Command-line interface for interacting with the Docs-to-Answers RAG Assistant.

Usage:
    python cli.py --query "Do you accept credit cards?"

If no query is provided, it will enter interactive mode.

Type 'exit' to quit interactive mode.
"""

import argparse
import requests

def main():
    parser = argparse.ArgumentParser(description="Hardware Store RAG Assistant CLI")
    parser.add_argument("--query", type=str, help="Your question or budget request")
    args = parser.parse_args()

    if args.query:
        try:
            response = requests.get("http://localhost:8000/ask", params={"query": args.query})
            data = response.json()
            print("\nResponse:\n")
            print(data["response"])
        except Exception as e:
            print(f"Error contacting API: {e}")
    else:
        print("Please provide a query using --query")

if __name__ == "__main__":
    main()