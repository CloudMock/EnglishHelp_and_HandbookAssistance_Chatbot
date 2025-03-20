from sentence_transformers import SentenceTransformer
# 加载模型
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


# 测试句子
sentences = ["Hello, how are you?", "This is an example sentence.", "FAISS is great for similarity search."]
embeddings = model.encode(sentences)

print(embeddings.shape)  # 输出: (3, 384)，表示3个句子，每个向量是 384 维
print(embeddings[0][:10])  # 打印第一个句子的前10个数值
