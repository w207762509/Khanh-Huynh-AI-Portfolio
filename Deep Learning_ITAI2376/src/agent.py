"""LangGraph ReAct agent: Azure OpenAI reasoning + tools + conversational memory."""

from __future__ import annotations

from langchain_openai import AzureChatOpenAI
from langgraph.prebuilt import create_react_agent

from src.config import Settings
from src.memory import build_checkpointer, build_policy_retriever
from src.tools import build_invoice_tools


AGENT_SYSTEM_PROMPT = """You are the Invoice Analysis Agent for accounts payable workflows.

Reasoning pattern: ReAct (reason about the goal, act with tools, observe results, repeat).

Workflow:
1) If the user provides an invoice file path, call extract_invoice_fields with that path.
2) Call validate_invoice_totals using the exact JSON string returned by extract_invoice_fields.
3) Call search_invoice_policies with focused queries when policy context would improve validation
   or reporting (tolerances, required fields, fraud checks).
4) Produce a concise final report with sections: Summary, Key Fields, Line Items (if present),
   Validation, Policy Notes (only if retrieved), Risks/Anomalies, Recommended Next Actions.

Rules:
- Never invent numeric fields; only use tool outputs for numbers.
- If OCR fields are missing or low-confidence, say so explicitly.
- Keep the final answer readable for a finance manager (plain English, short bullets).
"""


def build_invoice_agent(settings: Settings):
    llm = AzureChatOpenAI(
        azure_endpoint=settings.azure_openai_endpoint,
        azure_deployment=settings.azure_openai_deployment,
        api_version=settings.azure_openai_api_version,
        api_key=settings.azure_openai_api_key,
        temperature=0.2,
    )

    retriever = build_policy_retriever()
    tools = build_invoice_tools(settings, retriever)
    checkpointer = build_checkpointer()

    return create_react_agent(
        llm,
        tools,
        prompt=AGENT_SYSTEM_PROMPT,
        checkpointer=checkpointer,
    )
