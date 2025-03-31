from sentence_transformers import SentenceTransformer
import numpy as np
import faiss

# 加载模型
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# 读取文本文件
def load_text(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read().strip()

# 按 1000 字符拆分文本
def chunk_text(text, chunk_size=1000):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

# 处理文本
file_path = "output.txt"  # 你的 TXT 文件
text = load_text(file_path)

if not text:
    raise ValueError("文本文件为空，请检查 output.txt 是否有内容！")

text_chunks = chunk_text(text)  # 分割文本

# 生成嵌入向量
embeddings = model.encode(text_chunks)

# 确保 embeddings 不为空
if embeddings is None or len(embeddings) == 0:
    raise ValueError("生成的 embeddings 为空，请检查输入文本！")

# 保存向量 & 文本
np.save("text_embeddings.npy", embeddings)
with open("text_chunks.txt", "w", encoding="utf-8") as f:
    for chunk in text_chunks:
        f.write(chunk + "\n====\n")  # 每个文本块用 "====" 分隔，方便读取

# 初始化 FAISS 索引
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# 保存 FAISS 索引
faiss.write_index(index, "faiss.index")

print("✅ FAISS 索引构建完成，数据已保存！")
