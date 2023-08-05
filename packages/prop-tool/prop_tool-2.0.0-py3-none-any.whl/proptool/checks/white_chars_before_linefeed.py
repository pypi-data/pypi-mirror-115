"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""
from typing import Dict, Union

from proptool.decorators.overrides import overrides
from proptool.prop.items import Translation
from proptool.report.group import ReportGroup
from .base.check import Check


class WhiteCharsBeforeLinefeed(Check):
    r"""
    This check ensures there's no space before "\n", "\r" literals.
    """

    def __init__(self, config: Union[Dict, None] = None):
        super().__init__(config)
        self.is_single_file_check = True

    def _scan(self, report: ReportGroup, idx: int, item: Translation, literal: str) -> bool:
        literal_len = len(literal)
        # Let's crawl backward and see what's there...
        for pos in range(len(item.value) - literal_len, 0, -1):
            if item.value[pos:(pos + 2)] == literal:
                pre = item.value[pos - 1]
                if pre in {' ', '\t'}:
                    what = 'SPACE' if pre == ' ' else 'TAB'
                    report.warn(f'{idx + 1}:{pos}', f'Contains {what} character before "{literal}" literal.', item.key)
                    return True
        return False

    # noinspection PyUnresolvedReferences
    @overrides(Check)
    # Do NOT "fix" the PropFile reference and do not import it, or you step on circular dependency!
    def check(self, translation_file: 'PropFile', reference_file: 'PropFile' = None) -> ReportGroup:
        report = ReportGroup('White chars before linefeed literal')

        for idx, item in enumerate(translation_file.items):
            # We care translations only for now.
            # Do not try to be clever and filter() data first, because line_number values will no longer be correct.
            if not isinstance(item, Translation):
                continue

            for literal in (r'\n', r'\r'):
                # Skip too short lines.
                literal_len = len(literal)
                if len(item.value.strip()) <= literal_len:
                    continue

                if self._scan(report, idx, item, literal):
                    break

        return report
