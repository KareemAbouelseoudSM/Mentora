
import json # Needed for pretty printing dicts

from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from pydantic import BaseModel, Field
import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.chatter.agent import chatter_agent
from agents.planner.agent import planner_tool
from agents.explainer.agent import explainer_tool,explainer_agent
from agents.quizzer.agent import quizzer_tool
from agents.tracker.agent import tracker_tool
from langfuse import get_client
langfuse = get_client()
from agents.config import APP_NAME,config
# Initialize session service and runner
session_service = InMemorySessionService()
chatter_runner = Runner(
        agent=chatter_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )
explainer_runner = Runner(
        agent=explainer_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )
async def call_explainer_agent(topic, session_id, user_id):
    session = await session_service.create_session(app_name="Mentora", user_id=user_id, session_id=session_id)
    user_content = types.Content(role='user', parts=[types.Part(text=topic)])

    async for event in explainer_runner.run_async(user_id=user_id, session_id=session_id, new_message=user_content):
        if event.is_final_response() and event.content and event.content.parts:
            final_response_content = event.content.parts[0].text
            return final_response_content
        
async def call_chatter_agent(user_input, session_id, user_id):
    try:
        # Try to get existing session first
        session = await session_service.get_session(session_id=session_id,user_id=user_id,app_name="Mentora")
        print(f"Found existing session: {session.id}")
    except:
        # Create new session if it doesn't exist
        session = await session_service.create_session(app_name="Mentora", user_id=user_id, session_id=session_id)
        print(f"Created new session: {session.id}")
    
    print("--------------------------------")
    print(f"Session ID: {session.id}")
    print(f"User ID: {user_id}")
    
    user_content = types.Content(role='user', parts=[types.Part(text=user_input)])
    final_response_content = "No final response received."

    # Use the session ID from the session object
    async for event in chatter_runner.run_async(user_id=user_id, session_id=session.id, new_message=user_content,run_config=config):
        func_tools = event.get_function_calls()
        print(event)
        if event.is_final_response() and event.content and event.content.parts:
            # For output_schema, the content is the JSON string itself
            final_response_content = event.content.parts[0].text
        elif func_tools:
            print(func_tools)
        elif event.content.role == 'model' and event.content.parts[0].text != '':  
            yield event.content.parts[0].text


