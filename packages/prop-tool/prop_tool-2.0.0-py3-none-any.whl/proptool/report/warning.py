#
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#

from ..overrides import overrides
from .report import ReportItem


# #################################################################################################

class Warning(ReportItem):
    def __init__(self, line: int, msg: str) -> None:
        super().__init__(line, msg)

    # @overrides(ReportItem)
    def type(self):
        return 'W'
