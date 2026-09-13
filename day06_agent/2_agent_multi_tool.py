from openai import OpenAI
import os
from dotenv import load_dotenv


load_dotenv()


client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)


# 工具1：计算器
def calculator(expression):
    try:
        result = eval(expression)
        return str(result)
    except:
        return "计算失败"


# 工具2：时间
from datetime import datetime

def get_time():
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


def ask_ai(question):
    response = client.chat.completions.create(
        model="deepseek-v4-flash-0731",
        messages=[
            {
                "role":"system",
                "content":
"""
你是一个AI助手。

你拥有两个工具：

1. calculator
用于数学计算

格式：
TOOL:calculator:表达式

例如：
TOOL:calculator:128*36


2. time
用于查询当前时间

格式：
TOOL:time


如果不需要工具，
直接回答用户。
"""
            },
            {
                "role":"user",
                "content":question
            }
        ]
    )

    return response.choices[0].message.content


while True:
    question=input("\n用户：")

    if question=="退出":
        break

    answer=ask_ai(question)

    # 判断是否调用工具
    if answer.startswith("TOOL:"):
        command = answer.replace(
            "TOOL:",
            ""
        )

        if command.startswith("calculator:"):
            expression = command.replace(
                "calculator:",
                ""
            )

            result = calculator(expression)

            print("\n计算结果：")
            print(result)

        elif command.startswith("time"):
            result = get_time()

            print("\n当前时间：")
            print(result)

        else:
            print("未知工具")

    else:
        print("\nAI:")
        print(answer)