import os
from dotenv import load_dotenv
import dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam



def main():

    #CONFIG
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key == None:
        raise RuntimeError("Could Not Load API Key")
    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key,)
    messages: list[ChatCompletionMessageParam]  = [
        {
            "role": "user",
            "content": "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.",
        }
    ]
    #API CALL TO THE LLM
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
