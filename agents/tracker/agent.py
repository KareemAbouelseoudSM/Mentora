from pydantic import BaseModel, Field
from typing import Literal
from agents.config import MODEL
from google.adk.agents import Agent
from google.adk.tools import agent_tool
from LF.prompts import tracker_prompt
from typing import Optional

class TrackerInput(BaseModel):
    topic: str = Field(description="The topic to be explained")
    notes: str = Field( description="Additional instructions if any, you can make this empty if you want to skip it or write none")

tracker_agent = Agent(
    name="tracker_agent",
    model=MODEL,
    description=(
        "Agent that tracks the user's progress and updates the curriculum"
    ),
    instruction=(
        tracker_prompt
    ),
    input_schema=TrackerInput
)

tracker_tool= agent_tool.AgentTool(agent=tracker_agent)