import os

import chromadb
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_openai import ChatOpenAI
from sentence_transformers import SentenceTransformer


load_dotenv()


OPENROUTER_API_KEY = os.getenv(
    "OPENROUTER_API_KEY"
)

OPENROUTER_BASE_URL = (
    "https://openrouter.ai/api/v1"
)

LLM_MODEL = "openrouter/free"

EMBEDDING_MODEL_NAME = (
    "all-MiniLM-L6-v2"
)

CHROMA_PATH = os.path.join(
    os.path.dirname(__file__),
    "library_chroma_db"
)


embedding_model = SentenceTransformer(
    EMBEDDING_MODEL_NAME
)

chroma_client = chromadb.PersistentClient(
    path=CHROMA_PATH
)

library_collection = (
    chroma_client.get_or_create_collection(
        name="real_library_books"
    )
)


def validate_question(question):
    if not isinstance(question, str):
        raise ValueError(
            "Question must be text."
        )

    cleaned_question = question.strip()

    if len(cleaned_question) < 3:
        raise ValueError(
            "Question too short to answer meaningfully."
        )

    return cleaned_question


def retrieve_context(question):
    if library_collection.count() == 0:
        return (
            "No library books are currently indexed."
        )

    question_embedding = (
        embedding_model.encode(
            [question]
        ).tolist()
    )

    result_count = min(
        3,
        library_collection.count()
    )

    results = library_collection.query(
        query_embeddings=question_embedding,
        n_results=result_count
    )

    documents = results.get(
        "documents",
        [[]]
    )[0]

    if not documents:
        return (
            "No relevant library information "
            "was found."
        )

    return "\n".join(
        documents
    )


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a helpful library assistant.

Answer the user's question using ONLY the
library context provided.

Do not invent book titles, authors,
categories, or other information.

If the context is not enough to answer,
say:

"The available library information is not sufficient."
"""
        ),
        (
            "human",
            """
Library context:

{context}

Question:

{question}
"""
        )
    ]
)


llm = ChatOpenAI(
    model=LLM_MODEL,
    api_key=OPENROUTER_API_KEY,
    base_url=OPENROUTER_BASE_URL,
    temperature=0.2
)


input_guard = RunnableLambda(
    lambda question: validate_question(
        question
    )
)


question_with_context = {
    "question": RunnablePassthrough(),
    "context": RunnableLambda(
        retrieve_context
    )
}


rag_chain = (
    input_guard
    | question_with_context
    | prompt
    | llm
    | StrOutputParser()
)


def run_question(question):
    print()
    print("Question:")
    print(question)

    try:
        answer = rag_chain.invoke(
            question
        )

        print()
        print("Answer:")
        print(answer)

    except ValueError as error:
        print()
        print("Input guard:")
        print(error)

    except Exception as error:
        print()
        print("Error:")
        print(error)


def main():
    if not OPENROUTER_API_KEY:
        print(
            "OPENROUTER_API_KEY is missing."
        )
        return

    print(
        "Week 6 Part A - LCEL RAG Demo"
    )

    print(
        "Indexed books:",
        library_collection.count()
    )

    run_question(
        "Who wrote React Essentials?"
    )

    run_question(
        "a"
    )


if __name__ == "__main__":
    main()