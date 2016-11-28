# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import urllib, json
import string
import random
import time
from firefox_puppeteer import PuppeteerMixin
from marionette import MarionetteTestCase
from marionette_driver import By, expected, Wait


class TestFxaSync(PuppeteerMixin, MarionetteTestCase):

    def setUp(self):
        super(TestFxaSync, self).setUp()

        self.locationbar = self.browser.navbar.locationbar
        self.identity_popup = self.browser.navbar.locationbar.identity_popup

        self.url_signup = 'https://accounts.firefox.com/signup?service=sync&context=fx_desktop_v3'
        self.url_restmail = 'http://restmail.net/mail/'

    def tearDown(self):
        try:
            self.browser.switch_to()
            self.identity_popup.close(force=True)
            self.puppeteer.windows.close_all([self.browser])
        finally:
            super(TestFxaSync, self).tearDown()

    def test_fxa_sync(self):
        hostname = 'restmail.net'
        password = ''.join([random.choice(string.ascii_letters) for i in range(8)])
        account_email = 'fxa-e2e-' + ''.join(random.choice(string.ascii_lowercase) for _ in range(12))
        email_pattern = account_email + '@' + hostname

        with self.marionette.using_context('content'):
            self.marionette.navigate(self.url_signup)

            Wait(self.marionette, timeout=self.browser.timeout_page_load).until(
                expected.element_present(By.ID, 'fxa-pp'))

            input_email = Wait(self.marionette, timeout=self.browser.timeout_page_load).until(
                expected.element_present(By.CSS_SELECTOR, '.input-row .email'))
            input_email.send_keys(email_pattern)

            input_password = Wait(self.marionette, timeout=self.browser.timeout_page_load).until(
                expected.element_present(By.ID, 'password'))
            input_password.send_keys(password)

            input_age = Wait(self.marionette, timeout=self.browser.timeout_page_load).until(
                expected.element_present(By.ID, 'age'))
            input_age.send_keys('23')

            self.marionette.find_element(By.ID, 'submit-btn').click()

            # Choose what to sync
            Wait(self.marionette, timeout=self.browser.timeout_page_load).until(
                expected.element_present(By.ID, 'fxa-choose-what-to-sync-header'))

            self.marionette.find_element(By.ID, 'submit-btn').click()

            # Confirm your account
            Wait(self.marionette, timeout=self.browser.timeout_page_load).until(
                expected.element_present(By.ID, 'fxa-confirm-header'))

            # Waiting for the email
            time.sleep(3)

            response = urllib.urlopen(self.url_restmail + account_email)
            email_data = json.loads(response.read())

            self.marionette.navigate(email_data[0]['headers']['x-link'])

            # Account Confirmed
            Wait(self.marionette, timeout=self.browser.timeout_page_load).until(
                expected.element_present(By.ID, 'fxa-sign-up-complete-header'))

            Wait(self.marionette, timeout=self.browser.timeout_page_load).until(
                expected.element_present(By.CSS_SELECTOR, '.graphic-checkbox'))

            # give time for sync to kick in...
            time.sleep(3)

            self.marionette.navigate('about:preferences#sync')

            button_manage = Wait(self.marionette, timeout=self.browser.timeout_page_load).until(
                expected.element_present(By.ID, 'verifiedManage'))
            button_manage.click()

            # Wait for the window to open
            time.sleep(3)

            # Switch to the new Window
            self.marionette.switch_to_window(self.marionette.window_handles[1])

            # Account settings

            Wait(self.marionette, timeout=self.browser.timeout_page_load).until(
                expected.element_present(By.ID, 'fxa-settings-profile-header'))

            # Delete account
            button_delete = Wait(self.marionette, timeout=self.browser.timeout_page_load).until(
                expected.element_present(By.CSS_SELECTOR, '#delete-account .settings-button'))
            button_delete.click()

            input_delete_password = Wait(self.marionette, timeout=self.browser.timeout_page_load).until(
                expected.element_present(By.CSS_SELECTOR, '#delete-account input.password'))
            input_delete_password.send_keys(password)

            button_delete = Wait(self.marionette, timeout=self.browser.timeout_page_load).until(
                expected.element_present(By.CSS_SELECTOR, '#delete-account button[type=submit]'))
            button_delete.click()

            # Deleted
            Wait(self.marionette, timeout=self.browser.timeout_page_load).until(
                expected.element_present(By.ID, 'fxa-signup-header'))

            self.marionette.close()

            print "Sync works!"
