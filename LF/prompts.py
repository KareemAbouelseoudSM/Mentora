from langfuse import Langfuse
import os
from dotenv import load_dotenv

load_dotenv()

langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_HOST")
)
chatter_prompt = langfuse.get_prompt("chatter_prompt").prompt[0]['content']
planner_prompt = langfuse.get_prompt("planner_prompt").prompt[0]['content']
explainer_prompt = langfuse.get_prompt("explainer_prompt").prompt[0]['content']
quizzer_prompt = langfuse.get_prompt("quizzer_prompt").prompt[0]['content']
tracker_prompt = langfuse.get_prompt("tracker_prompt").prompt[0]['content']




print('hi')
