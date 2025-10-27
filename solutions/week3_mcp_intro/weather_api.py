from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from mcp_weather_tool import invoke_get_weather, TOOL_DESCRIPTOR
import time

app = FastAPI(title="MCP Weather Tool", description=TOOL_DESCRIPTOR["description"])

@app.get("/weather")
def get_weather(city: str = Query(..., description="City name (ASCII)")):
    start = time.time()
    try:
        result = invoke_get_weather(city)
        latency = round((time.time() - start) * 1000, 2)
        return JSONResponse(content={
            "request": {"tool": TOOL_DESCRIPTOR["name"], "params": {"city": city}},
            "response": result,
            "latency_ms": latency
        })
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})

@app.get("/descriptor")
def get_descriptor():
    return JSONResponse(content=TOOL_DESCRIPTOR)