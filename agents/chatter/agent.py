from google.adk.agents import Agent
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from LF.prompts import chatter_prompt
from agents.config import MODEL 
from agents.planner.agent import planner_tool
from agents.explainer.agent import explainer_tool
from agents.quizzer.agent import quizzer_tool
from agents.tracker.agent import tracker_tool

chatter_agent = Agent(
    name="chatter_agent",
    model=MODEL,
    description=(
        "Agent that interacts with the user and delegates tasks to other agents"
    ),
    instruction=(
        chatter_prompt
    ),
    tools=[planner_tool,explainer_tool,quizzer_tool,tracker_tool]
        )
