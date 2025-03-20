from sentence_transformers import SentenceTransformer
import numpy as np

# 加载模型
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# 读取文本文件
def load_text(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read().strip()  # 去除空行

# 按 200 字符拆分文本
def chunk_text(text, chunk_size=200):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

# 处理文本
file_path = "output.txt"  # 你的 TXT 文件
text = load_text(file_path)

if not text:
    raise ValueError("文本文件为空，请检查 output.txt 是否有内容！")

text_chunks = chunk_text(text)  # 分割文本
print(f"已拆分 {len(text_chunks)} 个文本块")

# 生成嵌入向量
embeddings = model.encode(text_chunks)

# 确保 embeddings 不为空
if embeddings is None or len(embeddings) == 0:
    raise ValueError("生成的 embeddings 为空，请检查输入文本！")

print(f"生成 {len(embeddings)} 个文本向量，每个向量维度 {embeddings.shape[1]}")

# 保存向量
np.save("text_embeddings.npy", embeddings)
print("已保存向量到 text_embeddings.npy")
