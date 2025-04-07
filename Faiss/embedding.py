from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import sys
import os

# load model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# read txt file
def load_text(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read().strip()

# split text into chunks of 1000 char
def chunk_text(text, chunk_size=1000):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

# Get the input file from command-line arguments
if len(sys.argv) < 2:
    print("Error: Please provide a text file as an argument.")
    print("Usage: python script.py input.txt")
    sys.exit(1)

file_path = sys.argv[1]

# Convert relative path to absolute path
file_path = os.path.abspath(file_path)

# Check if file exists
if not os.path.exists(file_path):
    print(f"Error: File '{file_path}' does not exist.")
    sys.exit(1)

text = load_text(file_path)

if not text:
    raise ValueError("Text file is empty. Please check if the input file contains any content!")

text_chunks = chunk_text(text)  # Split text into chunks

# Generate embeddings
embeddings = model.encode(text_chunks)

# Ensure embeddings are not empty
if embeddings is None or len(embeddings) == 0:
    raise ValueError("Generated embeddings are empty. Please check the input text!")

# Get the current script directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Ensure the 'store' directory exists
store_dir = os.path.join(script_dir, "store")
if not os.path.exists(store_dir):
    os.makedirs(store_dir)

# Save embeddings & text in the store directory
output_name = os.path.splitext(os.path.basename(file_path))[0]  # Use base name of input file
np.save(os.path.join(store_dir, f"{output_name}_embeddings.npy"), embeddings)
with open(os.path.join(store_dir, "text_chunks.txt"), "w", encoding="utf-8") as f:
    for chunk in text_chunks:
        f.write(chunk + "\n====\n")  # Separate text chunks with "====" for readability

# Initialize FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# Save FAISS index in the store directory
faiss.write_index(index, os.path.join(store_dir, f"{output_name}_faiss.index"))

print(f"FAISS index has been built and saved successfully!\nOutput files: {output_name}_embeddings.npy, text_chunks.txt, {output_name}_faiss.index")
