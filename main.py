import argparse
import os
from tokenize import String
from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam
from prompts import system_prompt
from call_function import available_functions, call_function
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
    messages= [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]
    #API CALL TO THE LLM
    max_iterations = 20
    for _ in range(max_iterations):
        is_final = generate_content(client, messages, args.verbose, args.user_prompt)
        if is_final:
            break
    else:
        print(f"Error: Reached max iterations ({max_iterations}) without a final response. The agent may be stuck in a tool-calling loop.")


def generate_content(client: OpenAI, messages, verbose : bool = False, userPrompt: str = "") -> bool:
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
    messages.append(message)
    if message.tool_calls == None:
        print(f"Final response: {message.content}")
        return True
    for tool_call in message.tool_calls:
        if tool_call.type != "function":
            continue
        function_args = json.loads(tool_call.function.arguments or "{}")
        result_message = call_function(tool_call, verbose)
        if result_message["content"] is None or len(result_message["content"]) <=0 :
            raise Exception("Content of tool call is empty")
        if verbose:
            print(f"-> {result_message['content']}")
        messages.append(result_message)
    return False

if __name__ == "__main__":
    main()
