from openai import OpenAI
from dotenv import load_dotenv
import os


load_dotenv()

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)


documents = [
    "公司正式员工每年享有10天带薪年假。",
    "员工入职满一年后可以享受更多公司福利。",
    "员工出差产生的交通费可以申请报销。",
    "公司工作日上班时间为上午9点到下午6点。"
]

scores = [
    0.95,
    0.88,
    0.60,
    0.20
]


# 把文档和分数绑定
document_scores = list(zip(documents, scores))

print("绑定后的数据：")

for document, score in document_scores:
    print(score, document)


# 按照分数从高到低排序
reranked_results = sorted(
    document_scores,
    key=lambda x: x[1], #按照每条数据的第 2 个元素(分数)来排序
    reverse=True
)

print("\nRerank 后的结果：")

for document, score in reranked_results:
    print("分数：", score)
    print("内容：", document)
    print()


top_n = reranked_results[:2]    #从第一个开始，取前2个

print("\n===== Rerank 后 Top-N =====")

for document, score in top_n:
    print("分数：", score)
    print("内容：", document)
    print()


context = "\n".join(
    document
    for document, score in top_n
)

print("\n===== Context =====")
print(context)


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
            公司员工有什么福利？
            
            请根据参考资料回答问题。
            """
        }
    ]
)

answer = response.choices[0].message.content

print("\n===== AI回答 =====")
print(answer)