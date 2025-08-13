#
# SPDX-License-Identifier: LicenseRef-Ezurio-Clause
# Copyright (C) 2024 Ezurio LLC.
#
"""
Module to support the printing of 'Hello World'.
"""


class HelloWorldService:
    """
    Exposes functionality to print 'Hello World'.
    """

    def get_hello_world(self) -> str:
        """
        Return 'Hello World' string.
        """
        return "Hello World"
