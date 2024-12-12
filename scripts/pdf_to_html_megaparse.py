import logging
from megaparse import MegaParse
from langchain_openai import ChatOpenAI
from megaparse.parser.unstructured_parser import UnstructuredParser
import nltk
import os
import markdown2

PDF_INPUT_DIR = os.getenv("PDF_INPUT_DIR", "./pdf_samples/")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "./outputs/")
os.makedirs(OUTPUT_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def check_nltk_data(resource_name):
    """
    Check if an NLTK resource is available locally.

    Args:
        resource_name (str): Name of the NLTK resource to check.

    Returns:
        bool: True if the resource is available, False otherwise.
    """
    try:
        nltk.data.find(
            f"tokenizers/{resource_name}"
            if "punkt" in resource_name
            else f"taggers/{resource_name}"
        )
        logger.info(f"The resource '{resource_name}' is available locally.")
        return True
    except LookupError:
        logger.warning(f"The resource '{resource_name}' is NOT available locally.")
        return False


resources = ["punkt_tab", "averaged_perceptron_tagger_eng"]

for resource in resources:
    if not check_nltk_data(resource):
        logger.info(f"Downloading the resource '{resource}'...")
        nltk.download(resource)

logger.info("Initializing MegaParse...")
parser = UnstructuredParser()
megaparse = MegaParse(parser)


logger.info(f"Processing PDF files in {PDF_INPUT_DIR}...")
for filename in os.listdir(PDF_INPUT_DIR):
    if filename.endswith(".pdf"):
        input_path = os.path.join(PDF_INPUT_DIR, filename)
        output_filename = f"Megaparse_{os.path.splitext(filename)[0]}.html"
        output_path = os.path.join(OUTPUT_DIR, output_filename)

        try:
            logger.info(f"Processing {filename}...")
            md_content = megaparse.load(input_path)
            html_content = markdown2.markdown(md_content)

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(html_content)
        except Exception as e:
            logger.exception(f"Error processing {filename}: {e}")
