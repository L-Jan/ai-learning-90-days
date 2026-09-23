from openai import OpenAI
from dotenv import load_dotenv
import chromadb
import os


# 读取 .env 文件
load_dotenv()


# 创建 AI 客户端
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)


# 创建 Chroma
chroma_client = chromadb.Client()

collection = chroma_client.create_collection(
    name="company_metadata_demo"
)


# 准备文档
documents = [
    "公司正式员工每年享有10天带薪年假。",
    "员工出差产生的交通费可以申请报销。",
    "公司工作日上班时间为上午9点到下午6点。"
]


# 准备 Metadata
metadatas = [
    {
        "source": "员工手册.pdf",
        "page": 12,
        "section": "休假制度"
    },
    {
        "source": "员工手册.pdf",
        "page": 25,
        "section": "报销制度"
    },
    {
        "source": "员工手册.pdf",
        "page": 8,
        "section": "工作制度"
    }
]


# 创建 Embedding
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


# 写入 Chroma
collection.add(
    documents=documents,
    embeddings=embeddings,
    metadatas=metadatas,
    ids=[
        "doc1",
        "doc2",
        "doc3"
    ]
)


print("数据写入成功！")


# 查询问题
question = "公司一年有多少天年假？"


# 将问题转换成向量
question_response = client.embeddings.create(
    model="text-embedding-v4",
    input=question,
    dimensions=1024
)

query_embedding = question_response.data[0].embedding


# 从 Chroma 检索
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=1,
    # where={
    #     "source": "员工手册.pdf"
    # }
    where={
        "$and": [
            {
                "source": "员工手册.pdf"
            },
            {
                "section": "休假制度"
            }
        ]
    }
)


# 获取检索到的文档
retrieved_document = results["documents"][0][0]

# 获取检索到的 Metadata
retrieved_metadata = results["metadatas"][0][0]


# print("\n检索到的内容：")
# print(retrieved_document)
#
# print("\n对应的 Metadata：")
# print(retrieved_metadata)

print("\n===== 检索结果 =====")

print("回答依据：")
print(retrieved_document)

print("\n来源信息：")
print("文件：", retrieved_metadata["source"])
print("页码：", retrieved_metadata["page"])
print("章节：", retrieved_metadata["section"])