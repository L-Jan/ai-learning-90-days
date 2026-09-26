import os
import chromadb

# 读取一个文件的内容
def load_document(file_path):

    # 以 UTF-8 编码读取文件
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    return text


# 读取文件夹中的所有 TXT 文件
def load_documents(folder_path):

    # 保存所有文档
    documents = []

    # 获取文件夹中的所有文件
    files = os.listdir(folder_path)

    # 遍历文件
    for file in files:

        # 只处理 TXT 文件
        if file.endswith(".txt"):

            # 拼接完整文件路径
            file_path = os.path.join(folder_path, file)

            # 读取文件内容
            text = load_document(file_path)

            documents.append({
                "id": f"doc{len(documents) + 1}",
                "text": text,
                "metadata": {
                    "file_name": file
                }
            })

    return documents


# 获取当前 Python 文件所在的文件夹
folder_path = os.path.dirname(__file__)


# 读取文件夹中的所有 TXT 文档
documents = load_documents(folder_path)


# 打印读取结果
print("\n===== 所有文档 =====")

for document in documents:
    print("ID：", document["id"])
    print("内容：", document["text"])
    print("来源：", document["metadata"]["file_name"])
    print("--------------------")

print("\n文档数量：", len(documents))

# 分别保存文本、元数据和 ID
ids = []
texts = []
metadatas = []
for document in documents:
    ids.append(document["id"])
    texts.append(document["text"]),
    metadatas.append(document["metadata"])

print("\n===== 整理后的数据 =====")
print("IDs：", ids)
print("Texts：", texts)
print("Metadatas：", metadatas)

# 查看三个列表是否一一对应
for i in range(len(documents)):
    print("\n===== 文档", i + 1, "=====")
    print("ID：", ids[i])
    print("内容：", texts[i])
    print("来源：", metadatas[i]["file_name"])


chroma_client = chromadb.Client()
collection = chroma_client.create_collection(
    name="day22_documents"
)
print("\nChroma 集合创建成功")

# 把所有文档添加到 Chroma
collection.add(
    ids=ids,
    documents=texts,
    metadatas=metadatas
)
print("\n所有文档添加成功")

# 查看 Chroma 中有多少个文档
print("\nChroma 文档数量：", collection.count())

# 查询公司福利相关的文档
results = collection.query(
    query_texts=["公司有什么福利？"],
    n_results=2
)
print("\n===== 搜索结果 =====")
print("文档：", results["documents"])
print("来源：", results["metadatas"])

# 取出第一个搜索到的文档
document = results["documents"][0][0]
# 取出第一个文档的来源
metadata = results["metadatas"][0][0]
print("\n===== 第一个搜索结果 =====")
print("内容：", document)
print("来源：", metadata["file_name"])

search_result = {
    "text":results["documents"][0][0],
    "source":results["metadatas"][0][0]["file_name"]
}
print("\n===== 整理后的搜索结果 =====")
print(search_result)
