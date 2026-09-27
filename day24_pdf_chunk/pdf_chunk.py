import os
import chromadb
from pypdf import PdfReader
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

chroma_client = chromadb.Client()

collection = chroma_client.create_collection(
    name="day24_pdf_chunks"
)


def load_pdf(file_path):
    # 打开 PDF 文件
    reader = PdfReader(file_path)

    # 保存所有页面文字
    all_text = ""

    # 遍历所有页面
    for page in reader.pages:
        text = page.extract_text()
        all_text += text + "\n"

    return all_text

text = load_pdf("../day23_pdf_loader/company.pdf")
print("===== PDF 内容 =====")
print(text)



def split_text(text, chunk_size=50, overlap=0):
    # 按换行符切分文本
    paragraphs = text.split("\n")

    # 保存最终的 Chunk
    chunks = []

    # 保存当前 Chunk
    current_chunk = ""

    for paragraph in paragraphs:
        paragraph = paragraph.strip()

        if not paragraph:
            continue

        # 当前 Chunk 没超过长度，就继续添加
        if len(current_chunk) + len(paragraph) <= chunk_size:
            current_chunk += paragraph

        else:
            # 保存当前 Chunk
            chunks.append(current_chunk)

            # 保留当前 Chunk 最后的部分
            if overlap > 0:
                current_chunk = current_chunk[-overlap:] + paragraph
            else:
                current_chunk = paragraph

    # 保存最后一个 Chunk
    if current_chunk:
        chunks.append(current_chunk)

    return chunks

chunks = split_text(text)
print("Chunk 数量：", len(chunks))
print("===== Chunk =====")
for i, chunk in enumerate(chunks):
    print(f"Chunk {i + 1}：")
    print(chunk)
    print("长度：", len(chunk))
    print("--------------------")


#把 3 个 Chunk 全部转换成向量
document_embeddings = []
for chunk in chunks:
    response = client.embeddings.create(
        model="text-embedding-v4",
        input=chunk,
        dimensions=1024
    )
    embedding = response.data[0].embedding
    document_embeddings.append(embedding)
print("===== Embedding =====")
print("Chunk 数量：", len(chunks))
print("向量数量：", len(document_embeddings))
print("第一个向量维度：", len(document_embeddings[0]))


# 把 Chunk 和向量放进 Chroma
ids = []
for i in range(len(chunks)):
    ids.append(f"chunk{i + 1}")
metadatas = []
for i in range(len(chunks)):
    metadatas.append({
        "file_name":"company.pdf",
        "chunk_index":i+1
    })
collection.add(
    ids=ids,
    documents=chunks,
    embeddings=document_embeddings,
    metadatas=metadatas
)
print("===== Chroma =====")
print("Chunk 数量：", collection.count())


# 让用户的问题变成向量
question = "公司有什么福利？"
question_response = client.embeddings.create(
    model="text-embedding-v4",
    input=question,
    dimensions=1024
)
query_embedding = question_response.data[0].embedding
print("===== 问题 Embedding =====")
print("问题：", question)
print("向量维度：", len(query_embedding))


# 用问题向量去 Chroma 检索最相关的 Chunk
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=2
)
print("===== 检索结果 =====")
documents = results["documents"][0]
distances = results["distances"][0]
metadatas = results["metadatas"][0]
for i in range(len(documents)):
    print(f"Top {i + 1}")
    print("Chunk：", documents[i])
    print("距离：", distances[i])
    print("来源：", metadatas[i]["file_name"])
    print("Chunk 编号：", metadatas[i]["chunk_index"])
    print("--------------------")


# 让 AI 根据资料回答问题
# context = "\n".join(documents)
context = ""
for i in range(len(documents)):
    context += f"""
    来源：{metadatas[i]["file_name"]}
    Chunk：{metadatas[i]["chunk_index"]}
    内容：{documents[i]}
    """
print("===== Context =====")
print(context)
prompt = f"""
你是一个企业知识库问答助手。

请严格根据下面的资料回答用户的问题。

回答时请在答案最后注明参考来源。
格式：
参考来源：文件名 + Chunk 编号

如果资料中没有答案，请明确告诉用户：
“资料中没有相关信息，无法确定。”

资料：
{context}

用户问题：
{question}
"""
print("===== Prompt =====")
print(prompt)
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
print("===== AI 回答 =====")
print(answer)


