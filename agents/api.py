from fastapi import FastAPI, Request
from pydantic import BaseModel
import uvicorn
import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.pipeline import call_chatter_agent,call_explainer_agent
from fastapi.responses import StreamingResponse
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioConnectionParams, StdioServerParameters
app = FastAPI()

class ChatterRequest(BaseModel):
    user_input: str
    session_id: str
    user_id: str

class ExplainerRequest(BaseModel):
    topic: str
    user_id: str
    session_id: str

@app.post("/chatter")
async def chatter_endpoint(request: ChatterRequest):
    return StreamingResponse(call_chatter_agent(user_input=request.user_input,session_id=request.session_id,user_id=request.user_id),media_type="text/event-stream")

@app.get("/check_mcp")
async def check_mcp():
    try:
        mcp_toolset = MCPToolset(
                connection_params=StdioConnectionParams(
                    server_params = StdioServerParameters(
                        command='python3',
                        args=[os.path.join('mentora_mcp', 'mentora.py')],
                    ),
                ),
                tool_filter=['wikipedia_search']
            )
        tools = await mcp_toolset.get_tools()
        
        # Extract only serializable information from tools
        tool_info = []
        for tool in tools:
            tool_info.append({
                "name": getattr(tool, 'name', str(tool)),
                "description": getattr(tool, 'description', ''),
                "type": type(tool).__name__,
            })
        
        return {"tools": tool_info, "count": len(tools)}
    except Exception as e:
        return {"error": str(e), "tools": [], "count": 0}

@app.post("/explain")
async def explainer_endpoint(request: ExplainerRequest):
     response= await call_explainer_agent(request.topic,request.session_id,request.user_id)
     return {"response": response}

if __name__ == "__main__":
    uvicorn.run("agents.api:app", host="0.0.0.0", port=8000, reload=True)