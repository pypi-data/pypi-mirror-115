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


class LinkedServiceList(Model):
    """List response of linked service.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :ivar value: Array of linked service.
    :vartype value: list[~_restclient.models.LinkedServiceResponse]
    """

    _validation = {
        'value': {'readonly': True},
    }

    _attribute_map = {
        'value': {'key': 'value', 'type': '[LinkedServiceResponse]'},
    }

    def __init__(self):
        super(LinkedServiceList, self).__init__()
        self.value = None
