import argparse
import os
from tokenize import String

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam


def main():

    #PARSING USER INPUT
    parser = argparse.ArgumentParser(description="chatbot")
    parser.add_argument("user_prompt", type=str, help="User Prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
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
    generate_content(client, messages, args.verbose, args.user_prompt)


def generate_content(client: OpenAI, messages: list[ChatCompletionMessageParam], verbose : bool = False, userPrompt: str = "") -> None:
    response = client.chat.completions.create(model="openrouter/free", messages=messages)
    usage = response.usage
    #HANDLING NULL CASE
    if usage == None:
        raise RuntimeError("Failed API Request")
    #OUTPUT DETAILS
    # VERBOSE FIRST
    if verbose:
        print("User prompt: ", userPrompt)
        print("Prompt tokens: ", usage.prompt_tokens)
        print("Response tokens: ", usage.completion_tokens)

    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
