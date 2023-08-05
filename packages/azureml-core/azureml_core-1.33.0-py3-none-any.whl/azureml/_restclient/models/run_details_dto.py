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


class RunDetailsDto(Model):
    """RunDetailsDto.

    :param run_id:
    :type run_id: str
    :param target:
    :type target: str
    :param status:
    :type status: str
    :param start_time_utc:
    :type start_time_utc: datetime
    :param end_time_utc:
    :type end_time_utc: datetime
    :param error:
    :type error: ~_restclient.models.ErrorResponse
    :param warnings:
    :type warnings: list[~_restclient.models.RunDetailsWarningDto]
    :param properties:
    :type properties: dict[str, str]
    :param input_datasets: A list of dataset used as input to the run.
    :type input_datasets: list[~_restclient.models.DatasetLineage]
    :param output_datasets:
    :type output_datasets: list[~_restclient.models.OutputDatasetLineage]
    :param run_definition:
    :type run_definition: object
    :param log_files:
    :type log_files: dict[str, str]
    """

    _attribute_map = {
        'run_id': {'key': 'runId', 'type': 'str'},
        'target': {'key': 'target', 'type': 'str'},
        'status': {'key': 'status', 'type': 'str'},
        'start_time_utc': {'key': 'startTimeUtc', 'type': 'iso-8601'},
        'end_time_utc': {'key': 'endTimeUtc', 'type': 'iso-8601'},
        'error': {'key': 'error', 'type': 'ErrorResponse'},
        'warnings': {'key': 'warnings', 'type': '[RunDetailsWarningDto]'},
        'properties': {'key': 'properties', 'type': '{str}'},
        'input_datasets': {'key': 'inputDatasets', 'type': '[DatasetLineage]'},
        'output_datasets': {'key': 'outputDatasets', 'type': '[OutputDatasetLineage]'},
        'run_definition': {'key': 'runDefinition', 'type': 'object'},
        'log_files': {'key': 'logFiles', 'type': '{str}'},
    }

    def __init__(self, run_id=None, target=None, status=None, start_time_utc=None, end_time_utc=None, error=None, warnings=None, properties=None, input_datasets=None, output_datasets=None, run_definition=None, log_files=None):
        super(RunDetailsDto, self).__init__()
        self.run_id = run_id
        self.target = target
        self.status = status
        self.start_time_utc = start_time_utc
        self.end_time_utc = end_time_utc
        self.error = error
        self.warnings = warnings
        self.properties = properties
        self.input_datasets = input_datasets
        self.output_datasets = output_datasets
        self.run_definition = run_definition
        self.log_files = log_files
