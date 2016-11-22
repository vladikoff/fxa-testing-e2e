#!/bin/bash -ex

rm -rf ./firefox

DATE=`date +%Y-%m-%d`

# Create virtualenv
virtualenv venv_modules

# Activate virtualenv
source venv_modules/bin/activate

# Install modules to download Firefox
pip install -r requirements.txt --no-cache-dir

# Download Firefox
mozdownload --type=daily --date=$DATE --destination=firefox

# Install Firefox into our directory
mozinstall firefox/$DATE-* -d firefox

# Download common test files
mozdownload --type=daily --date=$DATE --extension common.tests.zip --destination=firefox

# Unzip the common tests
unzip -q firefox/*.common.tests.zip -d firefox/tests

# Install Marionette requirements
cd firefox/tests/config && pip install -r firefox_ui_requirements.txt --no-cache-dir
cd ../../..

echo "Dependencies installed. Run ./run.sh to run the tests..."
