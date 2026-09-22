from openai import OpenAI
from dotenv import load_dotenv
import chromadb
import os


# 加载环境变量
load_dotenv()


# 创建 AI 客户端
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)


# 创建 Chroma 客户端
chroma_client = chromadb.Client()


# 创建知识库
collection = chroma_client.create_collection(
    name="company_documents"
)


# 公司资料
documents = [
    "公司正式员工每年享有10天带薪年假。",
    "员工出差产生的交通费可以申请报销。",
    "公司工作日上班时间为上午9点到下午6点。",
    "符合条件的订单可以在7天内申请退款。",
    "员工入职满一年后可以享受更多公司福利。"
]


# 生成文档 Embedding
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


# 把文档和向量存入 Chroma
collection.add(
    documents=documents,
    embeddings=embeddings,
    ids=[
        "doc1",
        "doc2",
        "doc3",
        "doc4",
        "doc5"
    ]
)


print("===== 企业知识库助手 =====")
print("输入“退出”可以结束程序。")


while True:

    question = input("\n请输入问题：")

    if question == "退出":
        break

    # 将用户问题转换成向量
    question_response = client.embeddings.create(
        model="text-embedding-v4",
        input=question,
        dimensions=1024
    )

    query_embedding = question_response.data[0].embedding

    # 从向量数据库检索
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=2
    )

    # 获取检索结果
    retrieved_documents = results["documents"][0]

    # 将多条资料合并
    context = "\n".join(retrieved_documents)

    # 让 AI 根据资料回答
    answer_response = client.chat.completions.create(
        model="deepseek-v4-flash-0731",
        messages=[
            {
                "role": "system",
                "content": """
                你是一个企业知识库问答助手。
                
                请严格根据提供的公司资料回答问题。
                
                如果资料中没有相关答案，
                请明确告诉用户“资料中没有相关信息”，
                不要自行编造答案。
                """
            },
            {
                "role": "user",
                "content": f"""
                公司资料：
                
                {context}
                
                用户问题：
                
                {question}
                """
            }
        ]
    )

    answer = answer_response.choices[0].message.content

    print("\nAI回答：")
    print(answer)

    print("\n参考资料：")
    for document in retrieved_documents:
        print("-", document)