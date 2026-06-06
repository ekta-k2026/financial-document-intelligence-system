import streamlit as st
from dotenv import load_dotenv
import os

import numpy as np
import faiss
import pandas as pd

from pypdf import PdfReader
from io import BytesIO

from openai import OpenAI
from utils.file_processor import process_uploaded_file
from utils.embeddings import build_index
from utils.retrieval import retrieve_relevant_chunks
from fintech.financial_analysis import generate_financial_summary
from fintech.dashboard import render_dashboard
from fintech.report_generator import generate_financial_report



# -------------------- LOAD ENV --------------------
load_dotenv()

# -------------------- OPENAI CLIENT --------------------
api_key = st.secrets["OPENAI_API_KEY"]

client = OpenAI(
    api_key=api_key
)

# -------------------- SESSION --------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    
uploaded_df = None
uploaded_kpis = {}



# -------------------- UI --------------------
st.title("Financial Document Intelligence System 💰")
st.divider()

if st.button("🧹 Clear Chat"):
    st.session_state.chat_history = []
    st.rerun()

uploaded_files = st.file_uploader(
    "Upload files (TXT, PDF, Excel)",
    type=["txt", "pdf", "xlsx"],
    accept_multiple_files=True
)

if uploaded_files:
    st.success(f"{len(uploaded_files)} files uploaded")

    for f in uploaded_files:
        st.write("📄", f.name)

    st.info("Using uploaded files for answers")

else:
    st.info("Using default knowledge base")

# -------------------- SHOW CHAT --------------------
for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.write(chat["content"])

# -------------------- DEFAULT DATA --------------------
@st.cache_resource
def load_data():

    documents = []

    # Prevent crash if Data folder missing
    if not os.path.exists("Data"):
        return [], None

    for filename in os.listdir("Data"):

        filepath = f"Data/{filename}"

        with open(filepath, "r", encoding="utf-8") as file:

            content = file.read()

            sentences = content.split(".")

            for i in range(0, len(sentences), 2):

                chunk = ".".join(
                    sentences[i:i+2]
                )

                if chunk.strip():

                    documents.append(
                        f"[{filename}] {chunk}"
                    )

    return build_index(documents, client)

# -------------------- LOAD DATA --------------------
if uploaded_files:

    all_documents = []

    uploaded_df = None
    uploaded_kpis = {}

    for file in uploaded_files:

        docs, full_text, df, kpis = process_uploaded_file(
            file.getvalue(),
            file.name
        )

        if docs:

            all_documents.extend(docs)

            if df is not None:
                uploaded_df = df

            if kpis:
                uploaded_kpis = kpis

    if not all_documents:

        st.error(
            "Uploaded files contain no readable content."
        )

        st.stop()

    documents, index = build_index(
        all_documents,
        client
    )

else:

    documents, index = load_data()



# -------------------- DEBUG --------------------
if uploaded_files:

    st.success(
        f"📄 Using {len(uploaded_files)} uploaded files"
    )

    st.write(
        f"Total chunks created: {len(documents)}"
    )

else:

    st.write(
        f"📚 Using default data | Total chunks: {len(documents)}"
    )

if not documents or index is None:

    st.warning("No documents available.")

    st.stop()

# -------------------- CHAT INPUT --------------------
question = st.chat_input("Ask something...")

if question:

    # Show user question
    with st.chat_message("user"):
        st.write(question)

    history = st.session_state.chat_history

    # -------------------- CONTEXT --------------------
    context_question = question

    if len(history) >= 4:

        context_question = (
            history[-4]["content"]
            + " "
            + history[-2]["content"]
            + " "
            + question
        )

    elif len(history) >= 2:

        context_question = (
            history[-2]["content"]
            + " "
            + question
        )

    # -------------------- RETRIEVAL --------------------
    if any(
        word in question.lower()
        for word in [
            "all",
            "list",
            "everything",
            "show all",
            "extract",
            "transactions",
            "amounts",
            "full"

        ]
    ):

        selected_knowledge = " ".join(documents)

    else:

        selected_knowledge = retrieve_relevant_chunks(
            context_question,
            documents,
            index,
            client
        )

    # Fallback
    if selected_knowledge.strip() == "":
        selected_knowledge = documents[0]
    # -------------------- FINANCIAL AI ANALYSIS --------------------
    with st.spinner("Analyzing financial documents..."):

        answer = generate_financial_summary(
            question,
            selected_knowledge,
            client
        )
    # -------------------- SHOW ANSWER --------------------
    with st.chat_message("assistant"):

        st.write(answer)

        with st.expander("📄 Sources used"):

            sources = set()

            for doc in selected_knowledge.split("["):

                if "]" in doc:

                    source = "[" + doc.split("]")[0] + "]"

                    sources.add(source)

            st.write("\n".join(sources))

    # -------------------- SAVE CHAT --------------------
    st.session_state.chat_history.append(
        {
            "role": "user",
            "content": question
        }
    )

    st.session_state.chat_history.append(
        {
            "role": "assistant",
            "content": answer
        }
    )
# -------------------- DOWNLOAD FINANCIAL REPORT --------------------

if uploaded_kpis:

    financial_report = generate_financial_report(
        uploaded_kpis
    )

    st.download_button(
        label="📥 Download Financial Report",
        data=financial_report,
        file_name="financial_report.txt",
        mime="text/plain"
    )

# -------------------- DOWNLOAD CHAT --------------------
chat_text = ""

for chat in st.session_state.chat_history:

    chat_text += (
        f"{chat['role'].upper()}: "
        f"{chat['content']}\n\n"
    )

st.download_button(
    "⬇️ Download Chat",
    chat_text,
    file_name="chat.txt"
)

# -------------------- DASHBOARD --------------------
if uploaded_files:

    if uploaded_df is not None and uploaded_kpis:

        render_dashboard(
            uploaded_df,
            uploaded_kpis
        )



# -------------------- SIDEBAR --------------------
with st.sidebar:

    st.header("⚙️ Controls")

    st.write(
        f"Documents loaded: {len(documents)}"
    )