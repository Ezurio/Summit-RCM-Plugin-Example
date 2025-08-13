#!/usr/bin/python
#
# SPDX-License-Identifier: LicenseRef-Ezurio-Clause
# Copyright (C) 2025 Ezurio LLC.
#
"""
Generate the OpenAPI spec for the Summit RCM REST API for the Hello World plugin
"""


def generate_docs():
    """
    Generate the OpenAPI spec for the Summit RCM REST API for the Hello World plugin. This function
    is called during the build process to generate the OpenAPI spec for the Hello World plugin.
    """
    from summit_rcm.rest_api.utils.spectree.generate_api_spec import generate_api_spec

    routes = {}

    try:
        from summit_rcm_hello_world.rest_api.legacy.hello_world import (
            HelloWorldResourceLegacy,
        )

        routes["/helloWorld"] = HelloWorldResourceLegacy
    except ImportError:
        pass

    try:
        from summit_rcm_hello_world.rest_api.v2.system.hello_world import (
            HelloWorldResource,
        )

        routes["/api/v2/system/helloWorld"] = HelloWorldResource
    except ImportError:
        pass

    generate_api_spec(routes)


if __name__ == "__main__":
    generate_docs()
