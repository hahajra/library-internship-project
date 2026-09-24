import chromadb
from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"


def main():
    print("Loading embedding model...")

    model = SentenceTransformer(
        MODEL_NAME
    )

    client = chromadb.Client()

    collection = client.create_collection(
        name="books_demo"
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

    print("Creating embeddings...")

    embeddings = model.encode(
        documents
    ).tolist()

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings
    )

    query = "I want a book about coding and software."

    print()
    print("Query:")
    print(query)

    query_embedding = model.encode(
        [query]
    ).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=2
    )

    print()
    print("Top matching books:")

    for document in results["documents"][0]:
        print("-", document)


if __name__ == "__main__":
    main()