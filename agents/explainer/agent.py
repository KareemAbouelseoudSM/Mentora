from pydantic import BaseModel, Field
from typing import Literal
from typing import Optional
import os
from agents.config import MODEL, TARGET_FOLDER_PATH
from google.adk.agents import LlmAgent
from google.adk.tools import agent_tool
from LF.prompts import explainer_prompt
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioConnectionParams, StdioServerParameters


class ExplainerInput(BaseModel):
    topic: str = Field(description="The topic to be explained, make it more descriptive.")
    difficulty: Literal["easy", "medium", "hard"] = Field(description="The difficulty of the topic")
    notes: str = Field(description="Additional instructions if any, you can make this empty if you want to skip it or write none")

explainer_agent = LlmAgent(
    name="explainer_agent",
    model=MODEL,
    description=(
        "Agent that explains the topic to the user"
    ),
    instruction=(
        explainer_prompt
        ),
    input_schema=ExplainerInput,
    tools=[
        MCPToolset(
                connection_params=StdioConnectionParams(
                    server_params = StdioServerParameters(
                        command='python3',
                        args=[os.path.join('mentora_mcp', 'mentora.py')],
                    ),
                ),
                tool_filter=['wikipedia_search']
            )
    ],   
)
explainer_tool= agent_tool.AgentTool(agent=explainer_agent)
