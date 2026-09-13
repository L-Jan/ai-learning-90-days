from openai import OpenAI
import os
from dotenv import load_dotenv


load_dotenv()


client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)


# 工具
def calculator(expression):
    try:
        result = eval(expression)
        return str(result)

    except:
        return "计算失败"



def ask_ai(question):
    response = client.chat.completions.create(
        model="deepseek-v4-flash-0731",
        messages=[
            {
                "role":"system",
                "content":
                """
                你是一个AI助手。

                如果用户的问题需要数学计算，
                回复格式：

                TOOL:表达式

                例如：

                TOOL:128*36

                如果不需要计算，
                直接回答。
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
        expression=answer.replace(
            "TOOL:",
            ""
        )

        result=calculator(expression)

        print("\n工具计算结果：")
        print(result)

    else:
        print("\nAI:")
        print(answer)