import os
import requests

from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

class AzureBingSearchInput(BaseModel):
    """Input schema for AzureBingSearchTool."""
    query: str = Field(..., description="Query to search the internet.")

class AzureBingSearchTool(BaseTool):
    name: str = "Azure Bing Search tool"
    description: str = (
        "Useful to search the internet about a given topic and return relevant results."
    )
    args_schema: Type[BaseModel] = AzureBingSearchInput

    def _run(self, query: str) -> str:
        top_result_to_return = 5
        subscription_key = os.getenv("AZURE_BING_SEARCH_API_KEY")
        search_url = "https://api.bing.microsoft.com/v7.0/search"

        headers = {"Ocp-Apim-Subscription-Key": subscription_key}
        params = {"q": query, "count": top_result_to_return, "textDecorations": True, "textFormat": "HTML"}
        response = requests.get(search_url, headers=headers, params=params)
        response.raise_for_status()
        search_results = response.json()

        # check if there is an organic key
        if 'webPages' not in search_results:
            return "Sorry, I couldn't find anything about that, there could be an error with your subscription key."
        else:
            results = search_results.get("webPages", {"value": []}).get("value", [])
            string = []
            for result in results[:top_result_to_return]:
                try:
                    string.append('\n'.join([
                        f"Title: {result['name']}", f"Link: {result['url']}",
                        f"Snippet: {result['snippet']}", "\n-----------------"
                    ]))
                except KeyError:
                    next

            return '\n'.join(string)
        