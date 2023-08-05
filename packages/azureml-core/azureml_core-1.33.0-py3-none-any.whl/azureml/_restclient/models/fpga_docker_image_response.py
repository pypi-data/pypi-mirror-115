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

from .image_response_base import ImageResponseBase


class FPGADockerImageResponse(ImageResponseBase):
    """The FPGA Docker Image response.

    :param id: The image Id.
    :type id: str
    :param name: The image name.
    :type name: str
    :param version: The image version.
    :type version: long
    :param digest: The sha256-based digest of the image
    :type digest: str
    :param description: The image description.
    :type description: str
    :param kv_tags: The image tag dictionary. Tags are mutable.
    :type kv_tags: dict[str, str]
    :param properties: The image properties dictionary. Properties are
     immutable.
    :type properties: dict[str, str]
    :param created_time: The time the image was created.
    :type created_time: datetime
    :param modified_time: The time the image was last modified.
    :type modified_time: datetime
    :param auto_delete: Whether the image will be automatically deleted with
     the last service using it.
    :type auto_delete: bool
    :param image_type: The type of the image. Possible values include:
     'Docker'
    :type image_type: str or ~_restclient.models.ImageType
    :param creation_state: The state of the operation. Possible values
     include: 'NotStarted', 'Running', 'Cancelled', 'Succeeded', 'Failed',
     'TimedOut'
    :type creation_state: str or ~_restclient.models.AsyncOperationState
    :param error: The error response.
    :type error: ~_restclient.models.ImageResponseBaseError
    :param model_ids: The list of model Ids.
    :type model_ids: list[str]
    :param model_details: The list of models.
    :type model_details: list[~_restclient.models.Model]
    :param image_location: The Image location string.
    :type image_location: str
    :param image_build_log_uri: The Uri to the image build logs.
    :type image_build_log_uri: str
    :param operation_id: The ID of the asynchronous operation for this image.
    :type operation_id: str
    :param image_flavor: Constant filled by server.
    :type image_flavor: str
    """

    _validation = {
        'image_flavor': {'required': True},
    }

    def __init__(self, id=None, name=None, version=None, digest=None, description=None, kv_tags=None, properties=None, created_time=None, modified_time=None, auto_delete=None, image_type=None, creation_state=None, error=None, model_ids=None, model_details=None, image_location=None, image_build_log_uri=None, operation_id=None):
        super(FPGADockerImageResponse, self).__init__(id=id, name=name, version=version, digest=digest, description=description, kv_tags=kv_tags, properties=properties, created_time=created_time, modified_time=modified_time, auto_delete=auto_delete, image_type=image_type, creation_state=creation_state, error=error, model_ids=model_ids, model_details=model_details, image_location=image_location, image_build_log_uri=image_build_log_uri, operation_id=operation_id)
        self.image_flavor = 'ACCELCONTAINER'
