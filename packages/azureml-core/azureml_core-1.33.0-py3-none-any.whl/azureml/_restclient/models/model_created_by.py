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

from .user import User


class ModelCreatedBy(User):
    """The User who created this entity.

    :param user_object_id: A user or service principal's object ID.
     This is EUPI and may only be logged to warm path telemetry.
    :type user_object_id: str
    :param user_pu_id: A user or service principal's PuID.
     This is PII and should never be logged.
    :type user_pu_id: str
    :param user_idp: A user identity provider. Eg live.com
     This is PII and should never be logged.
    :type user_idp: str
    :param user_alt_sec_id: A user alternate sec id. This represents the user
     in a different identity provider system Eg.1:live.com:puid
     This is PII and should never be logged.
    :type user_alt_sec_id: str
    :param user_iss: The issuer which issed the token for this user.
     This is PII and should never be logged.
    :type user_iss: str
    :param user_tenant_id: A user or service principal's tenant ID.
    :type user_tenant_id: str
    :param user_name: A user's full name or a service principal's app ID.
     This is PII and should never be logged.
    :type user_name: str
    """

    def __init__(self, user_object_id=None, user_pu_id=None, user_idp=None, user_alt_sec_id=None, user_iss=None, user_tenant_id=None, user_name=None):
        super(ModelCreatedBy, self).__init__(user_object_id=user_object_id, user_pu_id=user_pu_id, user_idp=user_idp, user_alt_sec_id=user_alt_sec_id, user_iss=user_iss, user_tenant_id=user_tenant_id, user_name=user_name)
