from openai import OpenAI
from dotenv import load_dotenv
import chromadb
import os


load_dotenv()

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

chroma_client = chromadb.Client()
collection = chroma_client.create_collection(
    name="top_k_demo"
)

documents = [
    "公司正式员工每年享有10天带薪年假。",
    "员工出差产生的交通费可以申请报销。",
    "公司工作日上班时间为上午9点到下午6点。",
    "符合条件的订单可以在7天内申请退款。",
    "员工入职满一年后可以享受更多公司福利。"
]

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

results = collection.query(
    query_texts=["公司员工有什么福利？"],
    n_results=1
)
retrieved_documents = results["documents"][0]
context = "\n".join(retrieved_documents)
print("\nContext：")
print(context)

# print("检索结果：")
# for document in results["documents"][0]:
#     print(document)

response = client.chat.completions.create(
    model="deepseek-v4-flash-0731",
    messages=[
        {
            "role": "system",
            "content": "请严格根据提供的参考资料回答问题，不要编造资料中没有的信息。"
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

print("\nAI回答：")
print(answer)