"""Load and validate environment-driven settings for the Invoice Analysis Agent."""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    """Azure OpenAI + Document Intelligence configuration."""

    azure_openai_api_key: str
    azure_openai_endpoint: str
    azure_openai_deployment: str
    azure_openai_api_version: str
    document_intelligence_endpoint: str
    document_intelligence_key: str


def load_settings() -> Settings:
    load_dotenv(override=True)

    azure_openai_api_key = os.getenv("AZURE_OPENAI_API_KEY", "").strip()
    azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "").strip()
    azure_openai_deployment = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME", "").strip()
    azure_openai_api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-08-01-preview").strip()

    document_intelligence_endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT", "").strip()
    document_intelligence_key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY", "").strip()

    missing = [
        name
        for name, value in [
            ("AZURE_OPENAI_API_KEY", azure_openai_api_key),
            ("AZURE_OPENAI_ENDPOINT", azure_openai_endpoint),
            ("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME", azure_openai_deployment),
            ("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT", document_intelligence_endpoint),
            ("AZURE_DOCUMENT_INTELLIGENCE_KEY", document_intelligence_key),
        ]
        if not value
    ]
    if missing:
        raise RuntimeError(
            "Missing required environment variables: "
            + ", ".join(missing)
            + ". Copy .env.example to .env and fill in your Azure values."
        )

    return Settings(
        azure_openai_api_key=azure_openai_api_key,
        azure_openai_endpoint=azure_openai_endpoint.rstrip("/"),
        azure_openai_deployment=azure_openai_deployment,
        azure_openai_api_version=azure_openai_api_version,
        document_intelligence_endpoint=document_intelligence_endpoint.rstrip("/"),
        document_intelligence_key=document_intelligence_key,
    )
