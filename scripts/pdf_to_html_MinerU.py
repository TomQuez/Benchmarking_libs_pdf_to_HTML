import os
import markdown2
from loguru import logger
from magic_pdf.data.data_reader_writer import FileBasedDataWriter
from magic_pdf.pipe.UNIPipe import UNIPipe

current_dir = os.path.dirname(os.path.realpath(__file__))
pdf_samples = os.path.join(current_dir, "../pdf_samples")
output_dir = os.path.join(current_dir, "../outputs")

os.makedirs(output_dir, exist_ok=True)

try:
    pdf_files = [f for f in os.listdir(pdf_samples) if f.endswith(".pdf")]
    for pdf_file in pdf_files:
        pdf_path = os.path.join(pdf_samples, pdf_file)
        pdf_bytes = open(pdf_path, "rb").read()

        jso_useful_key = {"_pdf_type": "", "model_list": []}
        local_image_dir = os.path.join(
            output_dir, f"{os.path.splitext(pdf_file)[0]}_images"
        )
        image_writer = FileBasedDataWriter(local_image_dir)

        pipe = UNIPipe(pdf_bytes, jso_useful_key, image_writer)
        pipe.pipe_classify()
        pipe.pipe_analyze()
        pipe.pipe_parse()

        md_content = pipe.pipe_mk_markdown(local_image_dir, drop_mode="none")
        html_content = markdown2.markdown(md_content)
        output_html_path = os.path.join(
            output_dir, f"{os.path.splitext(pdf_file)[0]}.html"
        )
        with open(output_html_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        print(f"extraction done for {pdf_file}. Output is {output_html_path}")
except Exception as e:
    logger.exception(f"Error during extraction: {e}")
    raise e
