from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from src.planner.tools.browser_tool import BrowserTool
from src.planner.tools.search_tool import AzureBingSearchTool
from src.planner.tools.hotel_tool import GoogleHotelSearchTool
from src.planner.tools.flight_tool import GoogleFlightsSearchTool
import os

@CrewBase
class ItineraryCrew():
    """Itinerary crew"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    ### Agents ###

    @agent
    def city_selection_expert(self) -> Agent:
        return Agent(
            config=self.agents_config['city_selection_expert'],
            llm=os.getenv("AZURE_OPENAI_MODEL"),
            verbose=True,
            max_rpm=6000,
            max_iter=20,
            tools=[AzureBingSearchTool(), BrowserTool()]
        )
    
    @agent
    def local_expert(self) -> Agent:
        return Agent(
            config=self.agents_config['local_expert'],
            llm=os.getenv("AZURE_OPENAI_MODEL"),
            verbose=True,
            max_rpm=6000,
            max_iter=100,
            tools=[AzureBingSearchTool(), BrowserTool()]
        )
    
    @agent
    def preitinerary_composer(self) -> Agent:
        return Agent(
            config=self.agents_config['preitinerary_composer'],
            llm=os.getenv("AZURE_OPENAI_MODEL"),
            verbose=True,
            max_rpm=6000,
            max_iter=40,
            tools=[AzureBingSearchTool(), BrowserTool()]
        )

    @agent
    def accommodation_advisor(self) -> Agent:
        return Agent(
            config=self.agents_config['accommodation_advisor'],
            llm=os.getenv("AZURE_OPENAI_MODEL"),
            verbose=True,
            max_rpm=6000,
            max_iter=20,
            tools=[GoogleHotelSearchTool()],
        )
    
    @agent
    def accommodation_picker(self) -> Agent:
        return Agent(
            config=self.agents_config['accommodation_picker'],
            llm=os.getenv("AZURE_OPENAI_MODEL"),
            verbose=True,
            max_rpm=6000,
            max_iter=20,
        )
    
    @agent
    def flight_advisor(self) -> Agent:
        return Agent(
            config=self.agents_config['flight_advisor'],
            llm=os.getenv("AZURE_OPENAI_MODEL"),
            verbose=True,
            max_rpm=6000,
            max_iter=20,
            tools=[GoogleFlightsSearchTool()]
        )
    
    @agent
    def flight_picker(self) -> Agent:
        return Agent(
            config=self.agents_config['flight_picker'],
            llm=os.getenv("AZURE_OPENAI_MODEL"),
            verbose=True,
            max_rpm=6000,
            max_iter=20,
        )
    
    ### Tasks ###
    
    @task
    def city_selection_task(self) -> Task:
        return Task(
            config=self.tasks_config['city_selection_task'],
        )

    @task
    def local_task(self) -> Task:
        return Task(
            config=self.tasks_config['local_task'],
            output_file="result/planner/places.txt",
        )
    
    @task
    def preitinerary_task(self) -> Task:
        return Task(
            config=self.tasks_config['preitinerary_task'],
            output_file="log/planner/preitinerary1.txt",
        )
    
    @task
    def hotels_suggestion_task(self) -> Task:
        return Task(
            config=self.tasks_config['hotels_suggestion_task'],
            output_file="result/planner/hotels.txt",
        )
    
    @task
    def choose_hotel_task(self) -> Task:
        return Task(
            config=self.tasks_config['choose_hotel_task'],
            output_file="log/planner/preitinerary2.txt",
        )
    
    @task
    def flight_suggestion_task(self) -> Task:
        return Task(
            config=self.tasks_config['flight_suggestion_task'],
            output_file="result/planner/flights.txt",
        )
    
    @task
    def choose_flight_task(self) -> Task:
        return Task(
            config=self.tasks_config['choose_flight_task'],
            output_file="log/planner/full_itinerary.txt"
        )
    
    @crew
    def crew(self) -> Crew:
        """Creates the TravelPlanner crew"""

        return Crew(
            agents=self.agents,     # Automatically created by the @agent decorator
            tasks=self.tasks,       # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
