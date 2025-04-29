import json
import os
from serpapi import GoogleSearch
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from dotenv import load_dotenv
load_dotenv()

class GoogleFlightSearchInput(BaseModel):
    departure_id: str = Field(..., description="IATA code of origin airport")
    arrival_id: str = Field(..., description="IATA code of destination airport")
    departure_date: str | None = Field(..., description="Departure date (YYYY-MM-DD), if null means flight arrive in Thailand")
    departure_time: str | None = Field(..., description="Departure time (00:00 - 05:59, 06:00 - 11:59, 12:00 - 17:59, 18:00 - 23:59), if null means flight arrive in Thailand")
    arrival_date: str | None = Field(..., description="Outbound date (YYYY-MM-DD), if null means flight depart from Thailand")
    arrival_time: str | None = Field(..., description="Outbound time (00:00 - 05:59, 06:00 - 11:59, 12:00 - 17:59, 18:00 - 23:59), if null means flight depart from Thailand")
    max_price: int = Field(0, ge=0, description="Price per flight (USD)")

class GoogleFlightsSearchTool(BaseTool):
    """
    Query Serper's Google Flights API to retrieve flight options for outbound and return segments.
    """
    name: str = "google_flights_search"
    description: str = (
        "Use Serper API's Google Flights engine to search for flights given departure_id, arrival_id, "
        "optional departure_date, optional departure_time, optional arrival_date, optional arrival_time, and max_price."
    )
    args_schema: Type[BaseModel] = GoogleFlightSearchInput

    def _run(self, departure_id: str, departure_date: str, departure_time: str, arrival_id: str, arrival_date: str, arrival_time: str, max_price: float) -> str:
        api_key = os.getenv("SERP_API_KEY")
        if not api_key:
            raise RuntimeError("SERP_API_KEY not set in environment")
        
        params = {
            "engine": "google_flights",
            "departure_id": departure_id,
            "arrival_id": arrival_id,
            "outbound_date": "",                # be filled later
            "outbound_times": "",               # be filled later
            "stops": "1",                       # non-stop
            "type": "2",                        # one-way
            "currency": "USD",
            "max_price": max_price,
            "hl": "en",
            "no_cache": False,                  # cache
            "api_key": api_key
        }

        time_mapper = {
            "00:00 - 05:59": "0,5", "06:00 - 11:59": "6,11",
            "12:00 - 17:59": "12,17", "18:00 - 23:59": "18,23"
        }
        if departure_date: # if depart from Thailand
            params["outbound_date"] = departure_date
            params["outbound_times"] = time_mapper.get(departure_time)
        else:   # if arrive in Thailand
            params["outbound_date"] = arrival_date
            params["outbound_times"] = f"0,23,{time_mapper.get(arrival_time)}"

        print(params)

        search = GoogleSearch(params)
        result = search.get_dict()

        flight_result = result.get("best_flights", []) # best_flights is not always returned
        flight_result += result.get("other_flights", [{"flights": []}])

        ## collect log
        with open(f"log/flight_{params.get("outbound_date")}.json", "w") as jf:
            json.dump(flight_result, jf, indent=4)

        return "\n".join([str(f) for f in flight_result[:3]]) # return top 3 results and will pick only 1 later
