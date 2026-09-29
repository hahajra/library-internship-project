import os

from dotenv import load_dotenv
from langchain_classic.retrievers.multi_query import MultiQueryRetriever
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_openai import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from langchain_community.vectorstores import Chroma


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


class SentenceTransformerEmbeddings(
    Embeddings
):
    def __init__(
        self,
        model_name
    ):
        self.model = (
            SentenceTransformer(
                model_name
            )
        )

    def embed_documents(
        self,
        texts
    ):
        return self.model.encode(
            texts
        ).tolist()

    def embed_query(
        self,
        text
    ):
        return self.model.encode(
            [text]
        )[0].tolist()


def build_demo_documents():
    return [
        Document(
            page_content=(
                "React Essentials is a book by ali. "
                "It belongs to Web Development. "
                "The book introduces React concepts, "
                "components, frontend development, "
                "and modern web application design."
            ),
            metadata={
                "title": "React Essentials"
            }
        ),
        Document(
            page_content=(
                "Python Fundamentals is a programming "
                "book for beginners. It explains Python "
                "syntax, variables, loops, functions, "
                "and basic software development."
            ),
            metadata={
                "title": "Python Fundamentals"
            }
        ),
        Document(
            page_content=(
                "Database Design Guide explains relational "
                "databases, SQL, tables, keys, normalization, "
                "and database architecture."
            ),
            metadata={
                "title": "Database Design Guide"
            }
        ),
        Document(
            page_content=(
                "Cloud Computing Basics introduces cloud "
                "infrastructure, virtual machines, deployment, "
                "scalability, and distributed systems."
            ),
            metadata={
                "title": "Cloud Computing Basics"
            }
        ),
        Document(
            page_content=(
                "Mystery at Midnight is a fiction book "
                "about a detective investigating a crime "
                "in a small town."
            ),
            metadata={
                "title": "Mystery at Midnight"
            }
        )
    ]


def print_documents(
    label,
    documents
):
    print()
    print(label)

    if not documents:
        print(
            "No documents retrieved."
        )
        return

    for index, document in enumerate(
        documents,
        start=1
    ):
        title = document.metadata.get(
            "title",
            "Unknown"
        )

        print(
            f"{index}. {title}"
        )

        print(
            "   ",
            document.page_content
        )


def main():
    if not OPENROUTER_API_KEY:
        print(
            "OPENROUTER_API_KEY is missing."
        )
        return

    print(
        "Week 6 Part B - "
        "Advanced Retrieval Demo"
    )

    documents = (
        build_demo_documents()
    )

    splitter = (
        RecursiveCharacterTextSplitter(
            chunk_size=300,
            chunk_overlap=40
        )
    )

    chunks = (
        splitter.split_documents(
            documents
        )
    )

    print()
    print(
        "Original documents:",
        len(documents)
    )

    print(
        "Chunks created:",
        len(chunks)
    )

    embeddings = (
        SentenceTransformerEmbeddings(
            EMBEDDING_MODEL_NAME
        )
    )

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=(
            "week6_advanced_retrieval"
        )
    )

    basic_retriever = (
        vector_store.as_retriever(
            search_kwargs={
                "k": 3
            }
        )
    )

    llm = ChatOpenAI(
        model=LLM_MODEL,
        api_key=OPENROUTER_API_KEY,
        base_url=OPENROUTER_BASE_URL,
        temperature=0
    )

    multi_query_retriever = (
        MultiQueryRetriever.from_llm(
            retriever=basic_retriever,
            llm=llm
        )
    )

    questions = [
        (
            "Which book should I read "
            "to learn React?"
        ),
        (
            "Which book explains "
            "programming for beginners?"
        ),
        (
            "Which book is about SQL "
            "and relational databases?"
        ),
        (
            "Which book discusses cloud "
            "infrastructure and deployment?"
        ),
        (
            "Which book is a detective "
            "fiction story?"
        )
    ]

    for number, question in enumerate(
        questions,
        start=1
    ):
        print()
        print(
            "=" * 70
        )

        print(
            f"Question {number}:"
        )

        print(question)

        basic_documents = (
            basic_retriever.invoke(
                question
            )
        )

        print_documents(
            "Basic Retriever:",
            basic_documents
        )

        try:
            multi_documents = (
                multi_query_retriever.invoke(
                    question
                )
            )

            print_documents(
                "MultiQueryRetriever:",
                multi_documents
            )

        except Exception as error:
            print()
            print(
                "Multi-query retrieval failed:"
            )

            print(error)

    print()
    print(
        "=" * 70
    )

    print(
        "Comparison complete."
    )

    print(
        "MultiQueryRetriever may improve "
        "recall by generating alternate "
        "versions of the user's question."
    )

    print(
        "However, broader alternate queries "
        "can sometimes reduce precision by "
        "retrieving extra unrelated documents."
    )


if __name__ == "__main__":
    main()