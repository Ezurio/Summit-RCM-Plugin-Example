"""
Module to support the printing of 'Hello World'
"""

import falcon
from summit_rcm import definition
from summit_rcm_hello_world.services.hello_world_service import HelloWorldService


class HelloWorldResourceLegacy:
    """
    Resource to expose 'Hello World' functionality
    """

    async def on_get(self, req, resp):
        """
        GET handler for the /helloWorld endpoint
        """
        resp.status = falcon.HTTP_200
        resp.content_type = falcon.MEDIA_JSON
        result = {
            "SDCERR": definition.SUMMIT_RCM_ERRORS["SDCERR_FAIL"],
            "InfoMsg": "Could not get 'Hello World'",
        }

        try:
            result["Message"] = HelloWorldService().get_hello_world()
        except Exception:
            resp.media = result
            return
        result["InfoMsg"] = ""
        result["SDCERR"] = definition.SUMMIT_RCM_ERRORS["SDCERR_SUCCESS"]
        resp.media = result
