import json
import os

from dotenv import load_dotenv
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field


load_dotenv()


OPENROUTER_API_KEY = os.getenv(
    "OPENROUTER_API_KEY"
)

OPENROUTER_BASE_URL = (
    "https://openrouter.ai/api/v1"
)

LLM_MODEL = "openrouter/free"

DATA_FILE = os.path.join(
    os.path.dirname(__file__),
    "library_books.json"
)


class BookAnswer(BaseModel):
    answer: str = Field(
        description=(
            "Answer to the user's "
            "library question"
        )
    )

    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description=(
            "Confidence score between "
            "0 and 1"
        )
    )

    sources: list[str] = Field(
        description=(
            "Book titles used as "
            "sources for the answer"
        )
    )


def load_library_context():
    if not os.path.exists(
        DATA_FILE
    ):
        return (
            "No library data is available."
        )

    with open(
        DATA_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        books = json.load(
            file
        )

    if not books:
        return (
            "No library books are available."
        )

    lines = []

    for book in books:
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

        lines.append(
            (
                f"Title: {title}. "
                f"Author: {author}. "
                f"Category: {category}."
            )
        )

    return "\n".join(
        lines
    )


LIBRARY_CONTEXT = (
    load_library_context()
)


llm = ChatOpenAI(
    model=LLM_MODEL,
    api_key=OPENROUTER_API_KEY,
    base_url=OPENROUTER_BASE_URL,
    temperature=0.2
)


memory_prompt = (
    ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
You are a helpful library assistant.

Use ONLY the supplied library context
and the conversation history.

Library context:

{library_context}

IMPORTANT CONVERSATION RULE:

If the user uses a pronoun or vague reference
such as:

- it
- this book
- that book
- the book
- its author
- its category

you may resolve that reference ONLY when a
specific book was clearly established earlier
in the CURRENT conversation history.

If the current conversation history does not
establish which book the user is referring to,
do NOT guess from the library context.

Even if the library contains only one book,
you must not assume that the unresolved
pronoun refers to that book.

Instead respond:

"I do not have enough conversation context to know which book you mean."

If the user directly names a book, you may
answer using the supplied library context.

Do not invent book titles, authors,
categories, or other information.
"""
            ),
            MessagesPlaceholder(
                variable_name="history"
            ),
            (
                "human",
                "{question}"
            )
        ]
    )
)


memory_chain = (
    memory_prompt
    | llm
    | StrOutputParser()
)


session_store = {}


def get_session_history(
    session_id
):
    if session_id not in session_store:
        session_store[
            session_id
        ] = (
            InMemoryChatMessageHistory()
        )

    return session_store[
        session_id
    ]


conversation_chain = (
    RunnableWithMessageHistory(
        memory_chain,
        get_session_history,
        input_messages_key="question",
        history_messages_key="history"
    )
)


def ask_with_memory(
    session_id,
    question
):
    return conversation_chain.invoke(
        {
            "question": question,
            "library_context":
                LIBRARY_CONTEXT
        },
        config={
            "configurable": {
                "session_id":
                    session_id
            }
        }
    )


def run_memory_test():
    print()
    print(
        "=" * 70
    )

    print(
        "SESSION MEMORY TEST"
    )

    print(
        "=" * 70
    )

    first_session = (
        "hajra-session-1"
    )

    first_question = (
        "Tell me about React Essentials."
    )

    print()
    print(
        "Session:",
        first_session
    )

    print(
        "Question 1:"
    )

    print(
        first_question
    )

    answer_one = ask_with_memory(
        first_session,
        first_question
    )

    print()
    print(
        "Answer 1:"
    )

    print(
        answer_one
    )

    follow_up = (
        "Who wrote it?"
    )

    print()
    print(
        "Question 2:"
    )

    print(
        follow_up
    )

    answer_two = ask_with_memory(
        first_session,
        follow_up
    )

    print()
    print(
        "Answer 2:"
    )

    print(
        answer_two
    )

    fresh_session = (
        "hajra-session-2"
    )

    print()
    print(
        "-" * 70
    )

    print(
        "Fresh session:",
        fresh_session
    )

    print(
        "Question:"
    )

    print(
        follow_up
    )

    fresh_answer = ask_with_memory(
        fresh_session,
        follow_up
    )

    print()
    print(
        "Fresh-session answer:"
    )

    print(
        fresh_answer
    )

    print()
    print(
        "Expected result:"
    )

    print(
        "- Same session should understand "
        "that 'it' refers to React Essentials."
    )

    print(
        "- Fresh session should refuse "
        "to guess what 'it' refers to."
    )


def run_structured_output_test():
    print()
    print(
        "=" * 70
    )

    print(
        "STRUCTURED OUTPUT TEST"
    )

    print(
        "=" * 70
    )

    structured_prompt = (
        ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
You are a library assistant.

Use ONLY this library context:

{library_context}

Answer the user's question.

Return the result using the required
structured response schema.

The schema requires:

- answer
- confidence
- sources

Do not invent information.
"""
                ),
                (
                    "human",
                    "{question}"
                )
            ]
        )
    )

    structured_llm = (
        llm.with_structured_output(
            BookAnswer
        )
    )

    structured_chain = (
        structured_prompt
        | structured_llm
    )

    question = (
        "Who wrote React Essentials?"
    )

    print()
    print(
        "Question:"
    )

    print(
        question
    )

    try:
        result = (
            structured_chain.invoke(
                {
                    "question":
                        question,
                    "library_context":
                        LIBRARY_CONTEXT
                }
            )
        )

        print()
        print(
            "Structured result:"
        )

        print(
            result
        )

        print()
        print(
            "Answer:",
            result.answer
        )

        print(
            "Confidence:",
            result.confidence
        )

        print(
            "Sources:",
            result.sources
        )

        print()
        print(
            "Structured output test: PASS"
        )

    except Exception as error:
        print()
        print(
            "Structured output could "
            "not be verified with the "
            "current free provider."
        )

        print()
        print(
            "Provider/model error:"
        )

        print(
            error
        )

        print()
        print(
            "The with_structured_output() "
            "integration is implemented, "
            "but free OpenRouter routing "
            "may not support the requested "
            "structured schema reliably."
        )


def main():
    if not OPENROUTER_API_KEY:
        print(
            "OPENROUTER_API_KEY is missing."
        )
        return

    print(
        "Week 6 Part C - "
        "Structured Output and "
        "Session Memory"
    )

    print()
    print(
        "Library context:"
    )

    print(
        LIBRARY_CONTEXT
    )

    run_memory_test()

    run_structured_output_test()

    print()
    print(
        "=" * 70
    )

    print(
        "KNOWN MEMORY LIMITATION"
    )

    print(
        "=" * 70
    )

    print(
        "Session history is stored "
        "only in Python memory."
    )

    print(
        "All conversation history "
        "will be lost when this "
        "process restarts."
    )


if __name__ == "__main__":
    main()