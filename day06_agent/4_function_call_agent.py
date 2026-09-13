from openai import OpenAI
import os
from dotenv import load_dotenv
import json


load_dotenv()


client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)



# 真实工具
def calculator(a, b):
    return str(a + b)

# 工具描述
tools = [
    {
        "type": "function",

        "function": {

            "name": "calculator",

            "description":
            "计算两个数字的和",

            "parameters": {

                "type": "object",

                "properties": {

                    "a": {
                        "type":"number",
                        "description":"第一个数字"
                    },

                    "b": {
                        "type":"number",
                        "description":"第二个数字"
                    }

                },

                "required":[
                    "a",
                    "b"
                ]

            }

        }

    }
]




def ask_ai(question):
    messages=[
        {
            "role":"user",
            "content":question
        }
    ]

    response = client.chat.completions.create(
        model="deepseek-v4-flash-0731",
        messages=messages,
        tools=tools
    )
    message=response.choices[0].message

    # 判断AI是否调用工具
    if message.tool_calls:
        tool_call=message.tool_calls[0]
        args=json.loads(
            tool_call.function.arguments
        )
        result=calculator(
            args["a"],
            args["b"]
        )
        return "计算结果："+result

    else:
        return message.content


while True:
    question=input("\n用户：")
    if question=="退出":
        break
    answer=ask_ai(question)
    print("\nAI:")
    print(answer)