#
# SPDX-License-Identifier: LicenseRef-Ezurio-Clause
# Copyright (C) 2024 Ezurio LLC.
#
"""
Module to support the printing of 'Hello World'
"""

import falcon.asgi
from summit_rcm.settings import ServerConfig
from summit_rcm.rest_api.services.spectree_service import (
    DocsNotEnabledException,
    SpectreeService,
)
from summit_rcm import definition
from summit_rcm_hello_world.services.hello_world_service import HelloWorldService

try:
    if not ServerConfig().rest_api_docs_enabled:
        raise DocsNotEnabledException()

    from spectree import Response
    from summit_rcm.rest_api.utils.spectree.models import (
        UnauthorizedErrorResponseModel,
    )
    from summit_rcm_hello_world.rest_api.utils.spectree.models import (
        HelloWorldResponseModelLegacy,
    )
    from summit_rcm.rest_api.utils.spectree.tags import system_tag
except (ImportError, DocsNotEnabledException):
    from summit_rcm.rest_api.services.spectree_service import DummyResponse as Response

    UnauthorizedErrorResponseModel = None
    HelloWorldResponseModelLegacy = None
    system_tag = None


spec = SpectreeService()


class HelloWorldResourceLegacy:
    """
    Resource to expose 'Hello World' functionality
    """

    @spec.validate(
        resp=Response(
            HTTP_200=HelloWorldResponseModelLegacy,
            HTTP_401=UnauthorizedErrorResponseModel,
        ),
        security=SpectreeService().security,
        tags=[system_tag],
        deprecated=True,
    )
    async def on_get(self, req, resp):
        """
        Retrieve 'Hello World' message (legacy)
        """
        resp.status = falcon.HTTP_200
        resp.content_type = falcon.MEDIA_JSON
        result = {
            "SDCERR": definition.SUMMIT_RCM_ERRORS["SDCERR_FAIL"],
            "InfoMsg": "Could not get 'Hello World'",
            "Message": "",
        }

        try:
            result["Message"] = HelloWorldService().get_hello_world()
        except Exception:
            resp.media = result
            return
        result["InfoMsg"] = ""
        result["SDCERR"] = definition.SUMMIT_RCM_ERRORS["SDCERR_SUCCESS"]
        resp.media = result
