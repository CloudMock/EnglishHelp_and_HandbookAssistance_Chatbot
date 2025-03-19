import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    text = ""
    doc = fitz.open(pdf_path)  # Open PDF file
    for page in doc:
        text += page.get_text("text") + "\n"  # Extract text content
    return text

# example
pdf_path = "example.pdf"  # Replace with your PDF file path
pdf_text = extract_text_from_pdf(pdf_path)

# Save to text file
with open("output.txt", "w", encoding="utf-8") as f:
    f.write(pdf_text)

print("PDF 转文本完成！结果保存在 output.txt")

