from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from src.planner.tools.search_tool import AzureBingSearchTool
import os


@CrewBase
class ChatbotCrew():
    """CrewAI Chatbot Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def local_thai_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["local_thai_agent"],
            llm=os.getenv("AZURE_OPENAI_MODEL"),
            verbose=True,
            tools=[AzureBingSearchTool()],
        )

    @task
    def local_thai_task(self) -> Task:
        return Task(
            config=self.tasks_config["local_thai_task"],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Chatbot Crew"""

        return Crew(
            agents=self.agents,     # Automatically created by the @agent decorator
            tasks=self.tasks,       # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
