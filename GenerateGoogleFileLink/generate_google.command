#!/usr/bin/env bash
requirement="requirements.txt"

# Checkout to current file path.
cd "`dirname "$0"`"

if [ -f ${requirement} ]; then
	pip3 install -r ${requirement}
fi

python3 generate_google_file_link.py