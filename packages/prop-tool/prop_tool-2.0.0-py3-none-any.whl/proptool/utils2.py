"""Utils module for BUILD file generator for depot3 to google3 project.

Utils module for BUILD file generator for depot3 to google3 automated
conversion project

Marcin Orlowski <orlowskim@google.com>
"""
import os
import re
import sys

import datetime
import time

from logger.log import Log

class Utils(object):
  """Utils module.
  """

  @staticmethod
  def get_relative_path(base_dir, src_dir, use_dot_folder=True):
    """Returns relative path to cwd for given absolute base path.

    Args:
      base_dir: base directory to make path relative to
      src_dir: directory to make relative
      use_dot_folder: if True, returned relative path will be prefixed with './'
      if result path is either empty string or starts with '/'. If False,
      empty string will be used instead of './'

    Returns:
      string with relative representation of the src_dir path
    """

    dot_folder = './' if use_dot_folder else ''

    # FIXME(orlowskim): temporary workaround, as ../ is invalid path anyway
    if src_dir[0:2] == '../':
      return src_dir

    result = os.path.abspath(src_dir).replace(os.path.abspath(base_dir), '')
    if not result:
      result = dot_folder
    else:
      if result[0:1] == '/':
        result = result.replace('/', dot_folder, 1)
    return result

  @staticmethod
  def exists_not_empty(key, dictionary):
    """Checks if given key exists in dict and is not empty.

    Args:
        key: key to look for
        dictionary: dict to dig in

    Returns:
      Returns True if key exists in dict AND contains any data.
    """
    return (key in dictionary) and dictionary[key]



  @classmethod
  def map_define(cls, define, no_none=False):
    """Maps compiler defines to blaze module.

    Tries to map defines (set via -DFOO=VAR) to blaze module, i.e.
    FOO=X becomes //third_party/foo dependency

    Args:
      define: define name to check mapping for
      no_none: when True, then returns lib argument if no mapping is found. When False, returns None

    Returns:
      Mapped define name or None
    """
    from config import Config

    mapped_name = Config.DEFINE_TO_MODULE_MAP.get(define)

    # no direct mapping, let's try regexps
    if mapped_name is None:
      for (regexp, module) in Config.DEFINE_TO_MODULE_MAP.items():
        if re.match(regexp, define) is not None:
          mapped_name = module
          break

    if mapped_name is None and no_none:
      mapped_name = define

    return mapped_name

  @classmethod
  def map_library(cls, lib, no_none=False):
    """Maps linkable library to blaze module.

    Tries to map linkable library to blaze module, i.e.
    gflags becomes //third_party/gflags dependency

    Args:
      lib: library name to check mapping for
      no_none: when True, then returns lib argument if no mapping is found. When False, returns None

    Returns:
      Mapped Blaze module name or None
    """
    from config import Config

    mapped_lib = Config.LIB_TO_MODULE_MAP.get(lib)

    if mapped_lib is None and no_none:
      mapped_lib = lib

    return mapped_lib

  @staticmethod
  def to_list(data):
    """Converts certain data types (str, unicode) into list.

    Args:
      data: data to convert

    Returns:
      list with converted data
    """
    # variable types to be converted
    str_types = [str]

    # for pre 3.x we add 'unicode' type as well
    if sys.version_info[0] < 3:
      # noinspection PyTypeChecker
      str_types.append(unicode)

    for data_type in str_types:
      if isinstance(data, data_type):
        return [data]

    return data

  @staticmethod
  def dict_to_list(data_to_convert, color=None):
    """Converts dictionary elements into list.

    Args:
      data_to_convert: dictionary to convert
      color: color code (i.e. '%red%' for each row)

    Returns:
      list with converted data.

    """
    if not isinstance(data_to_convert, dict):
      return data_to_convert

    array = []
    for (key, val) in data_to_convert.items():
      if color is not None:
        array.append('{color}{key}%reset% : {val}'.format(color=color, key=key, val=val))
      else:
        array.append('%s: %s' % (key, val))
    return array


  @staticmethod
  def sanitize_dependency_name(name):
    """Converts name to usable valid dependency name, i.e. FOO.bar => foo_bar.

    Args:
      name: name to be sanitized

    Returns:
      converted name
    """
    return name.replace('.', '_').lower()

  @staticmethod
  def make_blaze_dependency_name(name):
    """Converts filename to Blaze dependency name, i.e. FOO.bar => :foo_bar.

    Args:
      name: name to be converted to valid Blaze dependency name

    Returns:
      converted name
    """
    return ':%s' % Utils.sanitize_dependency_name(name)

  @staticmethod
  def is_regexp(string):
    """Checks if given string uses regexp meta chars.

    Args:
      string: string to check

    Returns:
      boolean
    """
    regexp = '^.*[\^\$\*\+\?\{\}\[\]\\\|\(\)].*$'
    return True if re.match(regexp, string) is not None else False

  @staticmethod
  def parse_libs(libs, log_label=None):
    """Processes dependency libs.

    Processes array of dependency libraries, returning ready to use array
    of Blaze dependencies

    Args:
      libs: list of libs to process
      log_label: optional log label

    Returns:
      Array of processed libraries
    """
    from target import Target
    from args import Args
    from config import Config

    if log_label is not None:
      Log.level_push(log_label)

    processed = []
    for lib_name in libs:
      lib = Utils.get_lib_name_from_linked(lib_name)

      # filter some libs out
      if lib in Config.IGNORED_LIBS is not None:
        Log.n('%s => [SKIPPED, IGNORED_LIBS:%s]' % (
            lib, Config.IGNORED_LIBS.index(lib) + 1))
        continue

      # check if we got such target locally
      target = Target.get_by_name(lib)
      if target is not None:
        mapped_lib = Utils.make_blaze_dependency_name(target.get_name())
      else:
        # nope, check if we can use mapping for it then
        mapped_lib = Utils.map_library(lib)

      if mapped_lib is None:
        Log.e('Unhandled library dependency for %r' % lib)
        if not Args.args.ignore_errors:
          Log.abort()
        else:
          mapped_lib = []

      for (idx, mapped) in enumerate(Utils.to_list(mapped_lib)):
        label = ' [LOCAL]' if mapped[0:1] == ':' else ''
        Log.v((lib if idx == 0 else ' ' * len(lib)) + ' => ' + mapped + label)
        Utils.add_if_not_in_list(processed, mapped)

    if log_label is not None:
      Log.level_pop()

    return processed

  @staticmethod
  def map_make_vars_key(key):
    """Maps smake dump file keys (in case these are remapped in config file.

    Args:
      key: key to map

    Returns:
      returns mapped key
    """
    from config import Config

    if key in Config.SMAKE_KEYS_MAP:
      key = Config.SMAKE_KEYS_MAP[key]

    return key

  # ***************************************************************************

  @staticmethod
  def merge_into_list(target, source):
    """Merges target list with source list. Preserves existing data.

    Args:
      target: target list to add items to
      source: source list

    Returns:
      int - number of elements skipped (not added) due to being duplicate
    """
    if not isinstance(target, list):
      raise RuntimeError('List target expected. %r found.' % type(target))
    if not isinstance(source, list):
      raise RuntimeError('List source expected. %r found.' % type(source))

    count = 0
    for item in source:
      if not Utils.add_if_not_in_list(target, item):
        count += 1

    return count

  @staticmethod
  def merge_into_dict(target, source):
    """Merges dict target with source dict. Preserves existing data.

    Args:
      target: target dict to add items to
      source: source dict

    Returns:
      int - number of elements skipped (not added) due to being duplicate
    """
    if not isinstance(target, dict):
      raise RuntimeError('Dict target expected. %r found.' % type(target))
    if not isinstance(source, dict):
      raise RuntimeError('Dict source expected. %r found.' % type(source))

    count = 0
    for (key, val) in source.items():
      if not Utils.add_if_not_in_dict(target, key, val):
        count += 1

    return count

  @staticmethod
  def get_formatted_stamp(millis=None, format=None):
    if millis is None:
      millis = Utils.now()

    timezone = time.tzname[time.daylight]

    if format is None:
      formatted = datetime.datetime.fromtimestamp(millis).strftime('%Y %b %d, %H:%M:%S') + ' ' + timezone
    else:
      formatted = datetime.datetime.fromtimestamp(millis).strftime(format)

    return formatted

  @staticmethod
  def now():
    return time.mktime(datetime.datetime.now().timetuple())

  # ***************************************************************************

  @staticmethod
  def cmd(cmd_list, working_dir=None):
    """Executes commands from cmd_list changing CWD to working_dir.

    Args:
      cmd_list: list with command i.e. ['g4', '-option', ...]
      working_dir: if not None working directory is set to it for cmd exec

    Returns: rc of executed command (usually 0 == success)
    """
    from subprocess import Popen, PIPE
    from args import Args

    rc = 0

    if working_dir:
      old_cwd = os.getcwd()
      os.chdir(working_dir)

    Log.d('Invoking: ' + ' '.join(cmd_list))

    if not Args.args.dry_run:
      p = Popen(cmd_list, stdin=PIPE, stdout=PIPE, stderr=PIPE)
      output, err = p.communicate(None)
      rc = p.returncode

      if rc == 0:
        if Args.args.verbose:
          Log.i('%%yellow%%OK. Output of %r' % ' '.join(cmd_list),)
          Log.i('+' + '-' * 30, Log.ANSI_YELLOW)
          [Log.i('| %s' % o, Log.ANSI_YELLOW) for o in output.splitlines()]
          Log.i('+' + '-' * 30, Log.ANSI_YELLOW)

      else:
        Log.level_push('%%red%%FAIL. Output of %r' % ' '.join(cmd_list), )
        Log.i('+' + '-' * 30, Log.ANSI_RED)
        [Log.i('| %s' % o, Log.ANSI_RED) for o in output.splitlines()]
        Log.i('+' + '-' * 30, Log.ANSI_RED)
        Log.level_pop()

        Log.e([
          'Command failed. Return code %d. Command:' % p.returncode,
          '  %s' % ' '.join(cmd_list),
        ])

        if Args.args.ignore_errors:
          Log.e('NOT aborting, due to --ignore-errors used')
        else:
          Log.abort()

    if working_dir:
      # noinspection PyUnboundLocalVariable
      os.chdir(old_cwd)

    return rc

  # ***************************************************************************

  @staticmethod
  def path_to_depot(path):
    """Converts /full/path/to/citc/workspace/something to //depot/something.
    Args:
      path: path to convert
    """
    from config import Config

    return re.sub(r'^/google/src/cloud/%s/.*?/(.*)$' % Config.user_name, r'//depot/\1', path)

  # ***************************************************************************

  @staticmethod
  def format_name(name_pattern, millis=None):
    from config import Config

    _time = Utils.__format('%H%M%S', millis)
    _date = Utils.__format('%Y%m%d', millis)
    _stamp = Utils.__format('%Y%m%d-%H%M%S', millis)

    return name_pattern.format(
      time=_time, date=_date, stamp=_stamp, user=Config.user_name
    )

  @staticmethod
  def __format(name_pattern, millis):
    if millis is None:
      millis = Utils.now()
    return datetime.datetime.fromtimestamp(millis).strftime(name_pattern)

  # ***************************************************************************

  @staticmethod
  def citc_setup_valid_or_abort(path):
    """Ensures certain CitC client settings are configred as expected.
    If not, Log.abort() is called

    Args:
      path: path to location within valid CitC client
    """
    import subprocess
    from args import Args

    if Args.args.debug_no_checks:
      Log.w('CitC setup validation skipped due to --no-checks')
      return

    cloud_dir_pattern = (r'^/google/src/cloud/(\w*)/(.*)/'
                         r'(depot3|google3)/platforms/networking/'
                         r'(sandcastle|sandblaze).*$')
    dm = re.match(cloud_dir_pattern, path)
    if dm is None:
      Log.abort('You must be in valid CitC client folder')

    citc_owner = dm.group(1)
    citc_name = dm.group(2)

    Log.n('CitC client: %r' % citc_name)
    patch_cmd = ['g4', 'client', '-o', citc_name]

    output = ''
    try:
      output = subprocess.check_output(patch_cmd)
    except subprocess.CalledProcessError:
      Log.abort([
        'Command failed. Try:',
        '  %s' % ' '.join(patch_cmd),
      ])

    Log.level_push('CitC client check details:')
    if not Args.args.ignore_errors:
      for line in output.splitlines():
        if line == '' or line[0:1] == '#':
          continue

        tmp = line.split()
        if tmp[0] == 'Options:':
          del tmp[0]
          if 'multichange' in tmp:
            Log.i('Multichange: OK')
          else:
            Log.abort([
              'CitC client %r must be in set to use "multichange". Enable it by:' % citc_name,
              '  g4 client --set_option multichange %s-%s' % (citc_owner, citc_name),
              'or use:',
              '  g4 user',
              'and save the file once "Options" section is adjusted.',
            ])
    else:
      Log.n('Check skipped because of --ignore-errors flag used')
    Log.level_pop()

  # ***************************************************************************

  @staticmethod
  def dir_in_depot3_or_googl3_or_abort(full_path, d3_allowed, g3_allowed):
    """Checks if current working dir is either/or in depot3/ or google3/ tree. Log.abort()s if not.

    Args:
      full_path: path to process
      d3_allowed: Log.abort() if set to False and full_path points to depot3/
      g3_allowed: Log.abort() if set to False and full_path points to google3/

    Returns:
      d3_dir: full path to package in depot3 dir (i.e. '/google/.../sandcastle/Foo/Bar)
      g3_dir: full path to package in google3 die (i.e. /google/.../sandblaze/foo/bar)
      citc_name: name of CitC workspace we are currently working in
    """
    from config import Config

    cloud_dir_pattern = r'^(/google/src/cloud/\w*/(.*)/)(depot3|google3)(/platforms/networking/)(sandcastle|sandblaze)(/.*)$'
    dm = re.match(cloud_dir_pattern, full_path)
    if dm is None:
      Log.abort('You must be in project\'s depot3/ or google3/ folder!')

    if not d3_allowed and dm.group(3) == 'depot3':
      Log.abort('You must be in project\'s google3/ folder!')

    if not g3_allowed and dm.group(3) == 'google3':
      Log.abort('You must be in project\'s depot3/ folder!')

    # in full_path points to google3, we need to map certain names to get right name for depot3
    d3_project_name = dm.group(6)
    for (name_from, name_to) in Config.G3_TO_D3_FOLDER_MAP.items():
      d3_project_name = d3_project_name.replace(name_from, name_to)

    d3_dir = '%s%s%s%s%s' % (dm.group(1), 'depot3', dm.group(4), 'sandcastle', d3_project_name)
    g3_dir = '%s%s%s%s%s' % (dm.group(1), 'google3', dm.group(4), 'sandblaze', dm.group(6).lower())
    citc_name = dm.group(2)

    return d3_dir, g3_dir, citc_name

  # ***************************************************************************

  @staticmethod
  def get_d3_dir(project_dir):
    from config import Config

    cloud_dir_pattern = r'^(/google/src/cloud/\w*/(.*)/)(depot3|google3)(/platforms/networking/)(sandcastle|sandblaze)(/.*)$'
    dm = re.match(cloud_dir_pattern, project_dir)
    if dm is None:
      Log.d(project_dir)
      Log.abort('Invalid project dir!')

    d3_project_name = dm.group(6)
    for (name_from, name_to) in Config.G3_TO_D3_FOLDER_MAP.items():
      d3_project_name = d3_project_name.replace(name_from, name_to)

    return '%s%s%s%s%s' % (dm.group(1), 'depot3', dm.group(4), 'sandcastle', d3_project_name)

  @staticmethod
  def get_g3_dir(project_dir):
    cloud_dir_pattern = r'^(/google/src/cloud/\w*/(.*)/)(depot3|google3)(/platforms/networking/)(sandcastle|sandblaze)(/.*)$'
    dm = re.match(cloud_dir_pattern, project_dir)
    if dm is None:
      Log.abort('Invalid project dir!')

    return '%s%s%s%s%s' % (dm.group(1), 'google3', dm.group(4), 'sandblaze', dm.group(6).lower())

  @staticmethod
  def get_project_name_from_dir(project_dir):
    cloud_dir_pattern = r'^(/google/src/cloud/\w*/(.*)/)(depot3|google3)(/platforms/networking/)(sandcastle|sandblaze)(/.*)$'
    dm = re.match(cloud_dir_pattern, project_dir)
    if dm is None:
      Log.abort('Invalid project dir!')

    return dm.group(6).lower()

  # ***************************************************************************

  @staticmethod
  def get_citc_name():
    """Returns CitC nameof current working dir if we are in right folder or None if not

    Returns:
      citc_name or None
    """
    from config import Config

    cloud_dir_pattern = r'^/google/src/cloud/\w*/(.*?).*$'
    dm = re.match(cloud_dir_pattern, Config.project_dir)
    return None if dm is None else dm.group(1)

  # ***************************************************************************

  @staticmethod
  def rebuild_smake_file(working_dir, project_config_obj=None):
    smake_cmd = ['smake', '-an', '--quiet']

    no_smake = False if project_config_obj is None else project_config_obj.get_no_smake()

    # noinspection PyArgumentList
    if not no_smake and project_config_obj:
      [smake_cmd.extend(['-G', var]) for var in project_config_obj.get_smake_vars()]

    Utils.cmd(smake_cmd, working_dir)

  # ***************************************************************************

  @staticmethod
  def remove_quotes(src_str):
    if len(src_str) >= 2:
      if src_str[0] == '"':
        src_str = src_str[1:]
      end_pos = src_str.rfind('"')
      if end_pos != -1:
        src_str = src_str[0:end_pos]

    return src_str
