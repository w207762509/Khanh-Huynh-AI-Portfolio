"""CLI entrypoint for the Invoice Analysis Agent (LangGraph ReAct + Azure)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from langchain_core.messages import HumanMessage

from src.agent import build_invoice_agent
from src.config import load_settings


def main() -> None:
    parser = argparse.ArgumentParser(description="Invoice Analysis Agent (LangGraph ReAct).")
    parser.add_argument("--invoice", required=True, help="Path to an invoice PDF or image file.")
    parser.add_argument(
        "--thread-id",
        default="default",
        help="Conversation thread id (LangGraph checkpointer / short-term memory).",
    )
    parser.add_argument(
        "--message",
        default="",
        help="Optional extra instructions appended to the analysis request.",
    )
    args = parser.parse_args()

    invoice_path = Path(args.invoice).expanduser().resolve()
    if not invoice_path.is_file():
        raise SystemExit(f"Invoice file not found: {invoice_path}")

    settings = load_settings()
    print("OPENAI ENDPOINT =", repr(settings.azure_openai_endpoint))
    print("OPENAI DEPLOYMENT =", repr(settings.azure_openai_deployment))
    print("OPENAI API VERSION =", repr(settings.azure_openai_api_version))
    graph = build_invoice_agent(settings)

    user_text = f"Analyze this invoice file: {invoice_path}"
    if args.message.strip():
        user_text = f"{user_text}\n\nAdditional instructions:\n{args.message.strip()}"

    result = graph.invoke(
        {"messages": [HumanMessage(content=user_text)]},
        config={"configurable": {"thread_id": args.thread_id}},
    )

    print(result["messages"][-1].content)


if __name__ == "__main__":
    main()
