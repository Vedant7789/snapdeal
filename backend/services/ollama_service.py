
import httpx

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "qwen2.5:7b"


async def generate_response(messages: list[dict]) -> str:
    """
    Send conversation messages to Ollama
    and return the model's response.
    """

    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "stream": False
    }

    timeout = httpx.Timeout(
        connect=10.0,
        read=120.0,
        write=10.0,
        pool=10.0
    )

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(
                OLLAMA_URL,
                json=payload
            )

            response.raise_for_status()

            result = response.json()

            return result["message"]["content"].strip()

    except httpx.ConnectError:
        raise RuntimeError(
            "Cannot connect to Ollama. Make sure Ollama is running."
        )

    except httpx.TimeoutException:
        raise RuntimeError(
            "Ollama took too long to respond."
        )

    except httpx.HTTPStatusError as error:
        raise RuntimeError(
            f"Ollama returned HTTP error: {error.response.status_code}"
        )

    except (KeyError, ValueError):
        raise RuntimeError(
            "Unexpected response received from Ollama."
        )
