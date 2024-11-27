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

### Create a virtual env for python

```bash
python3 -m venv .venv
```
