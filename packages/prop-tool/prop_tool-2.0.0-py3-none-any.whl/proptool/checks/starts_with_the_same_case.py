"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""

from proptool.decorators.overrides import overrides
from proptool.prop.items import Translation
from proptool.report.group import ReportGroup
from .base.check import Check


# noinspection PyUnresolvedReferences
class StartsWithTheSameCase(Check):
    """
    This check verifies translation first letter is the same lower/upper cased as original text.
    """

    @overrides(Check)
    # Do NOT "fix" the PropFile reference and do not import it, or you step on circular dependency!
    def check(self, translation_file: 'PropFile', reference_file: 'PropFile' = None) -> ReportGroup:
        self.need_both_files(translation_file, reference_file)

        report = ReportGroup('Sentence starts with different letter case.')

        for idx, item in enumerate(translation_file.items):
            # We care translations only for now.
            # Do not try to be clever and filter() data first, because line_number values will no longer be correct.
            if not isinstance(item, Translation):
                continue

            # Is there translation of this item present?
            ref = reference_file.find_by_key(item.key)
            # Skip dangling keys
            if not ref:
                continue

            # Skip if translation or reference string is empty.
            if item.value.strip() == '' or ref.value.strip() == '':
                continue

            trans_first_char = item.value[0]
            ref_first_char = ref.value[0]

            if trans_first_char.isupper() != ref_first_char.isupper():
                if ref_first_char.isupper():
                    expected = 'UPPER-cased'
                    found = 'lower-cased'
                else:
                    expected = 'lower-cased'
                    found = 'UPPER-cased'

                report.warn(idx + 1, f'Value starts with {found} character. Expected {expected}.', item.key)

        return report
