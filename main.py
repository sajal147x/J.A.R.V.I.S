import argparse
import os

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam


def main():

    #PARSING USER INPUT
    parser = argparse.ArgumentParser(description="chatbot")
    parser.add_argument("user_prompt", type=str, help="User Prompt")
    args = parser.parse_args()
    #CONFIG
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key == None:
        raise RuntimeError("Could Not Load API Key")
    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key,)
    messages: list[ChatCompletionMessageParam]  = [
        {
            "role": "user",
            "content": args.user_prompt,
        }
    ]
    #API CALL TO THE LLM
    generate_content(client, messages)


def generate_content(client: OpenAI, messages: list[ChatCompletionMessageParam]) -> None:
    response = client.chat.completions.create(model="openrouter/free", messages=messages)
    usage = response.usage
    #HANDLING NULL CASE
    if usage == None:
        raise RuntimeError("Failed API Request")
    #OUTPUT DETAILS
    print("Prompt tokens: ", usage.prompt_tokens)
    print("Response tokens: ", usage.completion_tokens)
    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
