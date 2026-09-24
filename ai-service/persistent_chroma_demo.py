import os

import chromadb
from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"

CHROMA_PATH = os.path.join(
    os.path.dirname(__file__),
    "chroma_db"
)


def main():
    print("Loading embedding model...")

    model = SentenceTransformer(
        MODEL_NAME
    )

    client = chromadb.PersistentClient(
        path=CHROMA_PATH
    )

    collection = client.get_or_create_collection(
        name="library_books"
    )

    documents = [
        "Python programming for beginners.",
        "A detective investigates a murder mystery.",
        "A romantic story about love and relationships.",
        "A science fiction story about robots and space."
    ]

    ids = [
        "book1",
        "book2",
        "book3",
        "book4"
    ]

    embeddings = model.encode(
        documents
    ).tolist()

    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings
    )

    print()
    print("Documents stored:")
    print(collection.count())

    query = "Which book is useful for learning programming?"

    query_embedding = model.encode(
        [query]
    ).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=2
    )

    print()
    print("Query:")
    print(query)

    print()
    print("Retrieved documents:")

    for document in results["documents"][0]:
        print("-", document)

    print()
    print("Chroma database saved at:")
    print(CHROMA_PATH)


if __name__ == "__main__":
    main()