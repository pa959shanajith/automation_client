#-------------------------------------------------------------------------------
# Name:        edge_chromium_options.py
# Purpose:     Add desired capabiliites like chrome for Edge Chromium browser
#
# Author:      ranjan.agrawal
#
# Created:     07-03-2021
# Copyright:   (c) ranjan.agrawal 2021
#-------------------------------------------------------------------------------

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class EdgeOptions(webdriver.chrome.options.Options):
    KEY = "ms:edgeOptions"

    def __init__(self):
        super(EdgeOptions, self).__init__()
        self._page_load_strategy = "normal"
        self._caps = DesiredCapabilities.EDGE.copy()

    @property
    def page_load_strategy(self):
        return self._page_load_strategy

    @page_load_strategy.setter
    def page_load_strategy(self, value):
        if value not in ['normal', 'eager', 'none']:
            raise ValueError("Page Load Strategy should be 'normal', 'eager' or 'none'.")
        self._page_load_strategy = value

    def to_capabilities(self):
        """
            Creates a capabilities with all the options that have been set and

            returns a dictionary with everything
        """
        caps = super().to_capabilities()
        caps['pageLoadStrategy'] = self._page_load_strategy

        return caps


webdriver.EdgeChromiumOptions = EdgeOptions