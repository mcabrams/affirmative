import time

from django.core import urlresolvers
from django.test import LiveServerTestCase

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.remote import webdriver


class FunctionalTestCase(LiveServerTestCase):
    host = 'web'

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.WebDriver(
            command_executor='http://selenium:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.CHROME)
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()
        super().tearDownClass()
        cls.driver.quit()

    @classmethod
    def addCleanup(cls):
        # Always quit the driver, even when an exception occurs.
        cls.driver.quit()

    def run(self, result):
        self.result = result.result if hasattr(result, 'result') else result
        self.result.stopTest = self.stopTest
        super().run(result)

    def stopTest(self, test):
        """Called when the given test has been run, if we have any errors
        let's take a screenshot"""
        if not self.passed:
            self.screen_shot()

    @property
    def passed(self):
        return not (self.errored or self.failed)

    @property
    def errored(self):
        return self.id() in [case.id() for case, _ in self.result.errors]

    @property
    def failed(self):
        return self.id() in [case.id() for case, _ in self.result.failures]

    def screen_shot(self):
        date_string = time.strftime("%m-%d-%H-%M")
        file_name = "/django/{}-{}.jpg".format(date_string,
                                               self._testMethodName)
        self.driver.save_screenshot(file_name)

    def url(self, path):
        """Returns a fully qualified URL given a path component."""
        return self.live_server_url + path

    def reverse(self, *args, **kwargs):
        """Returns a fully qualified URL given the arguments you would pass to
        reverse().

        See the reverse() documentation for details:
        https://docs.djangoproject.com/en/1.8/ref/urlresolvers/
        """

        return self.url(urlresolvers.reverse(*args, **kwargs))
