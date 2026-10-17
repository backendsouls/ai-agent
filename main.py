import argparse
import os

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam


def main(api_key: str | None) -> None:
    if api_key is None:
        raise RuntimeError("API KEY not found!")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    user_prompt: str = args.user_prompt
    is_verbose: bool = args.verbose

    messages: list[ChatCompletionMessageParam] = [
        {
            "role": "user",
            "content": user_prompt,
        }
    ]

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
    )

    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    content: str | None = response.choices[0].message.content

    if response.usage:
        prompt_tokens = response.usage.prompt_tokens
        completion_tokens = response.usage.completion_tokens

    if is_verbose:
        print(f"User prompt: {prompt_tokens}")
        print(f"Prompt tokens: {completion_tokens}")
        print(f"Response tokens: {response.choices[0].message.content}")
        return

    print(content)


if __name__ == "__main__":
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    main(api_key)
