#!/bin/bash
echo "Setting up environment variables"
echo "HOME var : $HOME"
eval "$($HOME/miniconda3/bin/conda shell.bash hook)"

if [[ "$CONDA_DEFAULT_ENV" == "base" ]] ; then
    conda deactivate
fi
# replace the env name "benchmarking" with your own env name
conda activate benchmarking

echo "Environment variables set up"