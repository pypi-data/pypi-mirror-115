"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""

from typing import List


class Config(object):
    VERSION = 1

    ALLOWED_SEPARATORS: List[str] = ['=', ':']
    ALLOWED_COMMENT_MARKERS: List[str] = ['#', '!']
    DEFAULT_COMMENT_TEMPLATE: str = 'COM ==> KEY SEP'

    def __init__(self):
        self.comment_marker: str = '#'
        self.comment_template: str = Config.DEFAULT_COMMENT_TEMPLATE
        self.debug = False
        self.debug_verbose = 1  # Log.VERBOSE_NORMAL
        self.fatal = False
        self.files: List[str] = []
        self.fix: bool = False
        self.languages: List[str] = []
        self.no_color = False
        self.quiet: bool = False
        self.separator: str = '='
        self.strict: bool = False
        self.verbose: bool = False

        self.checks = {
            'KeyFormat':   {
                'pattern': r'^[a-z]+[a-zA-Z0-9_.]*[a-zA-Z0-9]+$',
            },
            'Punctuation': {
                'chars': ['.', '?', '!', ':', r'\n'],
            },
        }
