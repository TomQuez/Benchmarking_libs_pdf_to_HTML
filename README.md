# PDF to HTML Benchmarking Project

This repository benchmarks various libraries for converting PDF files into HTML. The primary focus is on assessing the quality of the conversion, particularly for complex document structures such as tables, hierarchical sections, and text formatting.

## Project Overview

The aim of this project is to:
- Compare multiple libraries for PDF to HTML conversion.
- Evaluate performance based on fidelity, structure preservation, and ease of use.
- Generate outputs compatible with the [TipTap](https://tiptap.dev/) editor used in a React-based application (`react-orders`).

## Setup

### Prerequisites

Ensure you have the following installed:
- **Python** (version 3.8+ recommended)
- Any required dependencies for the libraries being tested (e.g., `pdf2htmlEX`, `pdfminer.six`).

### Clone the Repository

```bash
git clone https://github.com/<your-username>/<repository-name>.git
cd <repository-name>
```

### Create a conda virtual env

refer to <https://docs.anaconda.com/miniconda/install/#quick-command-line-install>
It's recommended to create a specific conda environment with these commands :

```bash
conda deactivate
conda create --name yourEnvName python=3.10
conda activate yourEnvName

```

## Using MinerU

### install MinerU

Ensure that your conda virtual env is activated.

```bash
pip install -U magic-pdf[full] --extra-index-url https://wheels.myhloli.com
```

Initial download of models files :

```bash
pip install huggingface_hub
wget https://github.com/opendatalab/MinerU/raw/master/scripts/download_models_hf.py -O download_models_hf.py
python download_models_hf.py
```
