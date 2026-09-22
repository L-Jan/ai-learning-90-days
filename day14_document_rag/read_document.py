from openai import OpenAI
from dotenv import load_dotenv
import chromadb
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

file = open("company.txt", "r", encoding="utf-8")
content = file.read()
file.close()

chunks = content.split("\n")
response = client.embeddings.create(
    model="text-embedding-v4",
    input=chunks,
    dimensions=1024
)
embeddings = [
    item.embedding
    for item in response.data
]

# 把这些 Embedding 存进 Chroma
chroma_client = chromadb.Client()
collection = chroma_client.create_collection(
    name="company_documents_day14"
)
collection.add(
    documents=chunks,
    embeddings=embeddings,
    ids=[
        "doc1",
        "doc2",
        "doc3",
        "doc4",
        "doc5"
    ]
)

print("Chunk数量：")
print(len(chunks))

print("\nEmbedding数量：")
print(len(embeddings))

print("\n第一个Chunk：")
print(chunks[0])

print("\n第一个Chunk的向量长度：")
print(len(embeddings[0]))


# 测试 Chroma 检索
question = "公司一年有多少天年假？"
question_response = client.embeddings.create(
    model="text-embedding-v4",
    input=question,
    dimensions=1024
)
query_embedding = question_response.data[0].embedding
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=2
)
retrieved_documents = results["documents"][0]

print("\n检索结果：")
for document in retrieved_documents:
    print(document)


# 接入 DeepSeek
context = "\n".join(retrieved_documents)
response = client.chat.completions.create(
    model="deepseek-v4-flash-0731",
    messages=[
        {
            "role":"system",
            "content":"请严格根据参考资料回答问题，不要编造资料中没有的信息。"
        },
        {
            "role":"user",
            "content":f"""
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

print("\nAI回答：")
print(answer)

