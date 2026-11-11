
import asyncio

from services.conversation import handle_seller_message


async def main():

    history = []

    questions = [
        "Why have my sales dropped this month?",
        "Most of my cancellations happen because products are unavailable.",
        "What should I do first?"
    ]

    for question in questions:

        answer = await handle_seller_message(
            question,
            history
        )

        print("\nSeller:", question)
        print("\nAI KAM:", answer)
        print("\n" + "-" * 60)


if __name__ == "__main__":
    asyncio.run(main())
