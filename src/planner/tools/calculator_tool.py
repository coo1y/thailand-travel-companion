from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field


class CalculatorToolInput(BaseModel):
    """Input schema for CalculatorTool."""
    operation: str = Field(..., description="Mathematical Operation.")

class CalculatorTool(BaseTool):
    name: str = "Calculator tool"
    description: str = (
        """Useful to perform any mathematical calculations, 
        like sum, minus, multiplication, division, etc.
        The input to this tool should be a mathematical 
        expression, a couple examples are `200*7` or `5000/2*10`
        """
    )
    args_schema: Type[BaseModel] = CalculatorToolInput

    def _run(self, operation: str) -> str:
        try:
            return eval(operation)
        except SyntaxError:
            return "Error: Invalid syntax in mathematical expression"
