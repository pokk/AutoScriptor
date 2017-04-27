#!/usr/bin/env bash
# Checkout to current file path.
cd "`dirname "$0"`"

if [ -f requirements.txt ]; then
	pip3 install -r requirements.txt
fi

python3 generate_google_file_link.py