from markitdown import MarkItDown
import os
import datetime
import markdown2

pdf_dir = "pdf_samples"
output_dir = "outputs"
os.makedirs(output_dir, exist_ok=True)

md_converter = MarkItDown()

for filename in os.listdir(pdf_dir):
    if filename.endswith("pdf"):
        pdf_path = os.path.join(pdf_dir, filename)

        try:
            markdown_result = md_converter.convert(pdf_path)
            markdown_text = markdown_result.text_content

            html_content = markdown2.markdown(markdown_text, extras=["tables"])

            current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            html_filename = (
                f"markitdown_{current_time}_{os.path.splitext(filename)[0]}.html"
            )
            html_path = os.path.join(output_dir, html_filename)

            with open(html_path, "w", encoding="utf-8") as html_file:
                html_file.write(html_content)

            print(f"Extraction terminée pour {filename}. Fichier créé : {html_path}")
        except Exception as e:
            print(f"error for {filename}: {e}")
