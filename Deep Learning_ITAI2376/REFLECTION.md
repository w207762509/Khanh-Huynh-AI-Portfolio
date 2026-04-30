<<<<<<< HEAD
# Reflection — Invoice Analysis Agent

## What worked well

- Separating the pipeline into **OCR (Azure Document Intelligence)**, **reasoning (Azure OpenAI)**, and **tools** meant that the system was easy to understand and score because the LLM had to provide reasoning by way of tool invocations rather than making random guesses.
- Utilizing **LangGraph’s `create_react_agent`** provided an elegant **ReAct** cycle without needing too much orchestration.
- Including a **tiny markdown-based knowledge base** and **BM25 retrieval** maintained RAG as a lightweight process (no GPU embeddings), but illustrated retrieval-augmented grounding nonetheless.

## What did not work (initially) and how it was handled

- **Versioning issues** arose whenever highly restrictive pins caused dependency problems between `langchain-*` and `langgraph-*`. It was remedied by aligning versions through the use of resolver-friendly pins and storing the resolved pins in `requirements.txt`.
- **PDF files for invoices** could not be easily shipped within the repo because of their large size and licensing concerns; instead, the repo explains how to create sample invoices stored within `data/sample_invoices/`.

## Biggest technical challenge

The main difficulty was making the **Document Intelligence JSON** compatible with both the LLM and a **validation deterministic function** without requiring inflexible parsing for any type of invoice format. To achieve this, we serialized the values of model fields to standard JSON-compatible values while maintaining validation criteria as simple as possible (only PASS/FAIL results).

## Single vs multi-agent

The project remained on **Option A (single agent)**. The process flow is largely sequential (OCR -> validation -> summarization), and dividing it into multiple agents does not seem to offer any advantages.

## What I would build next (another semester)

- A mini **Streamlit/Gradio interface** for uploads, dual PDF display, and manual editing of extracted data.    
- **Durable memory** (SQLite checkpointing) along with optional **duplicates filtering** using the processed invoice database.  
- Enhanced validation: tax jurisdiction logic, purchase order correlation, and intelligent forwarding to manual verification teams based on confidence.
=======
# Reflection — Invoice Analysis Agent

## What worked well

- Splitting the system into **OCR (Azure Document Intelligence)**, **reasoning (Azure OpenAI)**, and **tools** made the behavior easy to explain and grade: the LLM has to show its work through tool calls instead of guessing numbers.
- Using **LangGraph’s `create_react_agent`** gave a clean **ReAct** loop without a lot of custom orchestration code.
- Adding a **small markdown knowledge base** plus **BM25 retrieval** kept RAG lightweight (no GPU embeddings) while still demonstrating retrieval-augmented grounding.

## What did not work (initially) and how it was handled

- **Dependency conflicts** showed up when overly strict pins mixed incompatible `langchain-*` and `langgraph-*` versions. The fix was to align versions using a resolver-friendly set and record the resolved pins in `requirements.txt`.
- **Invoice PDFs** are hard to ship in a classroom repo due to size/licensing, so the repo documents how to place samples under `data/sample_invoices/` instead of committing unknown vendor PDFs.

## Biggest technical challenge

The biggest challenge was making the **Document Intelligence JSON** usable for both the LLM and a **deterministic validation tool** without forcing brittle parsing across every possible invoice layout. The approach was to serialize model fields into plain JSON-friendly primitives and keep validation rules conservative (explicit PASS/FAIL with “not enough fields” outcomes).

## Single vs multi-agent

The project stayed on **Option A (single agent)**. The workflow is mostly linear (OCR → validate → summarize), and splitting into multiple agents would add coordination complexity without a clear benefit for the scope.

## What I would build next (another semester)

- A small **Streamlit/Gradio UI** for uploads, side-by-side PDF view, and editable extracted fields.  
- **Persistent memory** (SQLite checkpointer) plus optional **duplicate detection** against a processed-invoice table.  
- Stronger validation: tax jurisdiction rules, purchase-order matching, and confidence-based routing to human review queues.
>>>>>>> 9c0675f (Update project)
