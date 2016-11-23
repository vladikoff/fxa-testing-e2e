#!/bin/bash -ex
ls firefox

source venv_modules/bin/activate

firefox-ui-functional fxa_tests/test_fxa_sync.py --binary firefox/firefox/firefox-bin
