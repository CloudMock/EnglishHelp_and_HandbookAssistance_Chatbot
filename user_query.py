from sentence_transformers import SentenceTransformer
import numpy as np
import faiss

# 加载模型 & FAISS 索引
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
index = faiss.read_index("faiss.index")

# 读取文本块
with open("text_chunks.txt", "r", encoding="utf-8") as f:
    text_chunks = f.read().split("\n====\n")  # 按 "====" 进行分割

# 用户输入查询
query_text = input("请输入查询文本：")
query_vector = model.encode([query_text])

# FAISS 搜索
k = 3  # 返回最相似的 3 个文本块
distances, indices = index.search(query_vector, k)

# 输出查询结果
print("\n🔍 查询结果：")
for i, idx in enumerate(indices[0]):
    print(f"\n相似度排名 {i+1}：")
    print(text_chunks[idx])
    print(f"🔹 相似度（L2 距离）：{distances[0][i]}")
    print("-" * 40)
