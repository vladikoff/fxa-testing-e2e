# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import urllib, json
import string
import random
import time
from firefox_puppeteer import PuppeteerMixin
from marionette_harness import MarionetteTestCase
from marionette_driver import By, expected, Wait


class TestFxaSync(PuppeteerMixin, MarionetteTestCase):

    def setUp(self):
        super(TestFxaSync, self).setUp()

        self.locationbar = self.browser.navbar.locationbar
        self.identity_popup = self.browser.navbar.locationbar.identity_popup

        self.url_settings = 'https://accounts.firefox.com/settings'
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

            Wait(self.marionette, timeout=self.marionette.timeout.page_load).until(
                expected.element_present(By.ID, 'fxa-pp'))

            input_email = Wait(self.marionette, timeout=self.marionette.timeout.page_load).until(
                expected.element_present(By.CSS_SELECTOR, '.input-row .email'))
            input_email.send_keys(email_pattern)

            input_password = Wait(self.marionette, timeout=self.marionette.timeout.page_load).until(
                expected.element_present(By.ID, 'password'))
            input_password.send_keys(password)

            input_age = Wait(self.marionette, timeout=self.marionette.timeout.page_load).until(
                expected.element_present(By.ID, 'age'))

            # repeat the send keys twice due to a bug with fast test runner typing
            input_age.send_keys('23')
            input_age.send_keys('23')

            self.marionette.find_element(By.ID, 'submit-btn').click()

            # Choose what to sync
            Wait(self.marionette, timeout=self.marionette.timeout.page_load).until(
                expected.element_present(By.ID, 'fxa-choose-what-to-sync-header'))

            self.marionette.find_element(By.ID, 'submit-btn').click()

            # Confirm your account
            Wait(self.marionette, timeout=self.marionette.timeout.page_load).until(
                expected.element_present(By.ID, 'fxa-confirm-header'))

            # Waiting for the email
            time.sleep(6)

            response = urllib.urlopen(self.url_restmail + account_email)
            email_data = json.loads(response.read())

            self.marionette.navigate(email_data[0]['headers']['x-link'])

            # Due to A/B testing here we need to take a different path:
            Wait(self.marionette, timeout=self.marionette.timeout.page_load).until(
                expected.element_present(By.ID, 'fox-logo'))

            # Account Confirmed
            time.sleep(4)
            if "connect_another_device" in self.marionette.get_url():
                Wait(self.marionette, timeout=self.marionette.timeout.page_load).until(
                    expected.element_present(By.CSS_SELECTOR, '.graphic-connect-another-device'))
            else:
                Wait(self.marionette, timeout=self.marionette.timeout.page_load).until(
                    expected.element_present(By.CSS_SELECTOR, '.graphic-checkbox'))


            # give time for sync to kick in...
            time.sleep(3)

            self.marionette.navigate('about:preferences#sync')

            button_manage = Wait(self.marionette, timeout=self.marionette.timeout.page_load).until(
                expected.element_present(By.ID, 'verifiedManage'))
            button_manage.click()

            # Wait for the window to open
            time.sleep(3)

            # Switch to the new Window
            self.marionette.switch_to_window(self.marionette.window_handles[1])

            # Account settings

            Wait(self.marionette, timeout=self.marionette.timeout.page_load).until(
                expected.element_present(By.ID, 'fxa-settings-profile-header'))

            # Login to reliers with this account

            # Add-ons
            self.marionette.navigate('https://addons.mozilla.org/en-US/firefox/')

            button_login = Wait(self.marionette, timeout=self.marionette.timeout.page_load).until(
                expected.element_present(By.CSS_SELECTOR, '.login > a:nth-child(2)'))
            button_login.click()

            fxa_login = Wait(self.marionette, timeout=self.marionette.timeout.page_load).until(
                expected.element_present(By.CSS_SELECTOR, '.use-logged-in'))
            fxa_login.click()

            Wait(self.marionette, timeout=self.marionette.timeout.page_load).until(
                expected.element_present(By.CSS_SELECTOR, '.logout'))

            # Pocket
            self.marionette.navigate('https://getpocket.com/login')

            button_login = Wait(self.marionette, timeout=self.marionette.timeout.page_load).until(
                expected.element_present(By.CSS_SELECTOR, '.login-btn-firefox'))
            button_login.click()

            fxa_login = Wait(self.marionette, timeout=self.marionette.timeout.page_load).until(
                expected.element_present(By.CSS_SELECTOR, '.use-logged-in'))
            fxa_login.click()

            fxa_accept = Wait(self.marionette, timeout=self.marionette.timeout.page_load).until(
                expected.element_present(By.CSS_SELECTOR, '#accept'))
            fxa_accept.click()

            Wait(self.marionette, timeout=self.marionette.timeout.page_load).until(
                expected.element_present(By.CSS_SELECTOR, '.gsf_pocketlogo'))

            # Pontoon
            self.marionette.navigate('https://pontoon.mozilla.org/teams/')

            button_menu = Wait(self.marionette, timeout=self.marionette.timeout.page_load).until(
                expected.element_present(By.CSS_SELECTOR, '.menu-icon'))
            button_menu.click()

            button_login = Wait(self.marionette, timeout=self.marionette.timeout.page_load).until(
                expected.element_present(By.CSS_SELECTOR, '#fxa-sign-in'))
            button_login.click()

            fxa_login = Wait(self.marionette, timeout=self.marionette.timeout.page_load).until(
                expected.element_present(By.CSS_SELECTOR, '.use-logged-in'))
            fxa_login.click()

            Wait(self.marionette, timeout=self.marionette.timeout.page_load).until(
                expected.element_present(By.CSS_SELECTOR, '#sign-out'))

            # Test Basket Subscription

            self.marionette.navigate(self.url_settings)

            comm_prefs = Wait(self.marionette, timeout=self.marionette.timeout.page_load).until(
                expected.element_present(By.CSS_SELECTOR, '#communication-preferences .settings-button'))
            comm_prefs.click()

            sub_button = Wait(self.marionette, timeout=self.marionette.timeout.page_load).until(
                expected.element_present(By.CSS_SELECTOR, '#marketing-email-optin'))
            sub_button.click()

            time.sleep(6)

            self.marionette.refresh()

            time.sleep(2)

            comm_prefs = Wait(self.marionette, timeout=self.marionette.timeout.page_load).until(
                expected.element_present(By.CSS_SELECTOR, '#communication-preferences .settings-button'))
            comm_prefs.click()

            Wait(self.marionette, timeout=self.marionette.timeout.page_load).until(
                expected.element_present(By.CSS_SELECTOR, '#preferences-url'))

            # Unsubscribe

            sub_button = Wait(self.marionette, timeout=self.marionette.timeout.page_load).until(
                expected.element_present(By.CSS_SELECTOR, '#marketing-email-optin'))
            sub_button.click()

            # Devices, check the device is in settings

            device_prefs = Wait(self.marionette, timeout=self.marionette.timeout.page_load).until(
                expected.element_present(By.CSS_SELECTOR, '#clients .settings-button'))
            device_prefs.click()

            Wait(self.marionette, timeout=self.marionette.timeout.page_load).until(
                expected.element_present(By.CSS_SELECTOR, '#clients .client-current'))

            # Delete account
            button_delete = Wait(self.marionette, timeout=self.marionette.timeout.page_load).until(
                expected.element_present(By.CSS_SELECTOR, '#delete-account .settings-button'))
            button_delete.click()

            input_delete_password = Wait(self.marionette, timeout=self.marionette.timeout.page_load).until(
                expected.element_present(By.CSS_SELECTOR, '#delete-account input.password'))
            input_delete_password.send_keys(password)

            button_delete = Wait(self.marionette, timeout=self.marionette.timeout.page_load).until(
                expected.element_present(By.CSS_SELECTOR, '#delete-account button[type=submit]'))
            button_delete.click()

            # Deleted
            Wait(self.marionette, timeout=self.marionette.timeout.page_load).until(
                expected.element_present(By.ID, 'fxa-signup-header'))

            self.marionette.close()

            print "FxA / Sync work!"
