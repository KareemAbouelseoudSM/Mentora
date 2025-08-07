from pydantic import BaseModel, Field
from typing import Literal,Optional
from agents.config import MODEL
from google.adk.agents import Agent
from google.adk.tools import agent_tool
from LF.prompts import quizzer_prompt
class QuizzerInput(BaseModel):
    topic: str = Field(description="The topic to be explained")
    difficulty: Literal["easy", "medium", "hard"] = Field(description="The difficulty of the topic")
    notes: str = Field( description="Additional instructions if any, you can make this empty if you want to skip it or write none")

quizzer_agent = Agent(
    name="quizzer_agent",
    model=MODEL,
    description=(
        "Agent that creates quizzes for the user"
    ),
    instruction=(
        quizzer_prompt
    ),
    input_schema=QuizzerInput
)

quizzer_tool= agent_tool.AgentTool(agent=quizzer_agent)