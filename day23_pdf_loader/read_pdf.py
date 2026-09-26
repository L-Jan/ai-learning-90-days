from pypdf import PdfReader
import os
import chromadb


def load_pdf(file_path):
    # 打开 PDF 文件
    reader = PdfReader(file_path)

    # 保存所有页面的文字
    all_text = ""

    # 遍历 PDF 的所有页面
    # for page in reader.pages:
    #     text = page.extract_text()
    #     all_text += text + "\n"

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text()

        all_text += f"\n--- 第 {page_number} 页 ---\n"
        all_text += text + "\n"

    return all_text


def load_pdfs(folder_path):
    documents = []

    # 获取文件夹中的所有文件
    files = os.listdir(folder_path)

    # 遍历文件
    for file in files:
        if file.endswith(".pdf"):
            file_path = os.path.join(folder_path, file)
            text = load_pdf(file_path)
            documents.append({
                "id": f"doc{len(documents) + 1}",
                "text": text,
                "metadata": {
                    "file_name": file
                }
            })

    return documents



# text = load_pdf("company.pdf")
# print("===== PDF 全部内容 =====")
# print(text)


folder_path = os.path.dirname(__file__)
documents = load_pdfs(folder_path)
print("===== PDF 文档 =====")
for document in documents:
    print("ID：", document["id"])
    print("内容：", document["text"])
    print("来源：", document["metadata"]["file_name"])
    print("--------------------")


chroma_client = chromadb.Client()
collection = chroma_client.create_collection(
    name="day23_pdf_documents"
)
ids = []
texts = []
metadatas = []
for document in documents:
    ids.append(document["id"])
    texts.append(document["text"])
    metadatas.append(document["metadata"])
collection.add(
    ids=ids,
    documents=texts,
    metadatas=metadatas
)
print("===== Chroma =====")
print("文档数量：", collection.count())

# 搜索与问题相关的文档
results = collection.query(
    query_texts=["公司主要销售什么产品？"],
    n_results=1
)
print("===== 搜索结果 =====")
print("文档：", results["documents"])
print("来源：", results["metadatas"])

# 获取第一个搜索结果
document = results["documents"][0][0]
metadata = results["metadatas"][0][0]
print("===== 第一个搜索结果 =====")
print("内容：", document)
print("来源：", metadata["file_name"])

# 整理搜索结果
search_result = {
    "text": document,
    "source": metadata["file_name"]
}
print("===== 整理后的搜索结果 =====")
print(search_result)