# AskMyDocs 📚

An AI-powered document Q&A chatbot built with Retrieval-Augmented Generation (RAG). Ask questions about your documents and get accurate, context-grounded answers — powered by Claude AI.

---

## Features

- **Document-grounded answers** – Claude only responds based on your loaded documents, never hallucinating outside of them
- **Semantic search** – Uses SentenceTransformers to find the most relevant document chunks for each query
- **Source transparency** – Every answer shows the exact document passages used to generate it
- **Conversation history** – Maintains chat history within a session
- **Simple web UI** – Clean Streamlit interface, no frontend experience needed

---

## How It Works

1. Documents are embedded using `all-MiniLM-L6-v2` from SentenceTransformers
2. Embeddings are stored in **ChromaDB**, a local vector database
3. When you ask a question, the top 3 most semantically similar chunks are retrieved
4. The question + retrieved context are sent to **Claude** (claude-haiku-4-5)
5. Claude answers strictly based on the provided context

---

## Installation

```bash
git clone https://github.com/YOUR_USERNAME/askmydocs.git
cd askmydocs
pip install -r requirements.txt
```

---

## Setup

Add your Anthropic API key to `app.py`:

```python
client = anthropic.Anthropic(api_key="YOUR_API_KEY_HERE")
```

Get your API key at [console.anthropic.com](https://console.anthropic.com).

---

## Usage

```bash
streamlit run app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

To load your own documents, replace the `DOCS` list in `app.py` with your own text chunks:

```python
DOCS = [
    "Your first document chunk here.",
    "Your second document chunk here.",
    ...
]
```

---

## File Structure

```
├── app.py            # Main application logic and Streamlit UI
└── README.md         # This file
```

---

## Requirements

```
streamlit
chromadb
anthropic
sentence-transformers
```

---

## Tech Stack

- **[Streamlit](https://streamlit.io)** – Web UI
- **[ChromaDB](https://www.trychroma.com)** – Vector database
- **[SentenceTransformers](https://www.sbert.net)** – Text embeddings
- **[Anthropic Claude API](https://www.anthropic.com)** – LLM for answer generation

---

## License

MIT
