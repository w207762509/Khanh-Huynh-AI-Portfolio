"""LangChain tools: Document Intelligence extraction, totals validation, policy RAG."""

from __future__ import annotations

import json
import re
from decimal import Decimal, InvalidOperation
from typing import Any

from langchain_core.tools import tool

from src.config import Settings
from src.di_client import analyze_invoice_file_json


def build_invoice_tools(settings: Settings, retriever):
    """Bind settings and retriever so tools run with configured credentials."""

    @tool
    def extract_invoice_fields(file_path: str) -> str:
        """Run Azure AI Document Intelligence (prebuilt-invoice) OCR on a PDF or image.

        Args:
            file_path: Absolute or relative path to an invoice PDF/PNG/JPG/TIFF.

        Returns:
            JSON string with extracted fields (vendor, dates, totals, line items, confidence).
        """
        return analyze_invoice_file_json(
            endpoint=settings.document_intelligence_endpoint,
            key=settings.document_intelligence_key,
            file_path=file_path,
        )

    @tool
    def validate_invoice_totals(extracted_invoice_json: str) -> str:
        """Rules engine: compare line-item math to stated subtotal/total/tax.

        Args:
            extracted_invoice_json: JSON from extract_invoice_fields (full payload).

        Returns:
            Human-readable validation summary with pass/fail and numeric deltas.
        """
        try:
            payload = json.loads(extracted_invoice_json)
        except json.JSONDecodeError as exc:
            return f"Invalid JSON for validation: {exc}"

        documents = payload.get("documents") or []
        if not documents:
            return "No documents found in extraction payload; nothing to validate."

        doc0 = documents[0]
        fields = doc0.get("fields") or {}

        def _to_decimal(value: Any) -> Decimal | None:
            if value is None:
                return None
            if isinstance(value, dict) and "amount" in value:
                value = value.get("amount")
            try:
                return Decimal(str(value))
            except (InvalidOperation, TypeError, ValueError):
                return None

        items = fields.get("Items") or []
        line_sum = Decimal("0")
        counted_lines = 0
        for item in items:
            if not isinstance(item, dict):
                continue
            amt = _to_decimal(item.get("Amount"))
            if amt is not None:
                line_sum += amt
                counted_lines += 1

        subtotal = _to_decimal(fields.get("SubTotal"))
        total_tax = _to_decimal(fields.get("TotalTax"))
        invoice_total = _to_decimal(fields.get("InvoiceTotal"))

        parts = []
        parts.append(f"Counted {counted_lines} line items with a summed Amount of {line_sum}.")

        checks: list[tuple[str, bool, str]] = []

        expected_with_tax = None
        if subtotal is not None and total_tax is not None:
            expected_with_tax = subtotal + total_tax
            ok = invoice_total is not None and abs(expected_with_tax - invoice_total) <= Decimal("0.02")
            checks.append(
                (
                    "subtotal_plus_tax_vs_invoice_total",
                    ok,
                    f"SubTotal {subtotal} + TotalTax {total_tax} = {expected_with_tax}; InvoiceTotal {invoice_total}",
                )
            )

        if subtotal is not None and counted_lines > 0:
            ok = abs(line_sum - subtotal) <= Decimal("0.02")
            checks.append(
                (
                    "line_sum_vs_subtotal",
                    ok,
                    f"Line sum {line_sum} vs SubTotal {subtotal}",
                )
            )

        if invoice_total is not None and subtotal is not None and total_tax is None:
            ok = abs(line_sum - invoice_total) <= Decimal("0.02")
            checks.append(
                (
                    "line_sum_vs_invoice_total_no_tax_field",
                    ok,
                    f"Line sum {line_sum} vs InvoiceTotal {invoice_total} (no TotalTax field)",
                )
            )

        for name, ok, detail in checks:
            parts.append(f"- {name}: {'PASS' if ok else 'FAIL'} — {detail}")

        if not checks:
            parts.append("Not enough numeric fields to run validation (need totals and/or lines).")

        return "\n".join(parts)

    @tool
    def search_invoice_policies(query: str) -> str:
        """Retrieve accounting/AP policy snippets (RAG) relevant to validation and reporting.

        Args:
            query: What to look up (e.g., 'tax tolerance', 'three-way match', 'PII on invoices').

        Returns:
            Concatenated excerpts from the local knowledge base.
        """
        q = (query or "").strip()
        if not q:
            return "Provide a non-empty query."

        docs = retriever.invoke(q)
        if not docs:
            return "No matching policy excerpts found."
        excerpts = []
        for doc in docs:
            meta = doc.metadata or {}
            src = meta.get("source", "unknown")
            excerpts.append(f"Source: {src}\n{doc.page_content.strip()}")
        return "\n\n---\n\n".join(excerpts)

    return [extract_invoice_fields, validate_invoice_totals, search_invoice_policies]
