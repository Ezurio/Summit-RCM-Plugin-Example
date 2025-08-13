#
# SPDX-License-Identifier: LicenseRef-Ezurio-Clause
# Copyright (C) 2024 Ezurio LLC.
#
"""Module to hold SpecTree Models"""

try:
    from pydantic.v1 import BaseModel
except ImportError:
    from pydantic import BaseModel
from summit_rcm.rest_api.utils.spectree.models import DefaultResponseModelLegacy


class HelloWorldResponseModel(BaseModel):
    """Model for the response to a request for the hello world message"""

    Message: str


class HelloWorldResponseModelLegacy(DefaultResponseModelLegacy):
    """Model for the response to a request for the hello world message (legacy)"""

    Message: str
