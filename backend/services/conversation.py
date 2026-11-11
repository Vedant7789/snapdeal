

import json

from prompts.system_prompt import SYSTEM_PROMPT
from services.analytics import analyze_seller_performance
from services.ollama_service import generate_response


async def handle_seller_message(
    user_message: str,
    history: list[dict]
) -> str:

    analytics = analyze_seller_performance()

    analytics_context = f"""
SELLER: Demo Seller

PERFORMANCE ANALYSIS:
{json.dumps(analytics, indent=2)}

DATA LIMITATIONS:
- Product-level inventory details are unavailable.
- Cancellation reasons are unavailable.
- Traffic, impressions and listing visits are unavailable.

Use only the available metrics and information shared
by the seller during this conversation.

Do not assume missing details.
"""

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "system",
            "content": analytics_context
        }
    ]

    # Include recent conversation history.
    messages.extend(history[-8:])

    # Add the latest seller message.
    messages.append({
        "role": "user",
        "content": user_message
    })

    # Generate the response.
    answer = await generate_response(messages)

    # Save both sides of the conversation.
    history.extend([
        {
            "role": "user",
            "content": user_message
        },
        {
            "role": "assistant",
            "content": answer
        }
    ])

    # Keep the conversation history manageable.
    del history[:-8]

    return answer
