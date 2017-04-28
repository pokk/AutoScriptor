#!/usr/bin/env bash
file_name="generate_google_file_link"
final_name="GGFL.app"

# Checkout to current file path.
cd "`dirname "$0"`"
# Install the necessary component.
easy_install -U py2app

# Check 'setup.py' is exist or not.
if [ -f setup.py ]; then
	rm setup.py
fi

# Build python to mac app.
py2applet --make-setup ${file_name}".py"
python3 setup.py py2app -A

# Rename.
mv dist/${file_name}".app" dist/${final_name}