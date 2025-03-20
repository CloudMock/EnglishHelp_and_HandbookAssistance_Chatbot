def chunk_text(text, chunk_size=200):
    """按 chunk_size 分割文本，每段 200 个字符"""
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

# 读取 PDF 提取的文本
with open("output.txt", "r", encoding="utf-8") as f:
    pdf_text = f.read()

# 分割文本
text_chunks = chunk_text(pdf_text)

# 生成嵌入向量
embeddings = model.encode(text_chunks)

print(f"生成 {len(embeddings)} 个文本向量，每个向量维度为 {embeddings.shape[1]}")
