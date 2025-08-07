from google.adk.agents.run_config import RunConfig, StreamingMode
import os

config = RunConfig(
    streaming_mode=StreamingMode.SSE,
)

MODEL = "gemini-2.0-flash"
APP_NAME = "Mentora"

# MCP Filesystem target folder - this will be used for file operations
# Create the folder if it doesn't exist
TARGET_FOLDER_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "mcp_files")
os.makedirs(TARGET_FOLDER_PATH, exist_ok=True)