"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""

from typing import Dict, List, Union

from proptool.decorators.overrides import overrides
from proptool.prop.items import Comment, Translation
from proptool.report.group import ReportGroup
from .base.check import Check


class Bracket(object):
    def __init__(self, pos: int, bracket: str):
        self.pos = pos
        self.bracket = bracket


# noinspection PyUnresolvedReferences
class Brackets(Check):
    """
    Checks if brackets are used in translation and if so, ensures proper nesting and checks if all
    opened brackets are closed.
    """

    def __init__(self, config: Union[Dict, None] = None):
        super().__init__(config)
        self.is_single_file_check = True

    report_title = 'Brackets'

    @overrides(Check)
    # Do NOT "fix" the PropFile reference and do not import it, or you step on circular dependency!
    def check(self, translation: 'PropFile', reference: 'PropFile' = None) -> ReportGroup:
        self.need_valid_config()

        report = ReportGroup(self.report_title)

        opening = self.config['opening']
        closing = self.config['closing']

        opening_cnt = len(opening)
        closing_cnt = len(closing)

        if opening_cnt == 0 or closing_cnt == 0:
            report.warn(line = None, msg = 'CONFIG: Empty "opening" and "closing" arrays.')
            return report
        if opening_cnt != closing_cnt:
            report.error(line = None, msg = 'CONFIG: Both "opening" and "closing" arrays must contain the same number of elements.')
            return report

        # We do that check at the end to ensure config is validated first.
        if not translation.items:
            return report

        for idx, item in enumerate(translation.items):
            # Do not try to be clever and filter() data first, because line_number values will no longer be correct.
            if not isinstance(item, (Translation, Comment)):
                continue

            stack: List[Bracket] = []
            has_errors = False
            for char_idx, current_char in enumerate(item.value):
                position: str = f'{idx + 1}:{char_idx + 1}'

                if current_char in opening:
                    # Every opening brace is pushed to the stack.
                    stack.append(Bracket(char_idx, current_char))
                    continue

                if current_char in closing:
                    # Every closing brace should take its own pair off the stack

                    if not stack:
                        # If stack is empty, then we had more closing brackets than opening ones.
                        report.create(position, f'No opening character matching "{current_char}".', item.key)
                        # Just show single error per line to avoid flooding.
                        has_errors = True
                        break

                    # Check if what we are about to pop from the stack and see if our current_char matches.
                    expected = closing[opening.index(stack[-1].bracket)]
                    if current_char == expected:
                        stack.pop()
                        continue

                    # This is not the bracket we were looking for...
                    report.create(position, f'Expected "{expected}", found "{current_char}".', item.key)
                    # Just show single error per line to avoid flooding.
                    has_errors = True
                    break

            if not has_errors and stack:
                # Just show single error per line to avoid flooding.
                bracket = stack[0]
                position: str = f'{idx + 1}:{bracket.pos + 1}'
                report.create(position, f'No closing character for "{bracket.bracket}" found.', item.key)

        return report

    @overrides(Check)
    def get_default_config(self) -> Dict:
        return {
            # Keep matching elements at the same positions
            'opening': ['(', '[', '<', '{'],
            'closing': [')', ']', '>', '}'],
        }
