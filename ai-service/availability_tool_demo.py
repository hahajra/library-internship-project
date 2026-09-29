import json
import os

import httpx
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI


load_dotenv()


OPENROUTER_API_KEY = os.getenv(
    "OPENROUTER_API_KEY"
)

OPENROUTER_BASE_URL = (
    "https://openrouter.ai/api/v1"
)

LLM_MODEL = "openrouter/free"

BACKEND_BASE_URL = (
    "https://localhost:7038"
)


@tool
def check_book_availability(
    book_id: int
) -> str:
    """
    Check whether a library book is currently available.

    Use this tool only when the user asks about
    the current availability, borrowing status,
    or whether a specific book can be borrowed.

    Do not use this tool for genre, author,
    category, summary, or general book questions.
    """

    url = (
        f"{BACKEND_BASE_URL}"
        f"/api/Books/{book_id}/availability"
    )

    try:
        response = httpx.get(
            url,
            timeout=20.0,
            verify=False
        )

        if response.status_code == 404:
            return json.dumps(
                {
                    "error": "Book not found.",
                    "bookId": book_id
                }
            )

        response.raise_for_status()

        data = response.json()

        return json.dumps(
            data
        )

    except httpx.RequestError as error:
        return json.dumps(
            {
                "error": (
                    "Could not reach the "
                    "Library API."
                ),
                "details": str(error)
            }
        )

    except httpx.HTTPStatusError as error:
        return json.dumps(
            {
                "error": (
                    "Library API returned "
                    "an error."
                ),
                "statusCode":
                    error.response.status_code
            }
        )


llm = ChatOpenAI(
    model=LLM_MODEL,
    api_key=OPENROUTER_API_KEY,
    base_url=OPENROUTER_BASE_URL,
    temperature=0
)


tools = [
    check_book_availability
]


llm_with_tools = llm.bind_tools(
    tools
)


SYSTEM_INSTRUCTIONS = """
You are a library assistant.

You have access to one tool:

check_book_availability

STRICT TOOL RULES:

1. Use check_book_availability ONLY when the
   user asks whether a specific book is
   currently available, borrowed, unavailable,
   or ready to borrow.

2. Do NOT use the availability tool for:
   - genre questions
   - category questions
   - author questions
   - summaries
   - recommendations
   - general book information

3. If a question does not require current
   availability information, answer normally
   without calling the tool.

4. Never invent an availability result.

5. When tool output is provided, use it to
   create a short natural-language answer.
"""


def run_tool_flow(
    question: str
):
    print()
    print(
        "=" * 70
    )

    print(
        "Question:"
    )

    print(
        question
    )

    messages = [
        SystemMessage(
            content=SYSTEM_INSTRUCTIONS
        ),
        HumanMessage(
            content=question
        )
    ]

    response = (
        llm_with_tools.invoke(
            messages
        )
    )

    tool_calls = (
        response.tool_calls
        if response.tool_calls
        else []
    )

    if not tool_calls:
        print()
        print(
            "Tool call:"
        )

        print(
            "No tool call."
        )

        print()
        print(
            "Model answer:"
        )

        print(
            response.content
        )

        return False

    print()
    print(
        "Tool call detected."
    )

    print(
        "Tool calls:"
    )

    print(
        tool_calls
    )

    messages.append(
        response
    )

    for tool_call in tool_calls:
        tool_name = (
            tool_call["name"]
        )

        tool_args = (
            tool_call["args"]
        )

        tool_call_id = (
            tool_call["id"]
        )

        if tool_name != (
            "check_book_availability"
        ):
            continue

        print()
        print(
            "Executing tool:"
        )

        print(
            tool_name
        )

        print(
            "Arguments:"
        )

        print(
            tool_args
        )

        tool_result = (
            check_book_availability.invoke(
                tool_args
            )
        )

        print()
        print(
            "Tool result:"
        )

        print(
            tool_result
        )

        messages.append(
            ToolMessage(
                content=tool_result,
                tool_call_id=tool_call_id
            )
        )

    final_response = (
        llm_with_tools.invoke(
            messages
        )
    )

    print()
    print(
        "Final answer:"
    )

    print(
        final_response.content
    )

    return True


def main():
    if not OPENROUTER_API_KEY:
        print(
            "OPENROUTER_API_KEY is missing."
        )
        return

    print(
        "Week 6 Part D - "
        "Book Availability Tool"
    )

    availability_called = (
        run_tool_flow(
            "Is book 2 available right now?"
        )
    )

    genre_called = (
        run_tool_flow(
            "What genre is book 2?"
        )
    )

    print()
    print(
        "=" * 70
    )

    print(
        "TEST RESULTS"
    )

    print(
        "=" * 70
    )

    if availability_called:
        print(
            "PASS: Availability question "
            "triggered the tool."
        )

    else:
        print(
            "FAIL: Availability question "
            "did not trigger the tool."
        )

    if not genre_called:
        print(
            "PASS: Genre question did not "
            "trigger the availability tool."
        )

    else:
        print(
            "FAIL: Genre question incorrectly "
            "triggered the availability tool."
        )


if __name__ == "__main__":
    main()