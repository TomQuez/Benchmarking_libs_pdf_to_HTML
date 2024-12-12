import os
from loguru import logger
from docling.datamodel.base_models import InputFormat
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions, TableFormerMode
from docling.models.tesseract_ocr_model import TesseractOcrOptions
import time

# Définir les répertoires d'entrée et de sortie
current_dir = os.path.dirname(os.path.realpath(__file__))
pdf_samples = os.path.join(current_dir, "../pdf_samples")
output_dir = os.path.join(current_dir, "../outputs")

os.makedirs(output_dir, exist_ok=True)
start_time = time.time()
try:
    pdf_files = [f for f in os.listdir(pdf_samples) if f.endswith(".pdf")]
    for pdf_file in pdf_files:
        try:
            logger.info(f"Début de l'extraction pour {pdf_file}")
            pdf_path = os.path.join(pdf_samples, pdf_file)
            pipeline_options = PdfPipelineOptions()
            pipeline_options.do_ocr = True
            pipeline_options.do_table_structure = True
            pipeline_options.table_structure_options.do_cell_matching = True
            pipeline_options.ocr_options = TesseractOcrOptions()

            pipeline_options.table_structure_options.mode = TableFormerMode.ACCURATE

            doc_converter = DocumentConverter(
                format_options={
                    InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
                }
            )

            result = doc_converter.convert(pdf_path)

            html_content = result.document.export_to_html()

            output_html_path = os.path.join(
                output_dir,
                f"Docling_{time.time()}_{os.path.splitext(pdf_file)[0]}.html",
            )
            with open(output_html_path, "w", encoding="utf-8") as f:
                f.write(html_content)

            logger.info(
                f"Extraction terminée pour {pdf_file}. Fichier créé : {output_html_path}"
            )
        except Exception as e:
            logger.exception(
                f"Erreur lors de l'extraction pour le fichier {pdf_file}: {e}"
            )
            raise e
except Exception as e:
    logger.exception(f"Erreur lors du processus d'extraction: {e}")
    raise e
