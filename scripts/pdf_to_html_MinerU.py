import os
import time
from loguru import logger
from magic_pdf.data.data_reader_writer import FileBasedDataWriter, FileBasedDataReader
from magic_pdf.data.dataset import PymuDocDataset
from magic_pdf.model.doc_analyze_by_custom_model import doc_analyze
from magic_pdf.config.enums import SupportedPdfParseMethod
import markdown2

# Définir les répertoires d'entrée et de sortie
current_dir = os.path.dirname(os.path.realpath(__file__))
pdf_samples = os.path.join(current_dir, "../pdf_samples")
output_dir = os.path.join(current_dir, "../outputs")
local_image_dir = os.path.join(output_dir, "images")
os.makedirs(output_dir, exist_ok=True)
os.makedirs(local_image_dir, exist_ok=True)

image_writer = FileBasedDataWriter(local_image_dir)
md_writer = FileBasedDataWriter(output_dir)

try:
    pdf_files = [f for f in os.listdir(pdf_samples) if f.endswith(".pdf")]
    for pdf_file in pdf_files:
        try:
            logger.info(f"Start extraction for {pdf_file}")
            pdf_path = os.path.join(pdf_samples, pdf_file)

            # Lecture du fichier PDF
            reader = FileBasedDataReader("")
            pdf_bytes = reader.read(pdf_path)

            # Initialisation de Dataset
            dataset = PymuDocDataset(pdf_bytes)

            # Classification pour déterminer le mode de traitement
            parse_method = dataset.classify()
            logger.info(f"PDF classification result: {parse_method}")

            if parse_method == SupportedPdfParseMethod.OCR:
                # Analyse avec OCR
                infer_result = dataset.apply(doc_analyze, ocr=True)
                pipe_result = infer_result.pipe_ocr_mode(image_writer)
            else:
                # Analyse avec le texte
                infer_result = dataset.apply(doc_analyze, ocr=False)
                pipe_result = infer_result.pipe_txt_mode(image_writer)

            # Sauvegarde des résultats
            name_without_suff = os.path.splitext(pdf_file)[0]

            # Génération et sauvegarde du fichier Markdown
            pipe_result.dump_md(md_writer, f"{name_without_suff}.md", "images")

            # Génération et sauvegarde de la liste de contenu
            pipe_result.dump_content_list(
                md_writer, f"{name_without_suff}_content_list.json", "images"
            )

            # Génération de l'HTML à partir du Markdown
            md_path = os.path.join(output_dir, f"{name_without_suff}.md")
            with open(md_path, "r", encoding="utf-8") as md_file:
                md_content = md_file.read()

            html_content = markdown2.markdown(md_content)
            html_path = os.path.join(
                output_dir, f"Mineru_{time.time()}_{name_without_suff}.html"
            )
            with open(html_path, "w", encoding="utf-8") as html_file:
                html_file.write(html_content)

            logger.info(f"Extraction done for {pdf_file}. Output is {html_path}")

        except Exception as e:
            logger.exception(f"Error during extraction for file {pdf_file}: {e}")
except Exception as e:
    logger.exception(f"Error during extraction: {e}")
