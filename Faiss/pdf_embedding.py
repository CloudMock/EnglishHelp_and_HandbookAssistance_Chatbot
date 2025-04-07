import os
import sys
import fitz  # PyMuPDF
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

def pdf_to_text(pdf_path):
    text = ""
    doc = fitz.open(pdf_path)
    for page in doc:
        text += page.get_text("text") + "\n"
    return text

def split_text(text, max_chunk_length=500):
    """
    简单分块：按段落或定长分段
    """
    paragraphs = text.split("\n")
    chunks = []
    chunk = ""
    for para in paragraphs:
        if len(chunk) + len(para) < max_chunk_length:
            chunk += para.strip() + " "
        else:
            chunks.append(chunk.strip())
            chunk = para.strip() + " "
    if chunk:
        chunks.append(chunk.strip())
    return chunks

def build_faiss_index(chunks, model):
    embeddings = model.encode(chunks)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings))
    return index, embeddings

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 pdf_embedding.py <pdf filename>")
        sys.exit(1)

    pdf_filename = sys.argv[1]
    pdf_path = os.path.join("PDF", pdf_filename)

    if not os.path.exists(pdf_path):
        print(f"Error: File {pdf_path} not found!")
        sys.exit(1)

    print(f"Converting {pdf_filename} to text...")
    text = pdf_to_text(pdf_path)

    chunks = split_text(text)
    print(f"Split into {len(chunks)} chunks.")

    print("Embedding chunks using sentence-transformers...")
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    index, _ = build_faiss_index(chunks, model)

    # 保存文本块
    os.makedirs("store", exist_ok=True)
    chunk_path = os.path.join("store", "text_chunks.txt")
    with open(chunk_path, "w", encoding="utf-8") as f:
        f.write("\n====\n".join(chunks))

    # 保存索引
    index_path = os.path.join("store", "student_handbook_faiss.index")
    faiss.write_index(index, index_path)

    print(f"\nAll done!")
    print(f"Text chunks saved to: {chunk_path}")
    print(f"FAISS index saved to: {index_path}")

if __name__ == "__main__":
    main()
