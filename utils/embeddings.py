import numpy as np
import faiss
import streamlit as st


@st.cache_resource(show_spinner=False)
def build_index(documents, _client):

    if not documents:
        return [], None

    documents = documents[:1000]

    doc_embeddings = []

    BATCH_SIZE = 100

    for i in range(0, len(documents), BATCH_SIZE):

        batch = documents[i:i + BATCH_SIZE]

        response = _client.embeddings.create(
            model="text-embedding-3-small",
            input=batch
        )

        batch_embeddings = [
            item.embedding for item in response.data
        ]

        doc_embeddings.extend(batch_embeddings)

    embeddings_array = np.array(
        doc_embeddings,
        dtype="float32"
    )

    index = faiss.IndexFlatL2(
        embeddings_array.shape[1]
    )

    index.add(embeddings_array)

    return documents, index