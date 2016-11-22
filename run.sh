#!/bin/bash -ex
ls firefox

firefox-ui-functional firefox/tests/firefox-ui/tests/functional/security/test_dv_certificate.py --binary firefox/firefox/firefox-bin
