from openai import OpenAI
import os
from dotenv import load_dotenv


load_dotenv()


client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)


def ask_ai(prompt):

    response = client.chat.completions.create(
        model="deepseek-v4-flash-0731",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content



product = input("请输入产品：")
audience = input("请输入目标用户：")


prompt = f"""
你是一名拥有5年经验的小红书美妆品牌运营专家。

请为下面产品生成5个高点击率标题：

产品：
{product}

目标用户：
{audience}


要求：

1. 符合小红书爆款标题风格
2. 标题包含用户痛点或使用场景
3. 激发收藏和点击欲望
4. 不使用虚假夸大宣传
5. 每个标题20字以内
6. 风格参考：
   - 姐妹分享
   - 真实体验
   - 避坑推荐
   - 成分分析


只输出标题，不要解释。
"""


answer = ask_ai(prompt)


print("AI回答：")
print(answer)