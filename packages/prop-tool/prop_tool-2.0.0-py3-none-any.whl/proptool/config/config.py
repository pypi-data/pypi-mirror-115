"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""
from typing import Dict, List

from proptool.config.checker_info import CheckerInfo


class Config(object):
    VERSION = 1

    ALLOWED_SEPARATORS: List[str] = ['=', ':']
    ALLOWED_COMMENT_MARKERS: List[str] = ['#', '!']
    DEFAULT_FILE_SUFFIX: str = '.properties'

    # COM: comment marker
    # KEY: translation key
    # SEP: "key SEP value" separator
    # VAL: original string
    COMMENTED_TRANS_TPL: str = 'COM ==> KEY SEP VAL'
    COMMENTED_TRANS_REGEXP = r'^[{com}]\s*==>\s*{key}\s*[{sep}].*'.format(
        com = ''.join(ALLOWED_COMMENT_MARKERS),
        # must be in () brackets to form a group used later!
        key = r'([a-zAz][a-zA-z0-9_.-]+)',
        sep = ''.join(ALLOWED_SEPARATORS))

    def __init__(self):
        """
        NOTE: Do NOT put any non-configurable elements as Config's instance attributes as by design
        it is assumed that any attribute can be modified, while consts cannot.
        """
        self.config_file = None

        self.file_suffix = Config.DEFAULT_FILE_SUFFIX

        self.fatal = False

        self.debug = False
        self.color = True
        self.quiet: bool = False
        self.verbose: bool = False

        self.update: bool = False
        self.create: bool = False

        self.files: List[str] = []
        self.languages: List[str] = []

        self.separator: str = '='
        self.comment_marker: str = '#'

        self.checks: Dict[str, CheckerInfo] = {
            # empty set. Populated and manipulated by ConfigBuilder.
        }

    def set_checker_config(self, checker_id: str, config: Dict) -> None:
        self.checks[checker_id] = config

    def get_checker_config(self, checker_id: str) -> Dict:
        if checker_id not in self.checks:
            raise KeyError(f'No config for {checker_id} found.')
        return self.checks[checker_id]
