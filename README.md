# PDF to HTML Benchmarking Project

This repository benchmarks various libraries for converting PDF files into HTML. The primary focus is on assessing the quality of the conversion, particularly for complex document structures such as tables, hierarchical sections, and text formatting.

## Project Overview

The aim of this project is to:

- Compare multiple libraries for PDF to HTML conversion.

- Evaluate performance based on fidelity, structure preservation, and ease of use.

- Generate outputs compatible with the [TipTap](https://tiptap.dev/) editor used in a React-based application.

## Setup

### Prerequisites

Ensure you have the following installed:

- **Python** version 3.10 recommended to have the laste release of MinerU magic_pdf, 3.11 for the others(documentation will be updated, be careful and try with different virtual env)
- Any required dependencies for the libraries being tested (see below).

Run these commands :

```bash
sudo apt update
sudo apt install libgl1-mesa-glx -y
```

### Clone the Repository

```bash
git clone git@github.com:TomQuez/Benchmarking_libs_pdf_to_HTML.git
cd Benchmarking_libs_pdf_to_HTML
```

## Using MinerU

### Create a virtual en adapted to Mineru magig_pdf

```bash
sudo apt install python3.10-venv
python3.10 -m venv env_magic_pdf
source env_magic_pdf/bin/activate
```

### install MinerU

MinerU documentation :
<https://mineru.readthedocs.io/en/latest/>
Mandatory to have python 3.10 to have access to the last version of magic_pdf.

Ensure that your conda virtual env is activated.

```bash
pip install -U magic-pdf[full] --extra-index-url https://wheels.myhloli.com
```

Initial download of models files :

```bash
pip install huggingface_hub markdown2
wget https://github.com/opendatalab/MinerU/raw/master/scripts/download_models_hf.py -O download_models_hf.py
python3 download_models_hf.py
```

If you have a GPU with more than 8GB of VRAM, and CUDA change the device-mode to cuda in the magic-pdf.json (see MinerU documentation).

Execute this command to test the MinerU script on your pdf documents:

```bash
python3 scripts/pdf_to_html_MinerU.py
```

## Using Docling

Docling should detect if you have a GPU available.

```bash
deactivate
sudo apt install python3.11 python3.11-venv python3.11-dev
python3.11 -m venv env_docling
source env_docling/bin/activate
pip install docling loguru
pip uninstall tesserocr
pip install --no-binary :all: tesserocr
python3 scripts/pdf_to_html_docling.py
```

## Using Megaparse

check Megaparse documentation. this doc is adapted to megaparse 0.0.48

```bash
deactivate
python3.11 -m venv env_megaparse
source env_megaparse/bin/activate
pip install megaparse markdown2
```

This readme file must be updated. Should be done soon.
