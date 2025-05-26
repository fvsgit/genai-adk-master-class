from google.adk.agents import Agent
from google.adk.tools import google_search
from datetime import datetime

def get_current_time() -> dict:
    """
    Get the current time in the format YYYY-MM-DD HH:MM:SS
    """

    return {
        "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

root_agent = Agent(
    model='gemini-2.0-flash-001',
    name='too_agent',
    description='Tool Agent',
    instruction="""
    You are a helpful assistant that can use the following tools:
    - google_search
    """,
    tools=[google_search], # Calling built-in tools
    #tools=[get_current_time], # Calling function tools 
    #tools=[google_search, get_current_time], # Calling built-in and function tools together -> Not working as of writing!
)
