from openai import OpenAI
import os
from dotenv import load_dotenv
import json


load_dotenv()


client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)



# 工具函数
def calculator(expression):
    result = eval(expression)
    return str(result)

# 工具描述
tools = [
    {
        "type": "function",
        "function": {

            "name": "calculator",

            "description":
            "用于数学计算",

            "parameters": {

                "type": "object",

                "properties": {

                    "expression": {

                        "type": "string",

                        "description":
                        "数学表达式，例如 128*36"

                    }

                },

                "required":[
                    "expression"
                ]

            }

        }

    }
]


def ask_ai(question):
    response = client.chat.completions.create(
        model="deepseek-v4-flash-0731",
        messages=[
            {
                "role":"user",

                "content":question
            }
        ],
        tools=tools
    )
    return response.choices[0].message


while True:
    question=input("\n用户：")

    if question=="退出":
        break

    message=ask_ai(question)

    # 判断AI是否调用工具
    if message.tool_calls:
        tool_call=message.tool_calls[0]
        function_name=tool_call.function.name
        arguments=json.loads(
            tool_call.function.arguments
        )
        if function_name=="calculator":
            result=calculator(
                arguments["expression"]
            )
            print("\n计算结果：")
            print(result)

    else:
        print("\nAI:")
        print(message.content)