from langchain_core.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from core.plugin import SMEPlugin

class SMEQueryInput(BaseModel):
    query: str = Field(description="The finance question to ask the expert")

class SMEPluginTool(BaseTool):
    name: str = "finance_expert_plugin"
    description: str = "Use this tool to ask complex financial questions. It provides structural reasoning and cites sources from the knowledge base."
    args_schema: Type[BaseModel] = SMEQueryInput
    plugin: SMEPlugin

    def _run(self, query: str) -> str:
        return self.plugin.process_query(query)
