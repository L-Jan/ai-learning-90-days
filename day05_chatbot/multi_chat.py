from openai import OpenAI
import os
from dotenv import load_dotenv


# 加载环境变量
load_dotenv()


client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)


# 保存聊天历史
messages = [
    {
        "role": "system",
        "content": "你是一个友好的AI助手"
    }
]


def chat_ai(user_message):

    # 加入用户消息
    messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )


    response = client.chat.completions.create(
        model="deepseek-v4-flash-0731",
        messages=messages
    )


    answer = response.choices[0].message.content


    # 保存AI回复
    messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )


    return answer



while True:

    user_input = input("\n你：")


    if user_input == "退出":
        print("聊天结束")
        break


    result = chat_ai(user_input)

    print("\nAI：")
    print(result)