"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""
import argparse
from pathlib import Path

from proptool.log import Log
from proptool.config_reader import ConfigReader
from proptool.config import Config
from proptool.const import Const
from proptool.utils import Utils


class ConfigBuilder(object):
    # List of options that can be either turned on or off.
    _onoff_pairs = [
        'fatal',
        'strict',
        'quiet',
        'verbose',
        'color',
    ]

    @staticmethod
    def build():
        # get default config
        config = Config()

        args = ConfigBuilder._parse_args()

        if args.config_file:
            config_file = Path(args.config_file[0])
            # override with loaded user config file
            config = ConfigReader().read(config, config_file)

        # override with command line arguments
        config = ConfigBuilder._set_from_args(config, args)

        ConfigBuilder._validate(config)

        return config

    @staticmethod
    def _validate(config: Config) -> None:
        if not config.files:
            Log.abort('No base file(s) specified.')
        if not config.languages:
            Log.abort('No language(s) specified.')
        if config.separator not in Config.ALLOWED_SEPARATORS:
            Log.abort('Invalid separator character.')
        if config.comment_marker not in Config.ALLOWED_COMMENT_MARKERS:
            Log.abort('Invalid comment marker.')

    @staticmethod
    def _set_onoff_option(config: Config, args, option: str) -> Config:
        """
        Changes Config's entry if either --<option> or --<no-option> switch is set.
        If none is set, returns Config object unaltered.
        :param config:
        :param args:
        :param option:
        :return:
        """
        if args.__getattribute__(option):
            config.__setattr__(option, True)
        elif args.__getattribute__(f'no_{option}'):
            config.__setattr__(option, False)
        return config

    @staticmethod
    def _set_from_args(config: Config, args) -> Config:
        # At this point it is assumed that args are in valid state (i.e. no mutually exclusive options are both set etc).

        for option in ConfigBuilder._onoff_pairs:
            config = ConfigBuilder._set_onoff_option(config, args, option)

        config.fix = args.fix
        config.languages = args.languages

        config.separator = args.separator
        config.comment_marker = args.comment
        config.comment_template = args.comment_template

        # base files
        suffix = '.properties'
        suffix_len = len(suffix)
        if args.files:
            for file in args.files:
                if file[suffix_len * -1:] != suffix:
                    file += suffix
                Utils.add_if_not_in_list(config.files, str(Path(file)))

        # languages
        if args.languages:
            Utils.add_if_not_in_list(config.languages, args.languages)

        return config

    @staticmethod
    def _parse_args() -> argparse:
        parser = argparse.ArgumentParser(prog = Const.APP_NAME.lower(), formatter_class = argparse.RawTextHelpFormatter,
                                         description = '\n'.join(Const.APP_DESCRIPTION))

        group = parser.add_argument_group('Base options')
        group.add_argument('--config', action = 'store', dest = 'config_file', nargs = 1, metavar = 'FILE',
                           help = 'Use specified config file. Note: command line arguments can override config!')
        group.add_argument('-b', '--base', action = 'store', dest = 'files', nargs = '+', metavar = 'FILE',
                           help = 'List of base files to check.')
        group.add_argument('-l', '--lang', action = 'store', dest = 'languages', nargs = '+', metavar = 'LANG',
                           help = 'List of languages to check (space separated if more than one, i.e. "de pl").')

        group = parser.add_argument_group('Additional options')
        group.add_argument('--fix', action = 'store_true', dest = 'fix',
                           help = 'Updated translation files in-place. No backup!')
        # group.add_argument('--pe', '--punctuation-exception', dest = 'punctuation_exception_langs', nargs = '*', metavar = 'LANG',
        #                    help = 'List of languages for which punctuation mismatch should not be checked for, i.e. "jp"')
        group.add_argument('--separator', action = 'store', dest = 'separator', metavar = 'CHAR', nargs = 1, default = '=',
                           help = 'If specified, only given CHAR is considered a valid key/value separator.'
                                  + f'Must be one of the following: {", ".join(Config.ALLOWED_SEPARATORS)}')
        group.add_argument('--comment', action = 'store', dest = 'comment', metavar = 'CHAR', nargs = 1, default = '#',
                           help = 'If specified, only given CHAR is considered valid comment marker.'
                                  + f'Must be one of the following: {", ".join(Config.ALLOWED_COMMENT_MARKERS)}')
        group.add_argument('-t', '--template', action = 'store', dest = 'comment_template', metavar = 'TEMPLATE', nargs = 1,
                           default = Config.DEFAULT_COMMENT_TEMPLATE,
                           help = f'Format of commented-out entries. Default: "{Config.DEFAULT_COMMENT_TEMPLATE}".')

        group = parser.add_argument_group('Checks controlling options')
        group.add_argument('-s', '--strict', action = 'store_true', dest = 'strict',
                           help = 'Enables strict validation mode for all checks involved.')
        group.add_argument('-ns', '--no-strict', action = 'store_true', dest = 'no_strict',
                           help = 'Disables strict validation mode for all checks involved (default).')

        group.add_argument('-f', '--fatal', action = 'store_true', dest = 'fatal',
                           help = 'Enables strict mode. All warnings are treated as errors and are fatal.')
        group.add_argument('-nf', '--no-fatal', action = 'store_true', dest = 'no_fatal',
                           help = 'Warnings are non-fatal, errors are fatal (default).')

        group = parser.add_argument_group('Application controls')
        group.add_argument('-q', '--quiet', action = 'store_true', dest = 'quiet',
                           help = 'Enables quiet mode, mutting all output but fatal errors.')
        group.add_argument('-nq', '--no-quiet', action = 'store_true', dest = 'no_quiet',
                           help = 'Disables quiet mode, enabling all type of messages (default).')
        group.add_argument('-v', '--verbose', action = 'store_true', dest = 'verbose',
                           help = 'Produces more verbose reports.')
        group.add_argument('-nv', '--no-verbose', action = 'store_true', dest = 'no_verbose',
                           help = 'Disables verbose mode, so only crucial messages are shown (default).')
        group.add_argument('-d', '--debug', action = 'store_true', dest = 'debug',
                           help = 'Enables debug output.')
        group.add_argument('-nd', '--no-debug', action = 'store_true', dest = 'no_debug',
                           help = 'Disables additional debug output (default).')

        group.add_argument('-c', '--color', action = 'store_true', dest = 'color',
                           help = 'Enables use of ANSI colors (default).')
        group.add_argument('-nc', '--no-color', action = 'store_true', dest = 'no_color',
                           help = 'Disables use of ANSI colors.')

        group = parser.add_argument_group('Misc')
        group.add_argument('--version', action = 'store_true', dest = 'show_version',
                           help = 'Displays application version details and quits.')

        args = parser.parse_args()

        # Check use of mutually exclusive pairs
        for key in ConfigBuilder._onoff_pairs:
            if args.__getattribute__(key) and args.__getattribute__(f'no_{key}'):
                parser.error(f'You cannot use "--{key}" and "--no-{key}" at the same time.')

        # Separator character.
        separator = args.separator[0]
        if separator not in Config.ALLOWED_SEPARATORS:
            parser.error(f'Invalid separator. Must be one of the following: {", ".join(Config.ALLOWED_SEPARATORS)}')

        # Comment marker character.
        comment = args.comment[0]
        if comment not in Config.ALLOWED_COMMENT_MARKERS:
            parser.error(f'Invalid comment marker. Must be one of the following: {Config.ALLOWED_COMMENT_MARKERS}')

        # Comment template.
        for placeholder in ('COM', 'SEP', 'KEY'):
            if args.comment_template.find(placeholder) == -1:
                parser.error(f'Missing literal in comment template: {placeholder}')

        return args
