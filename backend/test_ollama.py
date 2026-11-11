
import asyncio

from services.ollama_service import generate_response


async def main():
    messages = [
        {
            "role": "system",
            "content": "You are a helpful ecommerce business consultant."
        },
        {
            "role": "user",
            "content": (
                "A seller's sales dropped from 200000 to 135000. "
                "Calculate the percentage decline in one sentence."
            )
        }
    ]

    answer = await generate_response(messages)

    print("\nQwen response:")
    print(answer)


if __name__ == "__main__":
    asyncio.run(main())
