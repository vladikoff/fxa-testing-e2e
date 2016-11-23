# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time
from firefox_puppeteer import PuppeteerMixin
from marionette import MarionetteTestCase
from marionette_driver import By, expected, Wait


class TestDVCertificate(PuppeteerMixin, MarionetteTestCase):

    def setUp(self):
        super(TestDVCertificate, self).setUp()

        self.locationbar = self.browser.navbar.locationbar
        self.identity_popup = self.browser.navbar.locationbar.identity_popup

        self.url_signup = 'https://accounts.firefox.com/signup?service=sync&context=fx_desktop_v3'

    def tearDown(self):
        try:
            self.browser.switch_to()
            self.identity_popup.close(force=True)
            self.puppeteer.windows.close_all([self.browser])
        finally:
            super(TestDVCertificate, self).tearDown()

    def test_dv_cert(self):
        with self.marionette.using_context('content'):
            self.marionette.navigate(self.url_signup)

            Wait(self.marionette, timeout=self.browser.timeout_page_load).until(
                expected.element_present(By.ID, 'fxa-pp'))

            fxaPP = self.marionette.find_element(By.ID, 'fxa-pp')
            fxaPP.click()

            Wait(self.marionette, timeout=self.browser.timeout_page_load).until(
                expected.element_present(By.ID, 'fxa-pp-header'))
