import os
import json

import chromadb
from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"

CHROMA_PATH = os.path.join(
    os.path.dirname(__file__),
    "library_chroma_db"
)

DATA_FILE = os.path.join(
    os.path.dirname(__file__),
    "library_books.json"
)


def main():
    if not os.path.exists(DATA_FILE):
        print("library_books.json was not found.")
        return

    with open(
        DATA_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        books = json.load(file)

    model = SentenceTransformer(
        MODEL_NAME
    )

    client = chromadb.PersistentClient(
        path=CHROMA_PATH
    )

    collection = client.get_or_create_collection(
        name="real_library_books"
    )

    ids = []
    documents = []
    metadatas = []

    for book in books:
        book_id = str(
            book.get("bookId")
            or book.get("id")
        )

        title = book.get(
            "title",
            "Unknown Title"
        )

        author = book.get(
            "author",
            "Unknown Author"
        )

        category = book.get(
            "category",
            "Unknown Category"
        )

        document = (
            f"Title: {title}. "
            f"Author: {author}. "
            f"Category: {category}."
        )

        ids.append(book_id)
        documents.append(document)

        metadatas.append({
            "title": title,
            "author": author,
            "category": category
        })

    embeddings = model.encode(
        documents
    ).tolist()

    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )

    print(
        "Books indexed:",
        collection.count()
    )

    print(
        "Database saved at:",
        CHROMA_PATH
    )


if __name__ == "__main__":
    main()