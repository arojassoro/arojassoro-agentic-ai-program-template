"""Minimal agent runner that simulates MCP-style tool registration and invocation.

Flow:
1. Load tool descriptor (import from mcp_weather_tool)
2. Parse user natural language query for weather intent (regex/keywords)
3. If intent detected: extract city, invoke tool (function or HTTP)
4. Construct answer citing tool data (avoid hallucination)
5. Log structured record (JSON) for Playbook usage

NOTE: This is an instructional scaffold, not a production MCP client.
"""
from __future__ import annotations
import argparse
import requests
import json
import re
import time
from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any

try:
    from mcp_weather_tool import invoke_get_weather, TOOL_DESCRIPTOR  # type: ignore
except ImportError:  # pragma: no cover
    raise SystemExit("Run from project root so Python can resolve mcp_weather_tool.")

WEATHER_PATTERN = re.compile(r"weather (?:in|at|for) (?P<city>[A-Za-z\-\s]+)\??", re.IGNORECASE)
ALLOWED_CITIES = {"San Jose", "Madrid", "New York"}

@dataclass
class InvocationLog:
    query: str
    intent: Optional[str]
    tool_used: bool
    params: Dict[str, Any]
    success: bool
    latency_ms: float
    error: Optional[str]
    answer: str


def build_answer_from_api(query: str, api_url: str = "http://127.0.0.1:8765/weather"):
    # Extract city using regex
    import re
    match = re.search(r"\bweather\s+(?:in|at|for)\s+(?P<city>[A-Za-z\s\-]+)", query, re.IGNORECASE)
    if not match:
        return {
            "query": query,
            "answer": "I can help with weather if you ask like 'weather in <city>'.",
            "latency_ms": 0.0,
            "success" : False,
            "tool_used": False,
            "tool": None
        }

    city = match.group("city").strip().title()
    
    # Check if city is allowed
    if city not in ALLOWED_CITIES:
        return {
            "query": query,
            "answer": f"Sorry, I only support weather queries for: {', '.join(ALLOWED_CITIES)}.",
            "latency_ms": 0.0,
            "success": False,
            "tool_used": False,
            "tool": None
        }

    start = time.time()

    # Call the API
    try:
        response = requests.get(api_url, params={"city": city})
        response.raise_for_status()
        data = response.json()
        latency_ms = round((time.time() - start) * 1000, 2)

        tool_result = data["response"]
        return {
            "query": query,
            "answer": f"Weather for {tool_result['city']}: {tool_result['temp_c']}°C, {tool_result['conditions']}.",
            "latency_ms": latency_ms,
            "success" : True,
            "tool_used": True,
            "tool": {
                "name": "get_weather",
                "params": {"city": city},
                "result": tool_result,
                "timestamp": tool_result["timestamp"]
            }
        }

    except Exception as e:
        return {
            "query": query,
            "answer": f"Error retrieving weather: {str(e)}",
            "latency_ms": latency_ms,
            "success" : False,
            "tool_used": False,
            "tool": None
        }

def parse_intent(query: str) -> Optional[str]:
    if WEATHER_PATTERN.search(query):
        return "get_weather"
    return None


def extract_city(query: str) -> Optional[str]:
    m = WEATHER_PATTERN.search(query)
    return m.group("city").strip() if m else None


def answer_without_tool(query: str) -> str:
    return (
        "I can provide weather if you phrase it like 'weather in <city>'. "
        "Try again specifying a city."
    )
    

def build_structured_answer(query: str, weather: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "query": query,
        "answer": f"Weather for {weather['city']}: {weather['temp_c']}°C, {weather['conditions']}.",
        "tool": {
            "name": TOOL_DESCRIPTOR["name"],
            "params": {"city": weather["city"]},
            "result": weather,
            "timestamp": weather["timestamp"]
        }
    }
        

def mcp_weather_wrapper(query: str):
    print(f"Parsing query: '{query}'")

    match = WEATHER_PATTERN.search(query)
    if not match:
        print("No weather intent detected.")
        return {
            "intent": None,
            "response": "I can help with weather if you ask like 'weather in <city>'."
        }

    city = match.group("city").strip()
    
    if not city:
        print("City name not found.")
        return {
            "intent": "get_weather",
            "response": "Need city name. Try asking like 'weather in <city>'."
        }

    request = {
        "tool": TOOL_DESCRIPTOR["name"],
        "params": {"city": city},
        "timestamp": int(time.time())
    }

    print("Request:")
    print(json.dumps(request, indent=2))

    try:
        result = invoke_get_weather(city)
        response = {
            "result": result,
            "timestamp": int(time.time())
        }
        print("\nResponse:")
        print(json.dumps(response, indent=2))
        return build_structured_answer(query, result)
    except Exception as e:
        error_response = {
            "error": str(e),
            "timestamp": int(time.time())
        }
        print("\nError:")
        print(json.dumps(error_response, indent=2))
        return error_response

def main():
    parser = argparse.ArgumentParser(description="Minimal MCP-style agent runner")
    parser.add_argument("--query", type=str, required=True, help="User natural language query")
    parser.add_argument("--log-json", type=str, help="Optional path to append JSON log line")
    args = parser.parse_args()

    result = build_answer_from_api(args.query)
    
    print("\nFinal Output:")
    print(json.dumps(result, indent=2))


    if args.log_json:
        with open(args.log_json, "a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(log)) + "\n")
            print(f"Appended log to {args.log_json}")


if __name__ == "__main__":  # pragma: no cover
    main()
