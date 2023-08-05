#
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#

# #################################################################################################

from .report_item import ReportItem


# #################################################################################################

class Error(ReportItem):
    def __init__(self, line: int, msg: str) -> None:
        super().__init__(line, msg)

    def isFatal(self):
        return True


class Warning(ReportItem):
    def __init__(self, line: int, msg: str) -> None:
        super().__init__(line, msg)
