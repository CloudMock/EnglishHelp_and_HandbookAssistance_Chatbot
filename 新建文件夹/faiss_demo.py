from sentence_transformers import SentenceTransformer
import numpy as np
import faiss 
# 加载模型
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
# 读取文本文件
def load_text(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read().strip()  # 去除空行

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

# 保存向量
np.save("text_embeddings.npy", embeddings)

# 初始化 FAISS 索引（L2 距离）
dimension = embeddings.shape[1]  # 向量维度
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)  # 添加向量到索引

# 保存 FAISS 索引
faiss.write_index(index, "faiss.index")


# 查询示例
query_text = input("请输入：")  # 你要查询的句子
query_vector = model.encode([query_text])

# 执行搜索
k = 3  # 返回最相似的 3 个文本块
distances, indices = index.search(query_vector, k)

# 打印查询结果
print("\n查询结果：")
for i, idx in enumerate(indices[0]):
    print(f"相似度排名 {i+1}：")
    print(text_chunks[idx])
    print("-" * 40)
