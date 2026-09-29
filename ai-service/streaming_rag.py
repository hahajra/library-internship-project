import json
import os

import httpx
from dotenv import load_dotenv


load_dotenv()


OPENROUTER_API_KEY = os.getenv(
    "OPENROUTER_API_KEY"
)

OPENROUTER_URL = (
    "https://openrouter.ai/api/v1/chat/completions"
)

MODEL_NAME = os.getenv(
    "OPENROUTER_MODEL",
    "openrouter/free"
)


async def generate_answer_stream(
    system_prompt: str,
    user_prompt: str
):
    if not OPENROUTER_API_KEY:
        raise RuntimeError(
            "OPENROUTER_API_KEY is missing."
        )

    payload = {
        "model": MODEL_NAME,
        "temperature": 0.2,
        "max_tokens": 250,
        "stream": True,
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

    async with httpx.AsyncClient(
        timeout=None
    ) as client:

        async with client.stream(
            "POST",
            OPENROUTER_URL,
            headers=headers,
            json=payload
        ) as response:

            if response.status_code != 200:
                body = await response.aread()

                raise RuntimeError(
                    "OpenRouter streaming request "
                    f"failed with status "
                    f"{response.status_code}: "
                    f"{body.decode(errors='ignore')}"
                )

            async for line in response.aiter_lines():
                if not line:
                    continue

                if not line.startswith(
                    "data:"
                ):
                    continue

                data = line[5:].strip()

                if data == "[DONE]":
                    break

                try:
                    event = json.loads(
                        data
                    )

                except json.JSONDecodeError:
                    continue

                choices = event.get(
                    "choices",
                    []
                )

                if not choices:
                    continue

                delta = (
                    choices[0]
                    .get("delta", {})
                )

                content = delta.get(
                    "content"
                )

                if content:
                    yield content