from openai import OpenAI
from dotenv import load_dotenv
import chromadb
import os


# 加载 .env
load_dotenv()


# 创建百炼客户端
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)


# 创建 Chroma 客户端
chroma_client = chromadb.Client()


# 创建一个集合
collection = chroma_client.create_collection(
    name="company_documents"
)


# 公司资料
documents = [
    "公司正式员工每年享有10天带薪年假。",
    "员工出差产生的交通费可以申请报销。",
    "公司工作日上班时间为上午9点到下午6点。"
]


# 使用百炼 Embedding 模型生成向量
response = client.embeddings.create(
    model="text-embedding-v4",
    input=documents,
    dimensions=1024
)


# 获取向量
embeddings = [
    item.embedding
    for item in response.data
]


# 把资料和向量存入 Chroma
collection.add(
    documents=documents,
    embeddings=embeddings,
    ids=[
        "doc1",
        "doc2",
        "doc3"
    ]
)


# 用户问题
question = "公司几点上班？"


# 把用户问题转换成向量
question_response = client.embeddings.create(
    model="text-embedding-v4",
    input=question,
    dimensions=1024
)


query_embedding = question_response.data[0].embedding


# 使用问题向量搜索 Chroma
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=2
)


print("用户问题：")
print(question)

print("\n搜索结果：")
print(results["documents"])


# 获取检索到的资料
retrieved_documents = results["documents"][0]

# 把多条资料合并成一段文字
context = "\n".join(retrieved_documents)

# 让大模型根据检索到的资料回答
answer_response = client.chat.completions.create(
    model="deepseek-v4-flash-0731",
    messages=[
        {
            "role": "system",
            "content": "你是一个企业知识库问答助手。请严格根据提供的资料回答问题。如果资料中没有答案，就说资料中没有相关信息。"
        },
        {
            "role": "user",
            "content": f"""
            请根据以下公司资料回答问题。
            
            公司资料：
            {context}
            
            用户问题：
            {question}
            """
        }
    ]
)

answer = answer_response.choices[0].message.content

print("\nAI最终回答：")
print(answer)