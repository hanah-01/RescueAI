import fitz 
import os

PDF_FOLDER = "data"

for file in os.listdir(PDF_FOLDER):
    if file.lower().endswith(".pdf"):
        pdf_path = os.path.join(PDF_FOLDER, file)

        doc = fitz.open(pdf_path)
        text = ""

        for page in doc:
            text += page.get_text()

        txt_path = os.path.join(
            PDF_FOLDER,
            file.replace(".pdf", ".txt")
        )

        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(text)

        print(f"Created {txt_path}")