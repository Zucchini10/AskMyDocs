import streamlit as st
import chromadb
import anthropic
from sentence_transformers import SentenceTransformer

# ── Setup ──────────────────────────────────────────────────────────────────────
client = anthropic.Anthropic(api_key="YOUR_API_KEY_HERE")
embedder = SentenceTransformer("all-MiniLM-L6-v2")
chroma = chromadb.Client()
collection = chroma.get_or_create_collection("docs")

# ── Sample documents (swap these out for your own!) ────────────────────────────
DOCS = [
    "Python is a high-level programming language known for its simple syntax.",
    "Machine learning is a subset of AI where models learn from data.",
    "RAG stands for Retrieval Augmented Generation. It combines search with LLMs.",
    "ChromaDB is a vector database used to store and search embeddings.",
    "Streamlit is a Python library for building simple web apps quickly.",
    "Anthropic makes Claude, an AI assistant focused on safety and helpfulness.",
    "Embeddings are numerical representations of text that capture meaning.",
    "A vector database stores embeddings and lets you search by similarity.",
]

# Load docs into ChromaDB (only once)
if collection.count() == 0:
    embeddings = embedder.encode(DOCS).tolist()
    collection.add(
        documents=DOCS,
        embeddings=embeddings,
        ids=[f"doc_{i}" for i in range(len(DOCS))]
    )

# ── RAG function ───────────────────────────────────────────────────────────────
def ask(question):
    # 1. Embed the question
    q_embedding = embedder.encode(question).tolist()

    # 2. Find the 3 most relevant chunks
    results = collection.query(query_embeddings=[q_embedding], n_results=3)
    context = "\n".join(results["documents"][0])

    # 3. Send to Claude with context
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=500,
        messages=[{
            "role": "user",
            "content": f"""Answer the question using only the context below.
If the answer isn't in the context, say "I don't know based on the provided documents."

Context:
{context}

Question: {question}"""
        }]
    )
    return response.content[0].text, context

# ── Streamlit UI ───────────────────────────────────────────────────────────────
st.title("📚 My RAG Chatbot")
st.caption("Ask questions about the loaded documents")

if "messages" in st.session_state == False:
    st.session_state.messages = []

for msg in st.session_state.get("messages", []):
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if question := st.chat_input("Ask something..."):
    st.session_state.setdefault("messages", [])
    st.session_state.messages.append({"role": "user", "content": question})

    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer, context = ask(question)
        st.write(answer)
        with st.expander("📄 Sources used"):
            st.write(context)

    st.session_state.messages.append({"role": "assistant", "content": answer})