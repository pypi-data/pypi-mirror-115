# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator 2.3.33.0
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class UploadOptions(Model):
    """Upload specific options.

    :param overwrite: Whether to overwrite files that already exists at the
     destination path.
    :type overwrite: bool
    :param source_globs: Glob patterns to use to filter which files will be
     uploaded.
    :type source_globs: ~_restclient.models.GlobsOptions
    """

    _attribute_map = {
        'overwrite': {'key': 'overwrite', 'type': 'bool'},
        'source_globs': {'key': 'sourceGlobs', 'type': 'GlobsOptions'},
    }

    def __init__(self, overwrite=None, source_globs=None):
        super(UploadOptions, self).__init__()
        self.overwrite = overwrite
        self.source_globs = source_globs
