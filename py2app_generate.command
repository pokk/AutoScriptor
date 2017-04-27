#!/usr/bin/env bash
# Checkout to current file path.
cd "`dirname "$0"`"
easy_install -U py2app

# Check steup.py is exist or not.
if [ -f setup.py ]; then
	rm setup.py
fi

py2applet --make-setup generate_google_file_link.py
python3 setup.py py2app -A
