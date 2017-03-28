#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""."""

import re


class IndicatorParser():
    """Class for parsing indicators from an email."""

    def __init__(self, email_string):
        """."""
        self.text = email_string
        self.regexes = {
            'host': "\S*\.\S{1,10}",
            'ip_address': "^(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9])\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9]|0)\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9]|0)\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[0-9])$",
            'url': "http[s]?:\/\/\S*"
        }

    def _parse_indicator(self, indicator_type):
        """Parse indicators of a given type out of the text."""
        indicators = list()

        indicators = re.findall(self.regexes[indicator_type], self.text)

        return indicators

    def parse_indicators(self):
        """parse_indicators from a text."""
        indicators = dict()

        indicators['hosts'] = self._parse_indicator('host')
        indicators['ip_addresses'] = self._parse_indicator('ip_address')
        indicators['urls'] = self._parse_indicator('url')

        return indicators
