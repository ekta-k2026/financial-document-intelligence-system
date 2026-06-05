import numpy as np


def retrieve_relevant_chunks(
    question,
    documents,
    index,
    client,
    k=10
):

    question_embedding = client.embeddings.create(
        model="text-embedding-3-small",
        input=question
    ).data[0].embedding

    question_vector = np.array(
        [question_embedding],
        dtype="float32"
    )

    distances, indices = index.search(
        question_vector,
        min(k, len(documents))
    )

    selected_knowledge = " ".join(
        [documents[i] for i in indices[0]]
    )

    return selected_knowledge