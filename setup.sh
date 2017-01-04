#!/bin/bash -ex

rm -rf ./firefox
rm -rf ./venv_modules

# Always stay one day behind Nightly to avoid 404ing on the download
# Create virtualenv
virtualenv venv_modules

# Activate virtualenv
source venv_modules/bin/activate

pip install -U pip

# Install modules to download Firefox
pip install -r requirements.txt --no-cache-dir

# Download Firefox
mozdownload --type=daily --destination=firefox

# Install Firefox into our directory
mozinstall firefox/*firefox* -d firefox

# Download common test files
mozdownload --type=daily --extension common.tests.zip --destination=firefox

# Unzip the common tests
unzip -q firefox/*.common.tests.zip -d firefox/tests

# Install Marionette requirements
cd firefox/tests/config && pip install -r firefox_ui_requirements.txt
cd ../../..

# Replace firefox_puppeteer
# For some reason PIP installs the old version of firefox_puppeteer
# Replace the installed version with the one provided by common.tests.zip
rm -rf ./venv_modules/lib/python*/site-packages/firefox_puppeteer
cp -r firefox/tests/marionette/puppeteer/firefox/firefox_puppeteer ./venv_modules/lib/python*/site-packages/
cp -r firefox/tests/marionette ./venv_modules/lib/python*/site-packages/


echo "Dependencies installed. Run ./run.sh to run the tests..."
