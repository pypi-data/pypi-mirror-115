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


class HistoryConfiguration(Model):
    """A class to manage History Configuration. History configuration let users to
    disable and enable experiment history logging features.

    :param output_collection: True means history tracking will be enabled --
     this allows logs, outputs to be collected.
     False means history tracking will be disabled. Default value: True .
    :type output_collection: bool
    :param directories_to_watch: The list of directories to monitor and upload
     files from.
    :type directories_to_watch: list[str]
    :param enable_mlflow_tracking: True means MLflow tracking will be enabled
     False means MLflow tracking will be disbaled. Default value: True .
    :type enable_mlflow_tracking: bool
    """

    _attribute_map = {
        'output_collection': {'key': 'outputCollection', 'type': 'bool'},
        'directories_to_watch': {'key': 'directoriesToWatch', 'type': '[str]'},
        'enable_mlflow_tracking': {'key': 'enableMLflowTracking', 'type': 'bool'},
    }

    def __init__(self, output_collection=True, directories_to_watch=None, enable_mlflow_tracking=True):
        super(HistoryConfiguration, self).__init__()
        self.output_collection = output_collection
        self.directories_to_watch = directories_to_watch
        self.enable_mlflow_tracking = enable_mlflow_tracking
