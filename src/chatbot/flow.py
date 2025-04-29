import random
from typing import Any, Dict, List
from pydantic import BaseModel
from crewai.flow.flow import Flow, listen, router, start
from dotenv import load_dotenv
from litellm import completion
from src.chatbot.crews.chatbot_crew.chatbot_crew import ChatbotCrew
import os

## set ENV variables
load_dotenv()
os.environ["AZURE_API_KEY"] = os.getenv("AZURE_API_KEY")
os.environ["AZURE_API_BASE"] = os.getenv("AZURE_API_BASE")
os.environ["AZURE_API_VERSION"] = os.getenv("AZURE_API_VERSION")

# Define flow state
class ChatbotState(BaseModel):
    query: str = "" # user's query from chatbot

# Create a flow class
class ChatbotFlow(Flow[ChatbotState]):

    model: str = os.getenv("AZURE_OPENAI_MODEL")

    @start()
    def initialize_model(self):
        pass
    
    @router(initialize_model)
    def is_about_thai(self):
        answer_is_thai = completion(
            model=self.model,
            temperature=0.0,
            messages=[
                {
                    "role": "assistant", 
                    "content": "You are a triage agent. "
                        "Your job is to determine whether the user's query is about Thai. "
                        "Your answer is binary, just say either 'yes' or 'no'. "
                        "You must not say any extra words and characters.\n\n"
                        "Example:\n"
                        "User: Who is the president of the US?\n"
                        "Answer: no\n\n"
                        "User: Where is Thailand?\n"
                        "Answer: yes"
                },
                {
                    "role": "user",
                    "content": self.state.query
                }
            ],
        )

        answer_is_thai = answer_is_thai["choices"][0]["message"]["content"]

        return answer_is_thai.lower()
    
    @listen("yes")
    def crew_answer_query(self):
        answer_query = ChatbotCrew().crew().kickoff(
            inputs={"query": self.state.query}).raw
        return answer_query

    @listen("no")
    def crew_reject_query(self):
        rejection_choices = [
            "I’m focused on all things Thailand! Feel free to ask me anything about the country, and I’ll be happy to assist.",
            "I can only help with information about Thailand at the moment. If you have questions about Thai culture, geography, or anything else related to the country, feel free to ask!",
            "This is outside my scope, as I specialize in Thai topics. Let me know if you have any questions about Thailand, and I’ll gladly assist.",
            "I’m designed to answer questions about Thailand. If you’re looking for information on Thai cities, culture, or local events, I’m the right place!",
            "Sorry, I’m all about Thailand! If you’d like recommendations or info related to the country, I’m here to help.",
        ]

        rejection_answer = random.choice(rejection_choices)
        return rejection_answer
