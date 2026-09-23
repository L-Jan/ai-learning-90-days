import os
import dashscope
from dotenv import load_dotenv
from openai import OpenAI
from http import HTTPStatus

load_dotenv()

# 获取 API Key
dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")

# 设置百炼业务空间地址
dashscope.base_http_api_url = (
    "https://ws-e61gqeozrw0qsxpu.cn-beijing.maas.aliyuncs.com/api/v1"
)

question = "公司员工有什么福利？"

documents = [
    "公司工作日上班时间为上午9点到下午6点。",
    "员工出差产生的交通费可以申请报销。",
    "公司正式员工每年享有10天带薪年假。",
    "员工入职满一年后可以享受更多公司福利。"
]

print("===== 问题 =====")
print(question)

print("\n===== 原始文档 =====")

for i, document in enumerate(documents):
    print(f"{i + 1}. {document}")


# 调用 Rerank 模型
response = dashscope.TextReRank.call(
    model="qwen3-rerank",
    query=question,
    documents=documents,
    top_n=4,
    return_documents=True
)


if response.status_code == HTTPStatus.OK:

    # print("\n===== Rerank结果 =====")
    # print(response)
    results = response.output["results"]

    print("\n===== Rerank结果 =====")

    for result in results:
        print("原始位置：", result["index"])
        print("相关性分数：", result["relevance_score"])
        print("文档：", result["document"]["text"])
        print()


    top_n = results[:2]

    context = "\n".join(
        result["document"]["text"]
        for result in top_n
    )

    print("\n===== Context =====")
    print(context)


    print("\n===== Top-N结果 =====")

    for result in top_n:
        print("相关性分数：", result["relevance_score"])
        print("文档：", result["document"]["text"])
        print()

else:

    print("\n===== 调用失败 =====")
    print(response)


client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

response = client.chat.completions.create(
    model="deepseek-v4-flash-0731",
    messages=[
        {
            "role": "system",
            "content": """
            你是一个企业知识库问答助手。
            
            请严格根据提供的参考资料回答问题。
            
            如果参考资料中没有相关信息，请明确说明：
            资料中没有相关信息，无法确定。
            
            不要编造资料中没有的信息。
            """
        },
        {
            "role": "user",
            "content": f"""
            参考资料：
            {context}
            
            问题：
            {question}
            
            请根据参考资料回答问题。
            """
        }
    ]
)

answer = response.choices[0].message.content

print("\n===== AI回答 =====")
print(answer)