from typing import Any, Dict, List
from pydantic import BaseModel
from crewai.flow.flow import Flow, listen, start
from src.planner.crews.itinerary_crew.itinerary_crew import ItineraryCrew
from src.planner.crews.handbook_crew.handbook_crew import TravelHandbookCrew


# Define flow state
class SoloTravelPlannerState(BaseModel):
    passport: str = ""
    arr_date: str = ""
    arr_time: str = ""
    dep_from: str = ""
    ret_date: str = ""
    ret_time: str = ""
    ret_to: str = ""
    fli_budget: float = ""
    hot_budget: float = ""
    interest: str = ""

# Create a flow class
class SoloTravelPlannerFlow(Flow[SoloTravelPlannerState]):

    @start()
    def initialize_inputs(self) -> None:
        self.itinerary_params = {
            "interest": self.state.interest,
            "depart_from": self.state.dep_from,
            "arrival_date": self.state.arr_date,
            "arrival_time": self.state.arr_time,
            "return_to": self.state.ret_to,
            "return_date": self.state.ret_date,
            "return_time": self.state.ret_time,
            "hotel_budget": self.state.hot_budget,
            "flight_budget": self.state.fli_budget
        }
        self.html_travel_handbook_params = {
            "passport": self.state.passport,
            "interest": self.state.interest,
            "itinerary": ""         # be filled later
        }

    @listen(initialize_inputs)
    def get_itinerary(self) -> None:
        self.full_itinerary = ItineraryCrew().crew().kickoff(
            inputs=self.itinerary_params).raw

    @listen(get_itinerary)
    def generate_handbook(self):
        # generate a handbook including every information for this trip
        self.html_travel_handbook_params["itinerary"] = self.full_itinerary
        
        self.html_travel_handbook = TravelHandbookCrew().crew().kickoff(
            inputs=self.html_travel_handbook_params).raw

        return self.html_travel_handbook
