from subprocess import Popen, PIPE
import json

import sublime

from . import preferences, pathutil


def _get_node_path():
    node = pathutil.find_executable(preferences.get_path(), 'node')
    if not node:
        raise Exception('Could not find Node.js. Check that your configuration is correct.')
    return node


def _get_sql_formatter_path():
    node = pathutil.find_executable(preferences.get_path(), 'sql-formatter')
    if not node:
        raise Exception('Could not find sql-formatter. Check that it is installed and that your configuration is correct.')
    return node


def format_sql(sql, dialect=None):
    cmd = None
    if sublime.platform() == 'windows':
        cmd = [_get_sql_formatter_path()]
    else:
        cmd = [_get_node_path(), _get_sql_formatter_path()]

    if not dialect:
        dialect = preferences.get_pref('default_dialect')

    if dialect:
        cmd.extend(['-l', dialect])

    # add config param
    if preferences.get_pref('use_tabs'):
        config = json.dumps({"useTabs": True}, separators=(',', ':'))
    else:
        config = json.dumps({"tabWidth": preferences.get_pref('indent_size')}, separators=(',', ':'))
    cmd.extend(['-c', config])

    print(cmd)

    return Popen(cmd, stdin=PIPE, stdout=PIPE, shell=(sublime.platform() == 'windows')) \
        .communicate(sql.encode('utf-8'))[0] \
        .decode('utf-8')
