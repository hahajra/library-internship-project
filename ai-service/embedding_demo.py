from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"


def main():
    print("Loading embedding model...")

    model = SentenceTransformer(
        MODEL_NAME
    )

    sentences = [
        "Python is a programming language.",
        "Software development uses programming tools.",
        "A detective investigates a mysterious crime."
    ]

    print("Creating embeddings...")

    embeddings = model.encode(
        sentences
    )

    print()
    print("Embedding model:")
    print(MODEL_NAME)

    print()
    print("Number of sentences:")
    print(len(sentences))

    print()
    print("Embedding shape:")
    print(embeddings.shape)

    print()
    print("First sentence:")
    print(sentences[0])

    print()
    print("First 10 embedding values:")
    print(embeddings[0][:10])


if __name__ == "__main__":
    main()