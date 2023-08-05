# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from __future__ import print_function
import sys
import json
import base64
import binascii
import six
import logging
import re
import jwt

from six.moves import configparser

from msrestazure.azure_exceptions import CloudError
from msrest.exceptions import HttpOperationError

from azureml.exceptions import AuthenticationException

logger = logging.getLogger(__name__)

CLI_PACKAGE_NAME = 'azure-cli'
COMPONENT_PREFIX = 'azure-cli-'


def handle_exception(ex):
    # For error code, follow guidelines at https://docs.python.org/2/library/sys.html#sys.exit,
    if isinstance(ex, (AuthenticationException, CloudError)):
        logger.error(ex.args[0])
        return ex.args[1] if len(ex.args) >= 2 else 1
    elif isinstance(ex, KeyboardInterrupt):
        return 1
    elif isinstance(ex, HttpOperationError):
        try:
            response_dict = json.loads(ex.response.text)
            error = response_dict['error']

            # ARM should use ODATA v4. So should try this first.
            # http://docs.oasis-open.org/odata/odata-json-format/v4.0/os/odata-json-format-v4.0-os.html#_Toc372793091
            if isinstance(error, dict):
                code = "{} - ".format(error.get('code', 'Unknown Code'))
                message = error.get('message', ex)
                logger.error("%s%s", code, message)
            else:
                logger.error(error)

        except (ValueError, KeyError):
            logger.error(ex)
        return 1

    logger.exception(ex)
    return 1


def to_snake_case(s):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', s)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


# pylint: disable=inconsistent-return-statements
def empty_on_404(ex):
    if isinstance(ex, CloudError) and ex.status_code == 404:
        return None
    raise ex


def truncate_text(str_to_shorten, width=70, placeholder=' [...]'):
    if width <= 0:
        raise ValueError('width must be greater than 0.')
    s_len = width - len(placeholder)
    return str_to_shorten[:s_len] + (str_to_shorten[s_len:] and placeholder)


def get_token_for_adal_auth(token):
    decoded_json = jwt.decode(token, options={'verify_signature': False, 'verify_aud': False})
    token_expiry = {
        'expires_on': int(decoded_json['exp'])
    }
    return token_expiry


def get_json_object(json_string):
    """ Loads a JSON string as an object and converts all keys to snake case """

    def _convert_to_snake_case(item):
        if isinstance(item, dict):
            new_item = {}
            for key, val in item.items():
                new_item[to_snake_case(key)] = _convert_to_snake_case(val)
            return new_item
        if isinstance(item, list):
            return [_convert_to_snake_case(x) for x in item]
        return item

    return _convert_to_snake_case(shell_safe_json_parse(json_string))


def get_file_json(file_path, throw_on_empty=True, preserve_order=False):
    content = read_file_content(file_path)
    if not content and not throw_on_empty:
        return None
    return shell_safe_json_parse(content, preserve_order)


def read_file_content(file_path, allow_binary=False):
    from codecs import open as codecs_open
    # Note, always put 'utf-8-sig' first, so that BOM in WinOS won't cause trouble.
    for encoding in ['utf-8-sig', 'utf-8', 'utf-16', 'utf-16le', 'utf-16be']:
        try:
            with codecs_open(file_path, encoding=encoding) as f:
                logger.debug("attempting to read file %s as %s", file_path, encoding)
                return f.read()
        except (UnicodeError, UnicodeDecodeError):
            pass

    if allow_binary:
        try:
            with open(file_path, 'rb') as input_file:
                logger.debug("attempting to read file %s as binary", file_path)
                return base64.b64encode(input_file.read()).decode("utf-8")
        except Exception:  # pylint: disable=broad-except
            pass
    raise AuthenticationException('Failed to decode file {} - unknown decoding'.format(file_path))


def shell_safe_json_parse(json_or_dict_string, preserve_order=False):
    """ Allows the passing of JSON or Python dictionary strings. This is needed because certain
    JSON strings in CMD shell are not received in main's argv. This allows the user to specify
    the alternative notation, which does not have this problem (but is technically not JSON). """
    try:
        if not preserve_order:
            return json.loads(json_or_dict_string)
        from collections import OrderedDict
        return json.loads(json_or_dict_string, object_pairs_hook=OrderedDict)
    except ValueError as json_ex:
        try:
            import ast
            return ast.literal_eval(json_or_dict_string)
        except SyntaxError:
            raise AuthenticationException(json_ex)


def b64encode(s):
    """
    Encodes a string to base64 on 2.x and 3.x
    :param str s: latin_1 encoded string
    :return: base64 encoded string
    :rtype: str
    """
    encoded = base64.b64encode(six.b(s))
    return encoded if encoded is str else encoded.decode('latin-1')


def b64_to_hex(s):
    """
    Decodes a string to base64 on 2.x and 3.x
    :param str s: base64 encoded string
    :return: uppercase hex string
    :rtype: str
    """
    decoded = base64.b64decode(s)
    hex_data = binascii.hexlify(decoded).upper()
    if isinstance(hex_data, bytes):
        return str(hex_data.decode("utf-8"))
    return hex_data


