from openai import OpenAI
from dotenv import load_dotenv
import chromadb
import os


# 1. 加载环境变量

load_dotenv()


# 2. 创建 AI 客户端

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)


# 3. 创建 Chroma

chroma_client = chromadb.Client()

collection = chroma_client.create_collection(
    name="day18_similarity_demo"
)


# 4. 准备知识库

documents = [
    "公司正式员工每年享有10天带薪年假。",
    "员工出差产生的交通费可以申请报销。",
    "公司工作日上班时间为上午9点到下午6点。",
    "符合条件的订单可以在7天内申请退款。",
    "员工入职满一年后可以享受更多公司福利。"
]


# 5. 将资料写入 Chroma

collection.add(
    documents=documents,
    ids=[
        "doc1",
        "doc2",
        "doc3",
        "doc4",
        "doc5"
    ]
)


# 6. 用户问题

question = "公司员工有什么福利？"


# 7. 使用 Chroma 检索

results = collection.query(
    query_texts=[question],
    n_results=3,
    include=["documents", "distances"]
)


# 8. 获取检索结果和距离

documents = results["documents"][0]
distances = results["distances"][0]


print("===== 原始检索结果 =====")

for document, distance in zip(documents, distances):
    print("距离：", distance)
    print("内容：", document)
    print()


# 9. 设置距离阈值

threshold = 0.20


# 10. 根据距离过滤资料

filtered_documents = []

for document, distance in zip(documents, distances):

    if distance <= threshold:
        filtered_documents.append(document)


# 11. 查看过滤后的资料

print("===== 过滤后的资料 =====")

for document in filtered_documents:
    print(document)


# 12. 将过滤后的资料合并成 Context

context = "\n".join(filtered_documents)


print("\n===== Context =====")
print(context)


# 13. 将 Context 交给大模型

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


# 14. 获取 AI 最终回答

answer = response.choices[0].message.content


# 15. 输出最终答案

print("\n===== AI回答 =====")
print(answer)