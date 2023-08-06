#! python3
# -*- encoding: utf-8 -*-

from webuidriver.remote.until_fiind import UntilFind
from selenium.webdriver.firefox.webdriver import WebDriver as FirefoxWebDriver


class WebDriver(FirefoxWebDriver):
    def __init__(self, *args, **kwargs):
        FirefoxWebDriver.__init__(self, *args, **kwargs)
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