def random_string(length=16, force_lower=False, digits_only=False):
    from string import ascii_letters, digits, ascii_lowercase
    from random import choice
    choice_set = digits
    if not digits_only:
        choice_set += ascii_lowercase if force_lower else ascii_letters
    return ''.join([choice(choice_set) for _ in range(length)])


def hash_string(value, length=16, force_lower=False):
    """ Generate a deterministic hashed string."""
    import hashlib
    m = hashlib.sha256()
    try:
        m.update(value)
    except TypeError:
        m.update(value.encode())
    digest = m.hexdigest()
    digest = digest.lower() if force_lower else digest
    while len(digest) < length:
        digest = digest + digest
    return digest[:length]


def in_cloud_console():
    import os
    return os.environ.get('ACC_CLOUD', None)


def get_arg_list(op):
    import inspect

    try:
        # only supported in python3 - falling back to argspec if not available
        sig = inspect.signature(op)
        return sig.parameters
    except AttributeError:
        sig = inspect.getargspec(op)  # pylint: disable=deprecated-method
        return sig.args


DISABLE_VERIFY_VARIABLE_NAME = "AZURE_CLI_DISABLE_CONNECTION_VERIFICATION"


def should_disable_connection_verify():
    import os
    return bool(os.environ.get(DISABLE_VERIFY_VARIABLE_NAME))


def poller_classes():
    from msrestazure.azure_operation import AzureOperationPoller
    from msrest.polling.poller import LROPoller
    return (AzureOperationPoller, LROPoller)


def scopes_to_resource(scopes):
    """Convert MSAL scopes to ADAL resource by stripping the /.default suffix and return a str.
    For example:
       ['https://management.core.windows.net//.default'] -> 'https://management.core.windows.net/'
       ['https://managedhsm.azure.com/.default'] -> 'https://managedhsm.azure.com'
    :param scopes: The MSAL scopes. It can be a list or tuple of string
    :return: The ADAL resource
    :rtype: str
    """
    scope = scopes[0]
    if scope.endswith("/.default"):
        scope = scope[:-len("/.default")]

    return scope


def augment_no_wait_handler_args(no_wait_enabled, handler, handler_args):
    """ Populates handler_args with the appropriate args for no wait """
    h_args = get_arg_list(handler)
    if 'no_wait' in h_args:
        handler_args['no_wait'] = no_wait_enabled
    if 'raw' in h_args and no_wait_enabled:
        # support autorest 2
        handler_args['raw'] = True
    if 'polling' in h_args and no_wait_enabled:
        # support autorest 3
        handler_args['polling'] = False


def sdk_no_wait(no_wait, func, *args, **kwargs):
    if no_wait:
        kwargs.update({'raw': True, 'polling': False})
    return func(*args, **kwargs)


def open_page_in_browser(url):
    import subprocess
    import webbrowser
    platform_name, release = _get_platform_info()

    if _is_wsl(platform_name, release):   # windows 10 linux subsystem
        try:
            return subprocess.call(['cmd.exe', '/c', "start {}".format(url.replace('&', '^&'))])
        except FileNotFoundError:  # WSL might be too old
            pass
    elif platform_name == 'darwin':
        # handle 2 things:
        # a. On OSX sierra, 'python -m webbrowser -t <url>' emits out "execution error: <url> doesn't
        #    understand the "open location" message"
        # b. Python 2.x can't sniff out the default browser
        return subprocess.Popen(['open', url])
    try:
        return webbrowser.open(url, new=2)  # 2 means: open in a new tab, if possible
    except TypeError:  # See https://bugs.python.org/msg322439
        return webbrowser.open(url, new=2)


def _get_platform_info():
    import platform
    uname = platform.uname()
    # python 2, `platform.uname()` returns: tuple(system, node, release, version, machine, processor)
    platform_name = getattr(uname, 'system', None) or uname[0]
    release = getattr(uname, 'release', None) or uname[2]
    return platform_name.lower(), release.lower()


def _is_wsl(platform_name, release):
    platform_name, release = _get_platform_info()
    return platform_name == 'linux' and release.split('-')[-1] == 'microsoft'


def can_launch_browser():
    import os
    import webbrowser
    platform_name, release = _get_platform_info()
    if _is_wsl(platform_name, release) or platform_name != 'linux':
        return True
    # per https://unix.stackexchange.com/questions/46305/is-there-a-way-to-retrieve-the-name-of-the-desktop-environment
    # and https://unix.stackexchange.com/questions/193827/what-is-display-0
    # we can check a few env vars
    gui_env_vars = ['DESKTOP_SESSION', 'XDG_CURRENT_DESKTOP', 'DISPLAY']
    result = True
    if platform_name == 'linux':
        if any(os.getenv(v) for v in gui_env_vars):
            try:
                default_browser = webbrowser.get()
                if getattr(default_browser, 'name', None) == 'www-browser':  # text browser won't work
                    result = False
            except webbrowser.Error:
                result = False
        else:
            result = False

    return result


def get_command_type_kwarg(custom_command=False):
    return 'custom_command_type' if custom_command else 'command_type'


def reload_module(module):
    # reloading the imported module to update
    try:
        from importlib import reload
    except ImportError:
        pass  # for python 2
    reload(sys.modules[module])


def get_config_parser():
    return configparser.ConfigParser() if sys.version_info.major == 3 else configparser.SafeConfigParser()
