import os
import markdown2
from loguru import logger
from magic_pdf.data.data_reader_writer import FileBasedDataWriter, FileBasedDataReader
from magic_pdf.config.make_content_config import DropMode, MakeMode
from magic_pdf.pipe.OCRPipe import OCRPipe
from magic_pdf.pipe.UNIPipe import UNIPipe

# Define directories for input and output
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

            # Read the PDF content as bytes
            reader = FileBasedDataReader("")
            pdf_bytes = reader.read(pdf_path)

            # Define directory for storing images generated during the process

            local_image_dir = os.path.join(
                output_dir, f"MinerU_{os.path.splitext(pdf_file)[0]}_images"
            )
            image_writer = FileBasedDataWriter(local_image_dir)

            # Attempt extraction using UNIPipe (for text-based PDFs)
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
                # If UNIPipe fails, fallback to OCRPipe (for scanned or image-based PDFs)
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

            # Process each image in the local_image_dir to extract additional content
            for image_file in os.listdir(local_image_dir):
                if image_file.endswith((".png", ".jpg", ".jpeg")):
                    image_path = os.path.join(local_image_dir, image_file)
                    try:
                        # Read the image as bytes
                        with open(image_path, "rb") as img_file:
                            image_bytes = img_file.read()

                        # Pass the image through OCRPipe for table or text extraction
                        # image_writer=None raise an error, but we don't need to save the images after this process. It avoids double saving.
                        image_ocr = OCRPipe(
                            image_bytes,
                            {"_pdf_type": "", "model_list": []},
                            image_writer=None,
                            is_debug=True,
                        )
                        image_ocr.pipe_classify()
                        image_ocr.pipe_analyze()
                        image_ocr.pipe_parse()

                        image_md_content = image_ocr.pipe_mk_markdown(
                            "", drop_mode=DropMode.NONE, md_make_mode=MakeMode.MM_MD
                        )

                        # Check if the extracted content is valid before appending
                        if image_md_content and image_md_content.strip():
                            image_html_content = markdown2.markdown(image_md_content)
                            if html_content.beginswith("<p>"):
                                html_content += {image_html_content}
                            else:
                                html_content += f"<p>{image_html_content}</p>"
                        else:
                            logger.info(f"No OCR content for image {image_file}")

                    except Exception as ocr_error:
                        logger.warning(
                            f"OCR failed for image {image_file}. Error: {ocr_error}"
                        )

            output_html_path = os.path.join(
                output_dir, f"MinerU_{os.path.splitext(pdf_file)[0]}.html"
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
