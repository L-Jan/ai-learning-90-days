from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

question = input("请输入一个美妆产品：")

response = client.chat.completions.create(
    model="deepseek-v4-flash-0731",
    messages=[
        {
            "role": "system",
            "content": """
            你是一个美妆产品分析助手。

            用户输入一个美妆产品后，
            请严格按照JSON格式返回：

            {
                "product_type": "产品类型",
                "target_user": "适合人群",
                "score": 评分
            }

            只返回JSON，不要添加其他解释。
            """
        },
        {
            "role": "user",
            "content": question
        }
    ]
)

answer = response.choices[0].message.content

print("\nAI返回：")
print(answer)

result = json.loads(answer)     #把json字符串加载/解析成字典格式

print("\n数据类型：")
print(type(answer))
print(type(result))

print("\nPython解析后的结果：")
print(result)


product_type = result["product_type"]
target_user = result["target_user"]
score = result["score"]

print("\n产品类型：", product_type)
print("适合人群：", target_user)
print("评分：", score)