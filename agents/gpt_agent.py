import os
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
import asyncio

class GPTAgent:
    def __init__(self):
        api_key = os.environ.get("GOOGLE_API_KEY")

        if not api_key:
            raise ValueError(
                "GOOGLE_API_KEY environment variable not set. "
                "Please set your Gemini API key in your .env file and ensure it's loaded."
            )

        try:
            self.agent = Agent(
                name="genetic_wellness_agent",
                model="gemini-1.5-flash",
                instruction="You are an expert in genetic wellness. Answer user questions clearly and concisely. If you don't know the answer, state that you cannot provide it based on your knowledge.",
            )

            self.session_service = InMemorySessionService()
            self.runner = Runner(
                agent=self.agent,
                app_name="nu_genomics_app",
                session_service=self.session_service
            )

            self.user_id = "default_user"
            self.session_id = "default_session"

            print("GPTAgent initialized successfully using Google ADK.")

            # --- DEBUGGING ADDITION: Test basic connectivity during init ---
            print("\n--- DEBUG: Performing ADK connectivity test ---")
            try:
                async def _test_connectivity_async():
                    test_session = await self.session_service.get_session(
                        app_name=self.runner.app_name,
                        user_id=self.user_id,
                        session_id=self.session_id
                    )
                    if not test_session:
                        print(f"DEBUG: Creating session '{self.session_id}' for init test.")
                        await self.session_service.create_session(
                            app_name=self.runner.app_name,
                            user_id=self.user_id,
                            session_id=self.session_id
                        )

                    test_message_content = types.Content(role='user', parts=[types.Part(text="Hello, Gemini!")])
                    # CRITICAL CHANGE: REMOVE 'await' here. runner.run() returns a synchronous generator.
                    test_events = self.runner.run(user_id=self.user_id, session_id=self.session_id, new_message=test_message_content)
                    
                    test_response_text = ""
                    # CRITICAL CHANGE: Use a regular 'for' loop for iteration.
                    for event in test_events: 
                        print(f"DEBUG: Init test event received: {event}")
                        if event.content and event.content.parts:
                            for part in event.content.parts:
                                if part.text:
                                    test_response_text += part.text
                    return test_response_text

                test_response_text_sync = asyncio.run(_test_connectivity_async())
                
                if test_response_text_sync:
                    print(f"DEBUG: ADK connectivity test successful. Response snippet: '{test_response_text_sync[:100]}...'")
                else:
                    print("DEBUG: ADK connectivity test failed: Received empty response for 'Hello, Gemini!'.")
            except Exception as e:
                print(f"DEBUG: ADK connectivity test failed with exception during run: {e}")
            print("--- DEBUG: ADK connectivity test complete ---\n")

        except Exception as e:
            print(f"ERROR: Error initializing Google ADK Agent or Runner: {e}")
            raise

    async def get_answer(self, user_input):
        try:
            session = await self.session_service.get_session(
                app_name=self.runner.app_name,
                user_id=self.user_id,
                session_id=self.session_id
            )
            if not session:
                print(f"DEBUG: Session '{self.session_id}' not found for query. Creating a new one.")
                await self.session_service.create_session(
                    app_name=self.runner.app_name,
                    user_id=self.user_id,
                    session_id=self.session_id
                )
            
            new_message_content = types.Content(
                role='user',
                parts=[types.Part(text=user_input)]
            )
            
            print(f"DEBUG: Sending query to ADK: '{user_input}' for session '{self.session_id}'")
            
            # CRITICAL CHANGE: REMOVE 'await' here. runner.run() returns a synchronous generator.
            events = self.runner.run(
                user_id=self.user_id,
                session_id=self.session_id,
                new_message=new_message_content
            )
            
            final_response_text = ""
            event_count = 0
            print("DEBUG: Iterating through events from ADK Runner:")
            # CRITICAL CHANGE: Use a regular 'for' loop for iteration.
            for event in events:
                event_count += 1
                print(f"DEBUG: Event #{event_count}: {event}")
                if event.content and event.content.parts:
                    for part in event.content.parts:
                        print(f"DEBUG: Part from event: {part}")
                        if part.text:
                            final_response_text += part.text
            
            print(f"DEBUG: Total events received: {event_count}")
            print(f"DEBUG: Final response text collected: '{final_response_text}'")

            if final_response_text:
                return final_response_text
            else:
                return "I'm sorry, I couldn't get a clear response from the genetic wellness information. This might be due to an empty model response, API key issue, or network problem."
        except Exception as e:
            print(f"ERROR: Exception during ADK Agent query in get_answer: {e}")
            return f"An error occurred while fetching genetic wellness information: {str(e)}. Please check your console for full error details."