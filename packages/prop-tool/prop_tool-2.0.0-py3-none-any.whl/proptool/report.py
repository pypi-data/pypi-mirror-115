#
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#

# #################################################################################################

from .report_item import ReportItem


class Report(list):
    def add(self, item: ReportItem) -> None:
        if not isinstance(item, ReportItem):
            raise TypeError
        self.append(item)

    def addIf(self, condition: bool, item: ReportItem) -> None:
        if condition:
            self.add(item)
