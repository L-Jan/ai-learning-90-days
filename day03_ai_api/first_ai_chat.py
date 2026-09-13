from dotenv import load_dotenv
from openai import OpenAI
import os

# 读取 .env
load_dotenv()

# 创建百炼客户端
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)


def ask_ai(question):
    response = client.chat.completions.create(
        model="deepseek-v4-flash-0731",
        messages=[
            {
                "role": "user",
                "content": question
            }
        ]
    )

    return response.choices[0].message.content


# 获取用户输入
user_input = input("请输入你的问题：")

# 调用 AI
answer = ask_ai(user_input)

# 输出回答
print("\nAI回答：")
print(answer)