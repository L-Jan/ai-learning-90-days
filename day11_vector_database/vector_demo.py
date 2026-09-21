import chromadb

# 创建一个 Chroma 客户端，打开一个向量数据库
client = chromadb.Client()

# 创建一个集合，创建一个资料库
collection = client.create_collection(
    name="company_documents"
)

# 添加公司资料
collection.add(
    documents=[
        "公司正式员工每年享有10天带薪年假。",
        "员工出差产生的交通费可以申请报销。",
        "公司工作日上班时间为上午9点到下午6点。"
    ],
    ids=[
        "doc1",
        "doc2",
        "doc3"
    ]
)

# 搜索相关资料
results = collection.query(
    query_texts=["公司一年有多少天年假？"],
    n_results=2
)

print("搜索结果：")
print(results)