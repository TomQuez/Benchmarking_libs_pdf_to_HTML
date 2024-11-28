import os
import markdown2
from loguru import logger
from magic_pdf.data.data_reader_writer import FileBasedDataWriter, FileBasedDataReader
from magic_pdf.config.make_content_config import DropMode, MakeMode
from magic_pdf.pipe.OCRPipe import OCRPipe
from magic_pdf.pipe.UNIPipe import UNIPipe

current_dir = os.path.dirname(os.path.realpath(__file__))
pdf_samples = os.path.join(current_dir, "../pdf_samples")
output_dir = os.path.join(current_dir, "../outputs")

os.makedirs(output_dir, exist_ok=True)

try:
    pdf_files = [f for f in os.listdir(pdf_samples) if f.endswith(".pdf")]
    for pdf_file in pdf_files:
        try:
            logger.info(f"Start extraction for {pdf_file}")
            pdf_path = os.path.join(pdf_samples, pdf_file)

            reader = FileBasedDataReader("")
            pdf_bytes = reader.read(pdf_path)

            local_image_dir = os.path.join(
                output_dir, f"{os.path.splitext(pdf_file)[0]}_images"
            )
            image_writer = FileBasedDataWriter(local_image_dir)
            try:
                pipe = UNIPipe(
                    pdf_bytes,
                    {"_pdf_type": "", "model_list": []},
                    image_writer=image_writer,
                    is_debug=True,
                )
                pipe.pipe_classify()
                pipe.pipe_analyze()
                pipe.pipe_parse()
                logger.info(f"UNIPipe done for {pdf_file}")
            except Exception as uni_error:
                logger.warning(f"UNIPipe failed for {pdf_file}. Error: {uni_error}")
                pipe = OCRPipe(
                    pdf_bytes,
                    {"_pdf_type": "", "model_list": []},
                    image_writer=image_writer,
                    is_debug=True,
                )
                pipe.pipe_classify()
                pipe.pipe_analyze()
                pipe.pipe_parse()
                logger.info(f"OCRPipe done for {pdf_file}")

            md_content = pipe.pipe_mk_markdown(
                local_image_dir, drop_mode=DropMode.NONE, md_make_mode=MakeMode.MM_MD
            )
            html_content = markdown2.markdown(md_content)
            output_html_path = os.path.join(
                output_dir, f"{os.path.splitext(pdf_file)[0]}.html"
            )
            with open(output_html_path, "w", encoding="utf-8") as f:
                f.write(html_content)

            print(f"extraction done for {pdf_file}. Output is {output_html_path}")
        except Exception as e:
            logger.exception(f"Error during extraction for file {pdf_file}: {e}")
            raise e
except Exception as e:
    logger.exception(f"Error during extraction: {e}")
    raise e
