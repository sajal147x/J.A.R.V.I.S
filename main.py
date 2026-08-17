import argparse
import os
from tokenize import String
from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam
from prompts import system_prompt
from call_function import available_functions
import json


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
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]
    #API CALL TO THE LLM
    generate_content(client, messages, args.verbose, args.user_prompt)


def generate_content(client: OpenAI, messages: list[ChatCompletionMessageParam], verbose : bool = False, userPrompt: str = "") -> None:
    response = client.chat.completions.create(model="openrouter/free", messages=messages, temperature=0, tools=available_functions)
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

    message = response.choices[0].message
    print(message.content)
    if message.tool_calls != None:
        for tool_call in message.tool_calls:
            if tool_call.type != "function":
                continue
            function_args = json.loads(tool_call.function.arguments or "{}")
            print(f"Calling function: {tool_call.function.name}({function_args})")



if __name__ == "__main__":
    main()
