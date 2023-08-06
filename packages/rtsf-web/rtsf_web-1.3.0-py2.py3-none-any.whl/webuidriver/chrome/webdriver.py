#! python3
# -*- encoding: utf-8 -*-

from webuidriver.remote.until_fiind import UntilFind
from selenium.webdriver.chrome.webdriver import WebDriver as ChromeWebDriver


class WebDriver(ChromeWebDriver):
    def __init__(self, *args, **kwargs):
        ChromeWebDriver.__init__(self, *args, **kwargs)
        self._until_find = UntilFind(self)

    @property
    def until_find(self):
        """
        :Returns:
            - UntilFind: an object containing all options for dynamically waiting and finding elements.

        :Usage:
            element = driver.until_find.element_by_id('#username')
            element.send_keys("admin")
        """
        return self._until_find
