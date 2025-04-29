import json
import os
from serpapi import GoogleSearch
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from dotenv import load_dotenv
load_dotenv()

class GoogleHotelSearchInput(BaseModel):
    query: str = Field(..., description="Location or hotel name to search for")
    check_in_date: str = Field(..., description="Check‑in date (YYYY‑MM‑DD)")
    check_out_date: str = Field(..., description="Check‑out date (YYYY‑MM‑DD)")
    max_price: int = Field(0, ge=0, description="Maximum price (USD) of hotel per night")

class GoogleHotelSearchTool(BaseTool):
    """
    Query SerpAPI’s Google Hotels API to retrieve hotel options
    for a given query, dates, and a maximum price per night.
    """

    name: str = "google_hotel_search"
    description: str = "Use this tool to look up hotels via SerpAPI Google Hotels."
    args_schema: Type[BaseModel] = GoogleHotelSearchInput

    def _run(self, query: str, check_in_date: str, check_out_date: str, max_price: int) -> str:
        api_key = os.getenv("SERP_API_KEY")
        if not api_key:
            raise RuntimeError("SERP_API_KEY not set in environment")
        
        params = {
            "engine": "google_hotels",
            "q": query,
            "check_in_date": check_in_date,
            "check_out_date": check_out_date,
            "adults": "1",
            "currency": "USD",
            "rating": "8",
            "max_price": max_price,
            "hotel_class": "3,4,5",
            "gl": "us",
            "hl": "en",
            "no_cache": False,                  # cache
            "api_key": api_key
        }

        search = GoogleSearch(params)
        hotel_result = search.get_dict()
        hotel_result = hotel_result.get("properties", [])

        # save hotel
        with open(f"log/hotel_{check_in_date}_{check_out_date}.json", "w") as jf:
            json.dump(hotel_result, jf, indent=4)

        return "\n".join([str(h) for h in hotel_result[:3]]) # return top 3 results and will pick only 1 later
