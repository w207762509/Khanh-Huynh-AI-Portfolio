"""RAG retriever over local markdown policies + LangGraph checkpointer factory."""

from __future__ import annotations

from pathlib import Path

from langchain_community.retrievers import BM25Retriever
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.checkpoint.memory import MemorySaver


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def build_policy_retriever(knowledge_dir: Path | None = None, k: int = 4):
    """Load markdown files from data/knowledge and return a BM25 retriever (lexical RAG, no GPU)."""

    root = knowledge_dir or (_repo_root() / "data" / "knowledge")
    if not root.is_dir():
        raise FileNotFoundError(
            f"Knowledge directory not found: {root}. Add markdown files under data/knowledge/."
        )

    texts: list[str] = []
    sources: list[str] = []
    for path in sorted(root.glob("*.md")):
        texts.append(path.read_text(encoding="utf-8"))
        sources.append(str(path))

    if not texts:
        raise RuntimeError(f"No .md files found under {root}")

    splitter = RecursiveCharacterTextSplitter(chunk_size=900, chunk_overlap=120)
    documents: list[Document] = []
    for text, src in zip(texts, sources):
        for chunk in splitter.split_text(text):
            documents.append(Document(page_content=chunk, metadata={"source": src}))

    retriever = BM25Retriever.from_documents(documents)
    retriever.k = k
    return retriever


def build_checkpointer():
    """Short-term conversational memory for multi-turn sessions (ReAct + thread_id)."""
    return MemorySaver()
