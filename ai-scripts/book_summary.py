import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    print("OPENROUTER_API_KEY was not found in the .env file.")
    raise SystemExit

print("Library Book Summary Generator")
print("------------------------------")

book_title = input("Enter book title: ").strip()
author = input("Enter author name: ").strip()
category = input("Enter category: ").strip()
description = input("Enter a short book description: ").strip()

if not book_title or not description:
    print("Book title and description are required.")
    raise SystemExit

prompt = f"""
Create a short and clear summary for this library book.

Title: {book_title}
Author: {author}
Category: {category}
Description: {description}

Keep the summary concise and easy to understand.
"""

url = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

data = {
    "model": "openrouter/free",
    "messages": [
        {
            "role": "system",
            "content": "You create short, clear summaries for library books."
        },
        {
            "role": "user",
            "content": prompt
        }
    ]
}

try:
    response = requests.post(
        url,
        headers=headers,
        json=data,
        timeout=60
    )

    response.raise_for_status()

    result = response.json()

    summary = result["choices"][0]["message"]["content"]

    print("\nAI Summary")
    print("----------")
    print(summary)

except requests.exceptions.RequestException as error:
    print("\nUnable to generate summary.")
    print(error)

except (KeyError, IndexError):
    print("\nUnexpected response from OpenRouter.")