import uuid
from dotenv import load_dotenv

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from question_answering_agent import question_answering_agent  # Import the agent(s) you need to work with my folder name

# Global variables
APP_NAME = "Francois Bot"
USER_ID = "francois"
SESSION_ID = str(uuid.uuid4()) # Generate a unique sessionId

# Load the environment variables
load_dotenv()

# ------------------------------ Setup the state and session ------------------------------ #

# Define the object that holds the initial state when the agent starts
initial_state = {
    "user_name": "Francois",
    "user_preferences": """
        I like to play Pickleball, Disc Golf, and Tennis.
        My favorite food is Mexican.
        My favorite TV show is Game of Thrones.
        Loves it when people like and subscribe to his YouTube channel.
    """,
}

# Create the session service and setup the state
session_service_stateful = InMemorySessionService()
stateful_session = session_service_stateful.create_session(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID,
    state=initial_state,
)
print("CREATED NEW SESSION:")
print(f"\tSession ID: {SESSION_ID}")

# ------------------------------ Setup the rnner and run the agent ------------------------------ #

# We need to setup the runner and link it with the session
runner = Runner(
    agent=question_answering_agent, # Matches the folder name of the agent
    app_name=APP_NAME,
    session_service=session_service_stateful,
)

# Define a sample message to send to the agent
new_message = types.Content(
    role="user", parts=[types.Part(text="What is francois's favorite TV show?")]
)

# For each event in the runner, run it
for event in runner.run(
    user_id=USER_ID,
    session_id=SESSION_ID,
    new_message=new_message,
):
    # In the callback of the runner, we can check if the event is a final response
    if event.is_final_response():

        # Check if the event has content and parts and print it
        if event.content and event.content.parts:
            print(f"Final Response: {event.content.parts[0].text}")

# Debug the session state
print("==== Session Event Exploration ====")
session = session_service_stateful.get_session(
    app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
)

# Log final Session state
print("=== Final Session State ===")
for key, value in session.state.items():
    print(f"{key}: {value}")