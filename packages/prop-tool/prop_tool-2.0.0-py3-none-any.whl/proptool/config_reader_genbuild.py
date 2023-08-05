import argparse
import collections
import json
import os
from typing import List

from log import Log
from utils import Utils

import ConfigParser
from utils import Utils


class ConfigReader(object):
    # Config.USER_FOLDER = Config.DEFAULT_USER_FOLDER
    project_relative_dir = None
    sandcastle_root_dir = None
    project_name = None
    user_config_file = None
    tool_dir = None
    target = None
    project_dir = None
    user_name = None
    project_config = None

    CONFIG_VERSION = 2

    IGNORED_LIBS = []
    IGNORED_FLAGS = []
    LIB_TO_MODULE_MAP = collections.OrderedDict()
    DEFINE_TO_MODULE_MAP = collections.OrderedDict()
    INCLUDE_TO_MODULE_MAP = collections.OrderedDict()
    INCLUDE_TO_MODULE_KEY_PLAIN = []
    INCLUDE_TO_MODULE_KEY_REGEXP = []
    IGNORED_INCLUDES = []
    SMAKE_KEYS_MAP = collections.OrderedDict()
    CL_CC = []
    CL_REVIEWERS = []
    CL_DESCRIPTION_FOOTER = []
    CL_BUG_ID = None
    CL_RELEASE_CL = None
    IGNORED_PROTOBUF_IMPORTS = []
    SERVICE_DEPENDENCIES = {
        'erpc': [],
    }
    G3_TO_D3_FOLDER_MAP = {}

    # do NOT edit these defaults. Modify config.ini instead if needed
    IGNORED_INCLUDES_IN_D_FILE = [
        "^/google/src/files",
        "^/usr/local/google/outdir-.*/rootfs/.*",
        "^/usr/local/google/outdir-.*/linux/uapi/.*",
        ".*depot/google3/third_party/crosstool/v18/stable/gcc-x86_64-grtev4-linux-gnu/.*",
        ".*depot/google3/third_party/grte/v4_x86/release/usr/grte/v4/+include/.*",
    ]

    # ***************************************************************************

    INI_MAIN_KEY = 'prop-tool'
    INI_KEY_LISTS = 'lists'

    ini_maps = [
        'smake_keys_map',
        'lib_to_module_map',
        'include_to_module_map',
        'define_to_module_map',
        'g3_to_d3_folder_map',
    ]

    ini_keys = collections.OrderedDict([
        (INI_KEY_LISTS, ['ignored_libs',
                         'ignored_flags',
                         'ignored_includes',
                         'citc_release_clients',
                         'ignored_protobuf_imports',
                         'ignored_includes_in_d_file',
                         ]),
        (INI_KEY_CL, ['cl_cc',
                      'cl_reviewers',
                      'cl_description_footer',
                      'cl_bug_id',
                      'cl_release_cl',
                      ]),
    ])

    # ***************************************************************************

    REPO_PATH = '/google/data/rw/teams/sandblaze2.0/genbuild/'


    USER_FOLDER = '~/.genbuild/'
    DEFAULT_CONFIG_FILE_NAME = 'config.ini'
    USER_CONFIG_FILE_NAME_PATTERN = 'config-{username}.ini'
    MAKE_VAR_DUMP_NAME = 'make_var_dump.txt'
    BUILD_FILE_NAME = 'BUILD'
    PROJECT_NOTES_IN_G3_FILE_NAME = ".sandblaze_notes"
    CITC_RELEASE_CLIENTS = []

    RECENT_PATCH_LINK_NAME_PATTERN = 'genbuild_recent_{user}'

    PATCH_FILE_NAME = 'patch'
    PATCH_CONFIG_FILE_NAME = 'patch.ini'
    PATCH_LOG_FILE_NAME = 'patch.log'
    PATCH_OVERVIEW_FILE_NAME = 'overview.ini'
    PATCH_NOTES_FILE_NAME = 'patch_notes.txt'
    PATCH_APP_CONFIG_FILE_NAME = 'genbuild.ini'

    PATCH_FILE_NAME_PATTERN = 'sb.{stamp}_{user}.patch'
    PATCH_FILE_NAME_REGEXP = r'sb.\d{8}\-\d{6}_\w*\.patch'
    PATCH_NOTES_NAME_PATTERN = 'sb.{stamp}_{user}.notes'
    PATCH_NOTES_NAME_REGEXP = r'sb.\d{8}\-\d{6}_\w*.notes'
    PATCH_LOG_NAME_PATTERN = 'sb.{stamp}_{user}.log'
    PATCH_LOG_NAME_REGEXP = r'sb.\d{8}\-\d{6}_\w*.log'
    PATCH_CONFIG_NAME_PATTERN = 'sb.{stamp}_{user}.ini'
    PATCH_CONFIG_NAME_REGEXP = r'sb.\d{8}\-\d{6}_\w*.ini'
    PATCH_APP_CONFIG_NAME_PATTERN = 'sb.{stamp}_{user}.genbuild.ini'
    PATCH_APP_CONFIG_NAME_REGEXP = r'sb.\d{8}\-\d{6}_\w*.genbuild.ini'

    OVERLAY_LIST_GENERAL_FILTER_REGEXP = r'sb.\d{8}\-\d{6}_{user}\..*'
    OVERLAY_LIST_PATCH_FILE_FILTER_REGEXP = r'sb.\d{8}\-\d{6}_{user}\.patch'
    OVERLAY_LIST_PATCH_CONFIG_FILE_FILTER_REGEXP = r'sb.\d{8}\-\d{6}_{user}\.ini'
    OVERLAY_LIST_PATCH_NOTES_FILE_FILTER_REGEXP = r'sb.\d{8}\-\d{6}_{user}\.notes'
    OVERLAY_LIST_PATCH_LOG_FILE_FILTER_REGEXP = r'sb.\d{8}\-\d{6}_{user}\.log'
    OVERLAY_LIST_APP_CONFIG_FILE_FILTER_REGEXP = r'sb.\d{8}\-\d{6}_{user}\.genbuild\.ini'

    # ***************************************************************************

    def __init__(self, args: argparse):
        pass

    # command line args and project name
    # Config.tool_dir = os.path.dirname(os.path.realpath(__file__))
    # Config.project_dir = os.getcwd()

    # it we have config file names provided, we will load just these configs
    # if args.config is not None:
    #   for config_file in args.config:
    #     if not self.__load_config_ini('custom', os.path.expanduser(config_file), mute_config_load):
    #       Log.abort('Failed to load config %r' % config_file)
    # else:
    #   # if no config file is specified we will load default tool config and user config (if exists) over it
    #   # load default settings first from tool's home directory
    #   config_file = '%s/../%s' % (Config.tool_dir, Config.DEFAULT_CONFIG_FILE_NAME)
    #   if not self.__load_config_ini('default', config_file, mute_config_load):
    #     Log.abort('Failed to load default config %r' % config_file)
    #
    #   cfg = Config.USER_CONFIG_FILE_NAME_PATTERN.format(username=Config.user_name)
    #   config_file = os.path.join(Config.USER_FOLDER, cfg)
    #   if self.__load_config_ini('user', config_file, mute_config_load):
    #     Config.user_config_file = config_file

    # ***************************************************************************

    def __load_config_ini(self, log_label, config_file_name, fail_if_not_found = False):
        """Reads data from given configuration INI file.

        Args:
          log_label: config type to be logged when file is loaded
          config_file_name: name of configuration file to read
          mute: if True, not config loading progress logs would be emitted
          fail_if_not_found: if True, abort() will be called if file is missing. When False, warning will show up only.

        Returns:
          True if read it correctly, False if file does not exists. Aborts for
          any fatal error.
        """

        log_label = log_label.upper()

        config_file_name = os.path.normpath(config_file_name)
        config_file_name_full = os.path.expanduser(config_file_name)

        if not os.path.isfile(config_file_name_full):
            error_msg = '[%s] Not found %r' % (log_label, config_file_name)
            if not fail_if_not_found:
                Log.i(error_msg)
                return False
            else:
                Log.abort(error_msg)

        Log.level_push('[%s] %s' % (log_label, config_file_name))

        config = ConfigParser.ConfigParser()
        # prevent keys CaSe from being altered by default implementation
        config.optionxform = str

        # noinspection PyBroadException
        try:
            config.read(config_file_name_full)
        except:
            # noinspection PyUnresolvedReferences
            # ex = sys.exc_info[0]
            Log.abort([
                'Failed parsing config INI file',
                '[%s] %r' % (log_label, config_file_name),
                # 'Error %r' % ex.message,
            ])

        config_version = 0
        if config.has_section('genbuild'):
            config_version = config.getint('genbuild', 'version')

        if config_version < Config.CONFIG_VERSION:
            Log.abort('Old version (v%d) of config INI file. Please convert/update it first!' % config_version)

        Config.IGNORED_LIBS = self.__merge_list(Config.IGNORED_LIBS, config, 'ignored_libs')
        Config.LIB_TO_MODULE_MAP = self.__merge_dict(Config.LIB_TO_MODULE_MAP, config, 'lib_to_module_map')

        cl_section = 'cl'
        if config.has_section(cl_section):
            Config.CL_CC = self.__merge_list(Config.CL_CC, config, 'cl_cc', cl_section)
            Config.CL_REVIEWERS = self.__merge_list(Config.CL_REVIEWERS, config, 'cl_reviewers', cl_section)
            Config.CL_DESCRIPTION_FOOTER = self.__merge_list(Config.CL_DESCRIPTION_FOOTER, config, 'cl_description_footer',
                                                             cl_section)
            if config.has_option(cl_section, 'cl_bug_id'):
                Config.CL_BUG_ID = config.getint(cl_section, 'cl_bug_id')
            if config.has_option(cl_section, 'cl_release_cl'):
                Config.CL_RELEASE_CL = config.getint(cl_section, 'cl_release_cl')

        # no longer needed. We shall remove this
        section = 'service_dependencies'
        if config.has_section(section):
            for service_type in Config.SERVICE_DEPENDENCIES.keys():
                if config.has_option(section, service_type):
                    Config.SERVICE_DEPENDENCIES[service_type] = self.__merge_list(Config.SERVICE_DEPENDENCIES[service_type], config,
                                                                                  section,
                                                                                  service_type)

        # this map needs special treatment as we want to split the data into two separate lists
        # one with exact matching strings and the other with regular expressions
        if config.has_section('include_to_module_map'):
            for (key, val) in dict(config.items('include_to_module_map')).items():
                k = Utils.remove_quotes(key)
                v = Utils.remove_quotes(val)
                # first, make entry in global lookup table
                Config.INCLUDE_TO_MODULE_MAP[k] = v

                # then create helper key in dedicated table
                if Utils.is_regexp(k):
                    Config.INCLUDE_TO_MODULE_KEY_REGEXP.append(k)
                else:
                    Config.INCLUDE_TO_MODULE_KEY_PLAIN.append(k)

        return True

    # ***************************************************************************

    def __merge_list(self, old_list: List, ini_parser, option: str, section = 'lists') -> List:
        section_name_shown = False
        result = old_list

        if ini_parser.has_option(section, option):
            val = ini_parser.get(section, option).replace('\n', '')
            new_list = json.loads(val)
            if new_list is not None:
                for i in new_list:
                    if i[0:4] == 'DEL ':
                        if not section_name_shown:
                            Log.level_push('%%yellow_bright%%**WARN**%r list' % option)
                            section_name_shown = True

                        val = i[4:]
                        result.remove(val)
                    else:
                        Utils.add_if_not_in_list(result, Utils.remove_quotes(i))

            if section_name_shown:
                Log.level_pop()

        return result

    # ***************************************************************************

    def __merge_dict(self, old_dict, ini_parser, section):
        section_name_shown = False
        result = old_dict

        if ini_parser.has_section(section):
            new_dict = dict(ini_parser.items(section))

            if new_dict is not None:
                for (k, v) in new_dict.items():
                    v = Utils.remove_quotes(v)

                    # if key starts with "DEL " then value does not matter and such key is REMOVED from internal storage
                    if k[0:4] == 'DEL ':
                        key = k[4:]
                        if key in result:
                            if not section_name_shown:
                                # Log.level_push('%%yellow_bright%%**WARN**%r map' % section)
                                section_name_shown = True
                            del result[key]
                        continue

                    if k in old_dict and result[k] != v:
                        if not section_name_shown:
                            # Log.level_push('%%yellow_bright%%**WARN**%r map' % section)
                            section_name_shown = True

                        # Log.push('%%yellow%%%s has different values configured:' % k)
                        # Log.i(['%%red%%Old: %s' % result[k],
                        #        '%%green%%New: %s' % v,
                        #        ])
                        # Log.level_pop()
                    result[k] = v

        if section_name_shown:
            Log.level_pop()

        return result

    def __sanitize_dict(self, src_dict):
        import collections

        tmp = collections.OrderedDict()
        for (k, v) in src_dict.items():
            tmp[Utils.remove_quotes(k)] = Utils.remove_quotes(v)
        return tmp

    # ***************************************************************************

    # noinspection PyUnresolvedReferences
    @staticmethod
    def __prepare_config_entry(key_ini):
        from logger.log import Log

        result = ''

        key = key_ini.upper()
        exec('tmp = Config.' + key)

        if isinstance(tmp, list):
            result = Config.gen_ini_list(key_ini, tmp)
        elif isinstance(tmp, int):
            result = ['%s = %d' % (key_ini, tmp)]
        elif isinstance(tmp, dict):
            result = Config.gen_ini_dict(key_ini, tmp)
        else:
            Log.abort('Unknown type of %r' % key)

        return result

    # ***************************************************************************

    @staticmethod
    def gen_ini_list(key, elements):
        """Generates INI list.

        Args:
          key: dictionary INI list key name
          elements: list data

        Returns:
          List of INI text rows generated
        """
        tmp = ['%s = [' % key]
        indent = 4
        idx = 1
        for item in elements:
            sep = ',' if idx < len(elements) else ''
            tmp.append((' ' * indent) + ('"%s"%s' % (item, sep)))
            idx += 1
        tmp.extend([(' ' * indent) + ']', ''])
        return tmp

    # ***************************************************************************

    @staticmethod
    def gen_ini_dict(section, val):
        """Generates INI dictionary.

        Args:
          section: dictionary INI section name
          val: dictionary data

        Returns:
          List of INI text rows generated
        """
        tmp = ['[%s]' % section]
        for (k, v) in val.items():
            tmp.append('%s : %s' % (k, v))
        tmp.append('')
        return tmp

    # ***************************************************************************

    # noinspection PyUnresolvedReferences,PyUnusedLocal
    @staticmethod
    def config_print(__unused__):
        """Dumps important configuration parameters into log.

        Args:
          __unused__: unused. Present to satisfy "interface"

        Returns:
          Boolean
        """
        from logger.log import Log
        from utils import Utils

        for (k, elements) in Config.ini_keys.items():
            Config.__print(elements)

        Config.__print(Config.ini_maps)

        return True

    # ***************************************************************************

    # noinspection PyUnresolvedReferences,PyUnusedLocal
    @staticmethod
    def __print(config_var_names_list):
        for key in config_var_names_list:
            key = key.upper()
            exec('tmp = Config.' + key)
            if isinstance(tmp, list):
                Log.level_push('%s%s [%d]' % (Log.COLOR_NOTICE, key, len(tmp)))
                if tmp:
                    Log.i(tmp)
                else:
                    Log.n('No custom rules')
                Log.level_pop()
            elif isinstance(tmp, int):
                Log.i('%s = %d' % ('%green%' + key + '%reset%', tmp))
            elif isinstance(tmp, dict):
                Log.level_push('%s%s [%d]' % (Log.COLOR_NOTICE, key, len(tmp)))
                Log.i(Utils.to_list(tmp) if tmp else 'No custom mapping')
                Log.level_pop()
            else:
                Log.w('Unknown type of %r' % key)
