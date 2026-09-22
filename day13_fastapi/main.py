from fastapi import FastAPI
from openai import OpenAI
from dotenv import load_dotenv
import chromadb
import os


load_dotenv()

app = FastAPI()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

chroma_client = chromadb.Client()
collection = chroma_client.create_collection(
    name="company_documents"
)

documents = [
    "公司正式员工每年享有10天带薪年假。",
    "员工出差产生的交通费可以申请报销。",
    "公司工作日上班时间为上午9点到下午6点。",
    "符合条件的订单可以在7天内申请退款。",
    "员工入职满一年后可以享受更多公司福利。"
]

response = client.embeddings.create(
    model="text-embedding-v4",
    input=documents,
    dimensions=1024
)

embeddings = [
    item.embedding
    for item in response.data
]

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

@app.get("/")
async def root():
    return {"message": "我的第一个AI应用"}


@app.get("/ask")
async def ask(question: str):
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

    context = "\n".join(retrieved_documents)

    print("检索到的资料：")
    print(context)

    response = client.chat.completions.create(
        model="deepseek-v4-flash-0731",
        messages=[
            {
                "role": "system",
                "content": """
                你是一个企业内部知识库问答助手。
            
                请严格根据提供的参考资料回答问题。
            
                如果参考资料中没有相关信息，请明确回答：
                资料中没有相关信息，无法确定。
            
                不要根据自己的常识编造答案。
                """
            },
            {
                "role": "user",
                "content": f"""
                参考资料：
                {context}
            
                用户问题：
                {question}
            
                请根据参考资料回答用户问题。
                """
            }
        ]
    )

    answer = response.choices[0].message.content

    return {
        "问题": question,
        "回答": answer
    }