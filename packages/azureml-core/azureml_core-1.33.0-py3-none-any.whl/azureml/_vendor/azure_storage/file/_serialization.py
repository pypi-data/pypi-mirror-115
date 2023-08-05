# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
from ..common._common_conversion import _str
from ..common._error import (
    _validate_not_none,
    _ERROR_START_END_NEEDED_FOR_MD5,
    _ERROR_RANGE_TOO_LARGE_FOR_MD5,
)


def _get_path(share_name=None, directory_name=None, file_name=None):
    '''
    Creates the path to access a file resource.

    share_name:
        Name of share.
    directory_name:
        The path to the directory.
    file_name:
        Name of file.
    '''
    if share_name and directory_name and file_name:
        return '/{0}/{1}/{2}'.format(
            _str(share_name),
            _str(directory_name),
            _str(file_name))
    elif share_name and directory_name:
        return '/{0}/{1}'.format(
            _str(share_name),
            _str(directory_name))
    elif share_name and file_name:
        return '/{0}/{1}'.format(
            _str(share_name),
            _str(file_name))
    elif share_name:
        return '/{0}'.format(_str(share_name))
    else:
        return '/'


def _validate_and_format_range_headers(request, start_range, end_range, start_range_required=True,
                                       end_range_required=True, check_content_md5=False):
    # If end range is provided, start range must be provided
    if start_range_required or end_range is not None:
        _validate_not_none('start_range', start_range)
    if end_range_required:
        _validate_not_none('end_range', end_range)

    # Format based on whether end_range is present
    request.headers = request.headers or {}
    if end_range is not None:
        request.headers['x-ms-range'] = 'bytes={0}-{1}'.format(start_range, end_range)
    elif start_range is not None:
        request.headers['x-ms-range'] = 'bytes={0}-'.format(start_range)

    # Content MD5 can only be provided for a complete range less than 4MB in size
    if check_content_md5:
        if start_range is None or end_range is None:
            raise ValueError(_ERROR_START_END_NEEDED_FOR_MD5)
        if end_range - start_range > 4 * 1024 * 1024:
            raise ValueError(_ERROR_RANGE_TOO_LARGE_FOR_MD5)

        request.headers['x-ms-range-get-content-md5'] = 'true'
