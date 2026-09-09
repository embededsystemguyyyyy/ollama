# Building Local AI with Ollama — Companion Code

Companion code for *Building Local AI with Ollama: Build Local LLM Applications, RAG Systems, AI Agents, Tool-Using Assistants, and Multimodal Workflows*.

📖 **Get the book on Amazon:** https://www.amazon.com/dp/B0HHXW3QCV

Each chapter folder contains the runnable, build-along scripts from that chapter. Files are copy-paste-ready and self-contained; where a later chapter extends an earlier file, that's called out in comments at the top of the file.

## Requirements

- Python 3.10+
- [Ollama](https://ollama.com) installed and running locally
- `pip install -r requirements.txt`

## Chapters

| # | Chapter | Files |
|---|---|---|
| 1 | Getting Started with Ollama and Local AI | `hello_ollama.py`, `hello_ollama_stream.py` |
| 2 | Choosing and Running Local Models | `model_benchmark.py`, `memory_check.py` |
| 3 | Building Applications with the Ollama API | `ollama_client.py`, `local_assistant.py`, `raw_http_example.py`, `retry_wrapper.py`, `test_structured.py` |
| 4 | Prompt Engineering for Local LLMs | `prompt_templates.py`, `test_classification.py`, `test_extraction.py`, `test_temperature.py`, `test_reasoning_style.py` |
| 5 | Local RAG with Ollama | `ingest.py`, `chunking.py`, `vector_store.py`, `pdf_assistant.py` |
| 6 | Embeddings and Vector Databases | `chroma_store.py`, `build_knowledge_base.py`, `search_cli.py`, `inspect_collection.py`, `hybrid_search.py` |
| 7 | Tool Calling and AI-Powered Actions | `tools.py`, `tool_assistant.py`, `sensitive_tools.py` |
| 8 | Building AI Agents with Ollama | `search_tool.py`, `agent_notes.py`, `research_agent.py` |
| 9 | Advanced Local AI Agents | `agent_memory.py`, `pipeline_state.py`, `specialists.py`, `coordinator.py`, `recall_demo.py` |
| 10 | Multimodal AI with Ollama | `vision_tools.py`, `test_vision.py`, `document_extraction.py`, `image_knowledge_base.py`, `multimodal_assistant.py` |
| 11 | Local AI for Coding and Data Analysis | `code_generation.py`, `code_explain.py`, `code_debug.py`, `test_generation.py`, `repo_context.py`, `coding_assistant.py` |
| 12 | Connecting Ollama to Databases and Applications | `setup_sample_db.py`, `schema_discovery.py`, `sql_generation.py`, `sql_validation.py`, `sql_assistant.py` |
| 13 | Building Reliable and Production-Ready Local AI | `structured_logging.py`, `concurrency_guard.py`, `model_warmer.py`, `production_service.py`, `load_test.py` |
| 14 | Capstone: Building a Complete Local AI Platform | `workspace_router.py`, `workspace_capabilities.py`, `workspace.py`, `test_routing.py` |

## Usage

Pull the models used in the book before running examples:

```
ollama pull llama3.2:3b
ollama pull nomic-embed-text
ollama pull llava
ollama pull qwen2.5-coder:7b
```

Then run any script directly, e.g.:

```
python chapter-01-getting-started-with-ollama-and-local-ai/hello_ollama.py
```

Later chapters import from earlier ones (e.g. `ollama_client.py` from Chapter 3 is reused throughout) — copy shared modules into the working chapter folder, or add the earlier chapter's directory to your `PYTHONPATH`.
