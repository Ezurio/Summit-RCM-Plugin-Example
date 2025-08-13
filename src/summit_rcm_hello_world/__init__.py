#
# SPDX-License-Identifier: LicenseRef-Ezurio-Clause
# Copyright (C) 2024 Ezurio LLC.
#
"""Init File to setup the Hello World Plugin"""
from syslog import syslog, LOG_ERR
from typing import Optional


def get_at_commands():
    """Function to import and return Hello World AT Commands"""
    at_commands = []
    try:
        from summit_rcm_hello_world.at_interface.commands.hello_world_command import (
            HelloWorldCommand,
        )

        at_commands.extend([HelloWorldCommand])
    except ImportError:
        pass
    except Exception as exception:
        syslog(LOG_ERR, f"Error Importing hello world AT Commands: {str(exception)}")
    return at_commands


async def get_legacy_supported_routes():
    """Optional Function to return supported legacy routes"""
    routes = []
    routes.append("/helloWorld")
    return routes


async def get_legacy_routes():
    """Function to import and return Hello World API Routes"""
    routes = {}
    try:
        from summit_rcm_hello_world.services.hello_world_service import (
            HelloWorldService,
        )
        from summit_rcm_hello_world.rest_api.legacy.hello_world import (
            HelloWorldResourceLegacy,
        )

        routes["/helloWorld"] = HelloWorldResourceLegacy()
    except ImportError:
        pass
    except Exception as exception:
        syslog(LOG_ERR, f"Error Importing hello world legacy routes: {str(exception)}")
    return routes


async def get_v2_supported_routes():
    """Optional Function to return supported v2 routes"""
    routes = []
    routes.append("/api/v2/system/helloWorld")
    return routes


async def get_v2_routes():
    """Function to import and return Hello World API Routes"""
    routes = {}
    try:
        from summit_rcm_hello_world.services.hello_world_service import (
            HelloWorldService,
        )
        from summit_rcm_hello_world.rest_api.v2.system.hello_world import (
            HelloWorldResource,
        )

        routes["/api/v2/system/helloWorld"] = HelloWorldResource()
    except ImportError:
        pass
    except Exception as exception:
        syslog(LOG_ERR, f"Error Importing hello world v2 routes: {str(exception)}")
    return routes


async def get_middleware() -> Optional[list]:
    """Handler called when adding Falcon middleware"""
    return None


async def server_config_preload_hook(_) -> None:
    """Hook function called before the Uvicorn ASGI server config is loaded"""


async def server_config_postload_hook(_) -> None:
    """Hook function called after the Uvicorn ASGI server config is loaded"""
