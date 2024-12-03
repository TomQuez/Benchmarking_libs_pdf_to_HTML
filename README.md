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

- **Python** (version 3.8+ recommended)
- Any required dependencies for the libraries being tested (see below).

### Clone the Repository

```bash
git clone git@github.com:TomQuez/Benchmarking_libs_pdf_to_HTML.git
cd Benchmarking_libs_pdf_to_HTML
```

### Create a conda virtual env (not mandatory but recommended)

Refer to <https://docs.anaconda.com/miniconda/install/#quick-command-line-install>

After installing, add conda to your $PATH env variable.
Temporary:

```bash
export PATH=~/miniconda3/bin:$PATH
```

Permanently:

```bash
echo 'export PATH=~/miniconda3/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
exec bash
```

It's recommended to create a specific conda environment with these commands :

```bash
conda deactivate
conda create --name yourEnvName python=3.10
conda activate yourEnvName

```

Use the init_env.sh script to activate your env (replace the environment name by yours):

```bash
source ./init_env.sh
```

## Using MinerU

### install MinerU

MinerU documentation :
<https://mineru.readthedocs.io/en/latest/>

Ensure that your conda virtual env is activated.

```bash
pip install -U magic-pdf[full] --extra-index-url https://wheels.myhloli.com
```

Initial download of models files :

```bash
pip install huggingface_hub
wget https://github.com/opendatalab/MinerU/raw/master/scripts/download_models_hf.py -O download_models_hf.py
python3 download_models_hf.py
```

Execute this command to test the MinerU script on your pdf documents:

```bash
python3 scripts/pdf_to_html_MinerU.py  
```
