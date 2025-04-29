## Ref: https://github.com/crewAIInc/crewAI/blob/main/src/crewai/tools/agent_tools/add_image_tool.py

import json
import os

import requests
from crewai import Agent, Task, Crew
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from unstructured.partition.html import partition_html
from dotenv import load_dotenv

load_dotenv()

class BrowserToolInput(BaseModel):
    """Input schema for BrowserTool."""
    website: str = Field(..., description="A website of content wanted to scrape and summarize.")

class BrowserTool(BaseTool):
    name: str = "Browser tool"
    description: str = (
        "Useful to scrape and summarize a website content"
    )
    args_schema: Type[BaseModel] = BrowserToolInput

    def _run(self, website: str) -> str:
        token = os.environ['BROWSERLESS_API_KEY']
        url = f"https://chrome.browserless.io/content?token={token}"
        payload = json.dumps({"url": website})
        headers = {'cache-control': 'no-cache', 'content-type': 'application/json'}
        response = requests.request("POST", url, headers=headers, data=payload)
        elements = partition_html(text=response.text)
        content = "\n\n".join([str(el) for el in elements])
        content = [content[i:i + 8000] for i in range(0, len(content), 8000)]
        summaries = []
        for chunk in content:
            agent = Agent(
                role='Principal Researcher',
                goal='Do amazing researches and summaries based on the content you are working with',
                backstory="You're a Principal Researcher at a big company and you need to do a research about a given topic.",
                allow_delegation=False)
            task = Task(
                agent=agent,
                description=f'Analyze and summarize the content below, make sure to include the most relevant information in the summary.\n\nCONTENT\n----------\n{chunk}',
                expected_output="The full summary of the content with the most relevant information."
            )
            crew = Crew(
                agents=[agent],
                tasks=[task],
                verbose=False
            )
            result = crew.kickoff()
            summary = task.output.raw
            summaries.append(summary)
        
        return "\n\n".join(summaries)
