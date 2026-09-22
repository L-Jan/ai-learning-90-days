text = """
公司正式员工每年享有10天带薪年假。
员工出差产生的交通费可以申请报销。
公司工作日上班时间为上午9点到下午6点。
符合条件的订单可以在7天内申请退款。
员工入职满一年后可以享受更多公司福利。
"""

print(text)

chunk_size = 30
chunks = []

# for i in range(0,len(text),chunk_size):
#     chunk = text[i:i+chunk_size]
#     chunks.append(chunk)
overlap = 10
step = chunk_size - overlap
for i in range(0, len(text), step):
    chunk = text[i:i + chunk_size]
    chunks.append(chunk)

print("\n切分后的 Chunk：")
for i,chunk in enumerate(chunks):
    print(f"\nChunk {i + 1}:")
    print(chunk)