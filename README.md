# RAG — Retrieval-Augmented Generation Example

## Overview

This repository is a small Retrieval-Augmented Generation (RAG) example that:
- loads documents from `data_source/` (PDF/CSV/Excel/Other),
- splits them into chunks,
- inserts them into a LanceDB table with automatic vectorization using a `sentence-transformers` model,
- runs a simple interactive query loop that searches the DB for relevant chunks and calls Google Gemini (via the `google-genai` client) to generate answers using only the retrieved context.

Files of interest:
- `rag.py` — main script (interactive chat loop)
- `requirements.txt` — Python dependencies
- `data_source/` — place your documents here (a `sample.pdf` is included)

## Requirements

- Python 3.8+ (use a virtualenv)
- See `requirements.txt` for package list:

```
dotenv
google-genai
lancedb
sentence-transformers
langchain-text-splitters
llama-index
```

Install with:

```bash
python -m pip install -r requirements.txt
```

## Configuration

1. Create a `.env` file at the repo root with your Google Gemini / GenAI credentials. The project calls `load_dotenv()` and uses `google.genai.Client()` — set the environment variables expected by the `google-genai` library (for example a `GEMINI_API_KEY` or credentials described in the `google-genai` docs).

Example `.env` (adjust according to provider docs):

```
GEMINI_API_KEY=your_api_key_here
```

2. Place documents you want indexed under `data_source/` (PDF/CSV/Excel/Other). A `sample.pdf` is included as an example.

## How it works (brief)

- The script connects to a local LanceDB at `./embeddings` and creates a table `rag_test` with a schema that stores text and vectors.
- It uses a sentence-transformers model (from the registry in `lancedb.embeddings`) to compute vectors automatically when inserting documents.
- Documents under `data_source/` are read via `SimpleDirectoryReader` and split into chunks using `RecursiveCharacterTextSplitter` (chunk_size=100, overlap=10).
- Chunks are inserted into the LanceDB table. The script then starts an interactive loop:
  - User enters a query.
  - The script searches the LanceDB table for the most relevant chunks.
  - It calls the Gemini model (`gemini-2.5-flash` in the script) with a system instruction to only answer from the provided context and prints the result.

## Usage

1. Install deps and add your API key to `.env` as described above.
2. Add documents to `data_source/`.
3. Run the script:

```bash
python rag.py
```

4. In the interactive prompt type a question and press Enter. Type `stop` or `exit` to quit.

## Important notes & troubleshooting

- The script uses automatic vectorization provided by `lancedb` and the `sentence-transformers` registry. Ensure `sentence-transformers` is installed and compatible with your environment.
- The exact environment variable name and auth mechanism for `google.genai` may vary; consult the `google-genai` package documentation if authentication fails.
- LanceDB stores embeddings in `./embeddings` — you can inspect or reuse that directory.

## Extending

- Replace the `gemini-2.5-flash` model name in `rag.py` with another model if desired.
- Add more robust prompt engineering or a structured prompt template to improve answer quality.

## Files

- `rag.py` — main script
- `requirements.txt` — dependencies
- `data_source/` — input documents

---

If you'd like, I can:
- run the script locally (if you want to provide API credentials),
- add a `README` example `.env.example`, or
- add a small CLI wrapper to process documents non-interactively.
