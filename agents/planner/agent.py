from google.adk.agents import Agent
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from LF.prompts import planner_prompt
from google.adk.tools import agent_tool
from agents.config import MODEL
from pydantic import BaseModel, Field
from typing import Literal
from typing import Optional

class PlannerOutput(BaseModel):
    curriculum: list[str] = Field(description="The topics to be covered in the curriculum")
    time_needed: str = Field(description="The time needed to cover the curriculum")
    reasoning: str = Field(description="Explain why this topic is next")
    action: Literal["explain", "quiz", "retry", "skip",'harder_topic','easier_topic'] = Field(description="The action to be taken")
    notes: str = Field(description="Additional instructions if any, you can make this empty if you want to skip it or write none")
class PlannerInput(BaseModel):
    topic: str = Field(description="The topic to be explained")
    notes: str = Field(description="Additional instructions if any, you can make this empty if you want to skip it or write none")
    time_needed: str = Field(description="The time needed to cover the curriculum")
    
planner_agent = Agent(
    name="planner_agent",
    model=MODEL,
    description=(
        "Agent that creates a curriculum for the user"
    ),
    instruction=(
        planner_prompt
    ),
    input_schema=PlannerInput,
    output_schema=PlannerOutput,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

planner_tool= agent_tool.AgentTool(agent=planner_agent)