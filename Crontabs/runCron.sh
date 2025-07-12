#!/bin/bash

# Get the directory of the current script
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Activate the virtual environment
source "${script_dir}/../.venv/bin/activate"

# Check if a script name was provided
if [ -z "$1" ]; then
    echo "No python script given" >>"${script_dir}/output.log"
    exit 1
fi

# Get the Python script name from the first argument
pythonScript="$1"

# Run the Python script and log output
python3 $pythonScript >>"${script_dir}/output.log" 2>&1
