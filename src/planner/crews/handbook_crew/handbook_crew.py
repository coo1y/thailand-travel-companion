from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import FileReadTool
from src.planner.tools.browser_tool import BrowserTool
from src.planner.tools.calculator_tool import CalculatorTool
from src.planner.tools.search_tool import AzureBingSearchTool
import os


@CrewBase
class TravelHandbookCrew():
    """Travel Handbook crew"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    ### Agents ###

    @agent
    def transportation_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config['transportation_specialist'],
            llm=os.getenv("AZURE_OPENAI_MODEL"),
            verbose=True,
            max_rpm=6000,
            max_iter=100,
            tools=[AzureBingSearchTool(), BrowserTool(), CalculatorTool()]
        )
    
    @agent
    def cost_summary_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['cost_summary_agent'],
            llm=os.getenv("AZURE_OPENAI_MODEL"),
            verbose=True,
            max_rpm=6000,
            max_iter=20,
            tools=[CalculatorTool()],
        )
    
    @agent
    def weather_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['weather_agent'],
            llm=os.getenv("AZURE_OPENAI_MODEL"),
            verbose=True,
            max_rpm=6000,
            max_iter=20,
            tools=[AzureBingSearchTool(), BrowserTool()],
        )

    @agent
    def travel_essentials_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['travel_essentials_agent'],
            llm=os.getenv("AZURE_OPENAI_MODEL"),
            verbose=True,
            max_rpm=6000,
            max_iter=100,
            tools=[AzureBingSearchTool(), BrowserTool()],
        )
    
    @agent
    def html_generator(self) -> Agent:
        return Agent(
            config=self.agents_config['html_generator'],
            llm=os.getenv("AZURE_OPENAI_MODEL"),
            verbose=True,
            max_rpm=6000,
            max_iter=100,
            tools=[
                FileReadTool(file_path='template/handbook.html'), 
                FileReadTool(file_path='result/places.txt'), 
                FileReadTool(file_path='result/flights.txt'), 
                FileReadTool(file_path='result/hotels.txt'),
                ],
        )
    
    ### Tasks ###
    
    @task
    def determine_transport_task(self) -> Task:
        return Task(
            config=self.tasks_config['determine_transport_task'],
            output_file="log/planner/transport.txt",
        )

    @task
    def summarize_costs_task(self) -> Task:
        return Task(
            config=self.tasks_config['summarize_costs_task'],
            output_file="log/planner/cost_summary.txt",
        )
    
    @task
    def weather_forecast_task(self) -> Task:
        return Task(
            config=self.tasks_config['weather_forecast_task'],
            output_file="log/planner/weather.txt",
        )
    
    @task
    def travel_essentials_task(self) -> Task:
        return Task(
            config=self.tasks_config['travel_essentials_task'],
            output_file="log/planner/travel_essentials.txt",
        )
    
    @task
    def render_handbook_task(self) -> Task:
        return Task(
            config=self.tasks_config['render_handbook_task'],
            output_file="result/planner/travel_handbook.html"
        )
    
    @crew
    def crew(self) -> Crew:
        """Creates the TravelHandbook crew"""

        return Crew(
            agents=self.agents,     # Automatically created by the @agent decorator
            tasks=self.tasks,       # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
