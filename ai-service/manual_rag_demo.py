import os

import chromadb
import httpx
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer


load_dotenv()


MODEL_NAME = "all-MiniLM-L6-v2"
LLM_MODEL = "openrouter/free"

OPENROUTER_API_KEY = os.getenv(
    "OPENROUTER_API_KEY"
)

OPENROUTER_URL = (
    "https://openrouter.ai/api/v1/chat/completions"
)

CHROMA_PATH = os.path.join(
    os.path.dirname(__file__),
    "chroma_db"
)


def main():
    if not OPENROUTER_API_KEY:
        print(
            "OPENROUTER_API_KEY is missing."
        )
        return

    print("Loading embedding model...")

    embedding_model = SentenceTransformer(
        MODEL_NAME
    )

    client = chromadb.PersistentClient(
        path=CHROMA_PATH
    )

    collection = client.get_or_create_collection(
        name="library_books"
    )

    question = (
        "Which book should I read if I want "
        "to learn programming?"
    )

    print()
    print("Question:")
    print(question)

    question_embedding = embedding_model.encode(
        [question]
    ).tolist()

    results = collection.query(
        query_embeddings=question_embedding,
        n_results=2
    )

    retrieved_documents = (
        results["documents"][0]
    )

    print()
    print("Retrieved context:")

    for document in retrieved_documents:
        print("-", document)

    context = "\n".join(
        retrieved_documents
    )

    system_prompt = """
You are a library assistant.

Answer the user's question using ONLY the
provided library context.

If the answer cannot be found in the context,
say that the available library information is
not sufficient.

Do not invent books or information.
"""

    user_prompt = f"""
Library context:

{context}

Question:

{question}
"""

    payload = {
        "model": LLM_MODEL,
        "temperature": 0.2,
        "max_tokens": 150,
        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]
    }

    headers = {
        "Authorization":
            f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type":
            "application/json"
    }

    print()
    print("Sending retrieved context to LLM...")

    try:
        response = httpx.post(
            OPENROUTER_URL,
            headers=headers,
            json=payload,
            timeout=60.0
        )

        if response.status_code != 200:
            print()
            print("LLM request failed.")
            print(
                "Status:",
                response.status_code
            )
            print(response.text)
            return

        data = response.json()

        answer = (
            data["choices"][0]
            ["message"]["content"]
        )

        print()
        print("RAG Answer:")
        print(answer)

        print()
        print("Model:")
        print(LLM_MODEL)

    except httpx.RequestError as error:
        print()
        print(
            "Could not reach OpenRouter:"
        )
        print(error)


if __name__ == "__main__":
    main()