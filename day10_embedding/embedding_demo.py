from openai import OpenAI
from dotenv import load_dotenv
import os
import math

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

texts = [
    "公司年假有多少天？",
    "一年可以休多少带薪假？",
    "公司几点开始上班？"
]

response = client.embeddings.create(
    model="text-embedding-v4",
    input=texts
)

embeddings = [item.embedding for item in response.data]


def cosine_similarity(a, b):
    dot_product = sum(x * y for x, y in zip(a, b))

    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))

    return dot_product / (norm_a * norm_b)


similarity_ab = cosine_similarity(embeddings[0], embeddings[1])
similarity_ac = cosine_similarity(embeddings[0], embeddings[2])

print("A：", texts[0])
print("B：", texts[1])
print("A和B的相似度：", similarity_ab)

print()

print("A：", texts[0])
print("C：", texts[2])
print("A和C的相似度：", similarity_ac)