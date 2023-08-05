#
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#

from ..app import App
from ..entries import *
from ..report.report import Report
from ..report.warn import Warn
from ..report.error import Error


# #################################################################################################

class TrailingSpaces(object):
    @staticmethod
    def check(app: App, reference: 'PropFile', translation: 'PropFile' = None) -> Report:
        """
        Check if provided translation has trailing spaces at the end of each translation.
        """
        report = Report()
        for idx, item in enumerate(reference):
            if isinstance(item, (PropTranslation, PropComment)):
                diff = len(item.value) - len(item.value.rstrip())
                if diff == 0:
                    continue

                if isinstance(item, PropTranslation):
                    report.add(Error(idx + 1, f'Trailing whitespaces in translation of "{item.key}": {diff}'))
                else:
                    report.add(Warn(idx + 1, f'Trailing whitespaces in comment: {diff}'))
        return report
