import fitz  # PyMuPDF
import sys
import os

def pdf_to_txt(pdf_path):
    text = ""
    doc = fitz.open(pdf_path)  # Open PDF file
    for page in doc:
        text += page.get_text("text") + "\n"  # Extract text content
    return text

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("python3 pdf_to_txt.py <pdf file name>")
        sys.exit(1)
    
    # example
    pdf_filename = sys.argv[1]  # Replace with your PDF file path
    pdf_path = os.path.join("PDF", pdf_filename)

    if not os.path.exists(pdf_path):
        print(f"Error: file{pdf_path} not exists!")
        sys.exit(1)

    pdf_text = pdf_to_txt(pdf_path)

    output_filename = os.path.splitext(pdf_filename)[0] + ".txt"  # 修改后缀
    output_path = os.path.join("PDF", output_filename)  # 输出文件路径

    # Save to text file
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(pdf_text)
        print(f"PDF to text conversion completed! Results saved in {output_path}")
    except Exception as e:
        print(f"Error: Cannot write in {output_path}: {e}")
        sys.exit(1)
