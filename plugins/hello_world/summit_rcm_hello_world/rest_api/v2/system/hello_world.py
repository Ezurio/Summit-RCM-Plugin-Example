"""
Module to support the printing of 'Hello World'
"""

from syslog import LOG_ERR, syslog
import falcon.asgi
from summit_rcm_hello_world.services.hello_world_service import HelloWorldService


class HelloWorldResource(object):
    """
    Resource to handle requests of 'Hello World'
    """

    async def on_get(self, _: falcon.asgi.Request, resp: falcon.asgi.Response) -> None:
        """
        GET handler for the /system/helloWorld endpoint
        """
        try:
            resp.media["Message"] = HelloWorldService().get_hello_world()
            resp.status = falcon.HTTP_200
            resp.content_type = falcon.MEDIA_JSON
        except Exception as exception:
            syslog(
                LOG_ERR,
                f"Unable to get 'Hello World': {str(exception)}",
            )
            resp.status = falcon.HTTP_500
