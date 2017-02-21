#!/bin/bash -ex

source ./venv_modules/bin/activate
firefox-ui-functional fxa_tests/test_fxa_sync.py --binary firefox/FirefoxNightly.app/Contents/MacOS/firefox-bin -v
