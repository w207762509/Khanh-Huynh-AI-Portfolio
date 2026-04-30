"""Azure AI Document Intelligence helpers (OCR + prebuilt invoice schema)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult
from azure.core.credentials import AzureKeyCredential


def _field_to_primitive(field: Any) -> Any:
    if field is None:
        return None

    kind = getattr(field, "type", None)
    if kind == "string":
        return getattr(field, "value_string", None)
    if kind == "date":
        return getattr(field, "value_date", None)
    if kind in {"number", "integer"}:
        return getattr(field, "value_number", None) or getattr(field, "value_integer", None)
    if kind == "currency":
        cur = getattr(field, "value_currency", None)
        if cur is None:
            return None
        return {
            "amount": getattr(cur, "amount", None),
            "currency_code": getattr(cur, "currency_code", None),
        }
    if kind == "array":
        arr = getattr(field, "value_array", None) or []
        return [_field_to_primitive(item) for item in arr]
    if kind == "object":
        obj = getattr(field, "value_object", None) or {}
        return {k: _field_to_primitive(v) for k, v in obj.items()}
    if kind == "address":
        addr = getattr(field, "value_address", None)
        if addr is None:
            return None
        return getattr(addr, "content", None) or str(addr)
    if kind == "boolean":
        return getattr(field, "value_boolean", None)

    for attr in (
        "value_string",
        "value_date",
        "value_number",
        "value_integer",
        "value_boolean",
    ):
        val = getattr(field, attr, None)
        if val is not None:
            return val
    return str(field)


def analyze_invoice_file(
    *,
    endpoint: str,
    key: str,
    file_path: str,
) -> dict[str, Any]:
    path = Path(file_path).expanduser().resolve()
    if not path.is_file():
        raise FileNotFoundError(f"Invoice file not found: {path}")

    client = DocumentIntelligenceClient(endpoint, AzureKeyCredential(key))
    with path.open("rb") as handle:
        poller = client.begin_analyze_document("prebuilt-invoice", body=handle)
    result: AnalyzeResult = poller.result()

    documents: list[dict[str, Any]] = []
    for idx, doc in enumerate(result.documents or []):
        fields_out: dict[str, Any] = {}
        raw_fields = getattr(doc, "fields", None) or {}
        for name, field in raw_fields.items():
            fields_out[name] = _field_to_primitive(field)

        documents.append(
            {
                "index": idx,
                "doc_type": getattr(doc, "doc_type", None),
                "confidence": getattr(doc, "confidence", None),
                "fields": fields_out,
            }
        )

    return {
        "model_id": "prebuilt-invoice",
        "source_file": str(path),
        "page_count": len(result.pages or []),
        "documents": documents,
    }


def analyze_invoice_file_json(*, endpoint: str, key: str, file_path: str) -> str:
    payload = analyze_invoice_file(endpoint=endpoint, key=key, file_path=file_path)
    return json.dumps(payload, indent=2, default=str)
