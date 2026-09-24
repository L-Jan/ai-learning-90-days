import os
import chromadb
import dashscope
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

#将文本转换为向量
def get_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-v4",
        input=text,
        dimensions=1024
    )

    embedding = response.data[0].embedding

    return embedding



chroma_client = chromadb.Client()

collection = chroma_client.create_collection(
    name="day21_rag_demo",
    embedding_function=None
)

documents = [
    "公司正式员工每年享有10天带薪年假。",
    "员工出差产生的交通费可以申请报销。",
    "公司工作日上班时间为上午9点到下午6点。",
    "符合条件的订单可以在7天内申请退款。",
    "员工入职满一年后可以享受更多公司福利。"
]

document_embeddings = []

for document in documents:
    embedding = get_embedding(document)
    document_embeddings.append(embedding)

collection.add(
    documents=documents,
    embeddings=document_embeddings,
    ids=[
        "doc1",
        "doc2",
        "doc3",
        "doc4",
        "doc5"
    ]
)

# 从 Chroma 中检索与用户问题相关的候选文档
def search_documents(query_embedding):
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=2
    )

    retrieved_documents = results["documents"][0]

    return retrieved_documents



# 使用 Rerank 模型重新判断候选文档与问题的相关性
def rerank_documents(question, documents):
    response = dashscope.TextReRank.call(
        model="qwen3-rerank",
        query=question,
        documents=documents,
        top_n=2,
        return_documents=True
    )

    results = response.output["results"]

    reranked_documents = []

    for result in results:
        reranked_documents.append(
            result["document"]["text"]
        )

    return reranked_documents



# 将用户问题和相关资料交给大模型生成最终回答
def generate_answer(question, documents):
    context = "\n".join(documents)

    prompt = f"""
            你是一个企业知识库问答助手。
            
            请严格根据下面提供的资料回答用户问题。
            
            如果资料中没有答案，请明确告诉用户：
            “资料中没有相关信息，无法确定。”
            
            资料：
            {context}
            
            用户问题：
            {question}
            """

    response = client.chat.completions.create(
        model="deepseek-v4-flash-0731",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    answer = response.choices[0].message.content

    return answer



# 将整个 RAG 流程封装起来
def rag_pipeline(question):
    # 第一步：把问题转换成向量
    query_embedding = get_embedding(question)

    # 第二步：向量检索
    retrieved_documents = search_documents(query_embedding)

    # 第三步：Rerank重新排序
    reranked_documents = rerank_documents(
        question,
        retrieved_documents
    )

    # 第四步：让大模型根据资料回答
    answer = generate_answer(
        question,
        reranked_documents
    )

    return answer


#测试代码
# question = "公司有什么福利？"
# query_embedding = get_embedding(question)
#
# retrieved_documents = search_documents(query_embedding)
# print("\n===== 检索结果 =====")
# for document in retrieved_documents:
#     print(document)
#
# reranked_documents = rerank_documents(
#     question,
#     retrieved_documents
# )
#
# print("\n===== Rerank结果 =====")
# for document in reranked_documents:
#     print(document)
#
# answer = generate_answer(
#     question,
#     reranked_documents
# )
#
# print("\n===== AI最终回答 =====")
# print(answer)

question = "公司有什么福利？"

answer = rag_pipeline(question)

print("\n===== AI最终回答 =====")
print(answer)