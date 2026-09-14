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
                "score": 评分,
                "selling_points": [
                    "卖点1",
                    "卖点2",
                    "卖点3"
                ],
                "xiaohongshu_topics": [
                    "选题1",
                    "选题2",
                    "选题3"
                ]
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


selling_points = result["selling_points"]
print("\n产品卖点：")
for point in selling_points:
    print("-", point)


topics = result["xiaohongshu_topics"]
print("\n小红书选题：")
for topic in topics:
    print("-", topic)
