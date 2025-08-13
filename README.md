# Summit-RCM-Plugin-Example
Summit RCM Plugin Example Repo

This repo is meant as a working example of a Summit RCM plugin integrated into a custom Buildroot "external" directory.

## Getting Started
1. Clone this repo under the `package` sub-directory of your custom Buildroot "external" directory.
```
cd my_br2_external/package
git clone git@github.com:Ezurio/Summit-RCM-Plugin-Example.git summit-rcm-hello-world-plugin
```

Your Buildroot "external" directory should now look something like this:

```bash
.
├── Config.in  # Config.in file for any packages, which will be modified later
├── package
│   └── summit-rcm-hello-world-plugin  # summit-rcm-NAME-OF-PLUGIN-plugin
│       ├── Config.in  # Config.in for the plugin
│       ├── pyproject.toml  # Python project file for the plugin
│       ├── src
│       │   ├── generate_docs.py
│       │   ├── setup.py
│       │   └── summit_rcm_hello_world  # summit_rcm_NAME_OF_PLUGIN
│       │       ├── __init__.py
│       │       ├── at_interface  # If the plugin includes an AT Command
│       │       │   └── commands
│       │       │       ├── hello_world_command.py
│       │       │       └── __init__.py
│       │       ├── rest_api
│       │       │   ├── legacy  # If the plugin includes a legacy REST endpoint
│       │       │   │   ├── hello_world.py
│       │       │   │   └── __init__.py
│       │       │   ├── utils
│       │       │   │   └── spectree
│       │       │   │       ├── __init__.py
│       │       │   │       └── models.py  # If REST API live doc model definitions are included
│       │       │   └── v2  # If the plugin includes a v2 REST endpoint
│       │       │       └── system
│       │       │           ├── hello_world.py
│       │       │           └── __init__.py
│       │       └── services
│       │           ├── hello_world_service.py
│       │           └── __init__.py
│       └── summit-rcm-hello-world-plugin.mk  # Makefile for the plugin
└── ...
```
 
2. Update the top-level `Config.in` file for your Buildroot "external" directory as seen above to include the plugin `Config.in`. For example, add something like this:
```bash
source "$BR2_EXTERNAL_NAME_OF_EXTERNAL_PATH/package/summit-rcm-hello-world-plugin/Config.in"
```

3. Create the content of the Config.in file for the plugin, which will include any configuration options/dependencies:
```bash
config BR2_PACKAGE_SUMMIT_RCM_HELLO_WORLD_PLUGIN  # Name of Plugin
	bool "Hello World plugin for Summit RCM"
	depends on BR2_PACKAGE_SUMMIT_RCM  # Dependent on Summit RCM
	default y
	help
		Add Hello World configuration support to Summit RCM.
```

4. Create the content of the Makefile for the plugin:
```bash
#####################################################################
# Summit Remote Control Manager (RCM) Hello World Plugin
#####################################################################

SUMMIT_RCM_HELLO_WORLD_PLUGIN_VERSION = local  # All Makefile parameters will be in the form of SUMMIT_RCM_NAME_OF_PLUGIN_PLUGIN_PARAMETER
SUMMIT_RCM_HELLO_WORLD_PLUGIN_SITE = $(SUMMIT_RCM_HELLO_WORLD_PLUGIN_PKGDIR)/src # Location of plugin code
SUMMIT_RCM_HELLO_WORLD_PLUGIN_SITE_METHOD = local
SUMMIT_RCM_HELLO_WORLD_PLUGIN_LICENSE = Ezurio
SUMMIT_RCM_HELLO_WORLD_PLUGIN_LICENSE_FILES = LICENSE.ezurio
SUMMIT_RCM_HELLO_WORLD_PLUGIN_SETUP_TYPE = pep517
SUMMIT_RCM_HELLO_WORLD_PLUGIN_DEPENDENCIES = python3 summit-rcm

ifeq ($(BR2_PACKAGE_HOST_PYTHON_CYTHON),y)
SUMMIT_RCM_HELLO_WORLD_PLUGIN_DEPENDENCIES += host-python-cython
endif

SUMMIT_RCM_HELLO_WORLD_PLUGIN_EXTRA_PACKAGES = \  # Add all extra packages that must be installed during build, will always include the root directory and services
	summit_rcm_hello_world \
	summit_rcm_hello_world/services

ifeq ($(BR2_PACKAGE_SUMMIT_RCM_AT_INTERFACE),y)  # Include the AT commands if AT Interface is enabled
	SUMMIT_RCM_HELLO_WORLD_PLUGIN_EXTRA_PACKAGES += summit_rcm_hello_world/at_interface/commands
endif
ifeq ($(BR2_PACKAGE_SUMMIT_RCM_REST_API_V2_ROUTES),y)  # Include the V2 routes if V2 is enabled
    SUMMIT_RCM_HELLO_WORLD_PLUGIN_EXTRA_PACKAGES += summit_rcm_hello_world/rest_api/v2/system
endif
ifeq ($(BR2_PACKAGE_SUMMIT_RCM_REST_API_LEGACY_ROUTES),y)  # Include the legacy routes if legacy is enabled
    SUMMIT_RCM_HELLO_WORLD_PLUGIN_EXTRA_PACKAGES += summit_rcm_hello_world/rest_api/legacy
endif

ifeq ($(BR2_PACKAGE_SUMMIT_RCM_REST_API_DOCS),y)  # Generate the REST API live docs for the plugin, if enabled
	SUMMIT_RCM_HELLO_WORLD_PLUGIN_EXTRA_PACKAGES += summit_rcm_hello_world/rest_api/utils/spectree
	SUMMIT_RCM_HELLO_WORLD_PLUGIN_DEPENDENCIES += host-summit-rcm-hello-world-plugin
	HOST_SUMMIT_RCM_HELLO_WORLD_PLUGIN_DEPENDENCIES += \
		host-summit-rcm \
		host-python3 \
		host-python-falcon \
		host-python-spectree \
		host-python-pydantic \
		host-python-typing-extensions
	HOST_SUMMIT_RCM_HELLO_WORLD_PLUGIN_ENV = \
		DOCS_GENERATION='True' \
		OPENAPI_JSON_PATH='$(TARGET_DIR)/summit-rcm-openapi-hello-world-plugin.json' \
		SUMMIT_RCM_HELLO_WORLD_PLUGIN_EXTRA_PACKAGES='$(SUMMIT_RCM_HELLO_WORLD_PLUGIN_EXTRA_PACKAGES)'
	HOST_SUMMIT_RCM_HELLO_WORLD_PLUGIN_BUILD_OPTS = && \
		$(HOST_SUMMIT_RCM_HELLO_WORLD_PLUGIN_ENV) \
		$(HOST_DIR)/bin/python3 generate_docs.py
endif

SUMMIT_RCM_HELLO_WORLD_PLUGIN_ENV = SUMMIT_RCM_HELLO_WORLD_PLUGIN_EXTRA_PACKAGES='$(SUMMIT_RCM_HELLO_WORLD_PLUGIN_EXTRA_PACKAGES)'  # Sets the environment to the extra packages

$(eval $(python-package))  # Run the setup.py file for the plugin
$(eval $(host-python-package)) # Run the setup.py file for generating documentation for the plugin
```

5. Create the contents of the setup.py file for the plugin:
```python
#!/usr/bin/python
#
# SPDX-License-Identifier: LicenseRef-Ezurio-Clause
# Copyright (C) 2024 Ezurio LLC.
#

import glob
import os

from setuptools import setup, Extension

MYDIR = os.path.abspath(os.path.dirname(__file__))

try:
    from Cython.Distutils import build_ext

    CYTHON = True
except ImportError:
    CYTHON = False


class BuildFailed(Exception):
    pass


packages = []
environment_variable_value = os.environ.get(
    "SUMMIT_RCM_HELLO_WORLD_PLUGIN_EXTRA_PACKAGES", ""
)  # Get the plugin extra packages
if len(environment_variable_value) > 0:
    extra_packages = [s.strip() for s in environment_variable_value.split()]
else:
    extra_packages = []
for package in extra_packages:
    packages.append(package)


def get_cython_options():
    from distutils.errors import (
        CCompilerError,
        DistutilsExecError,
        DistutilsPlatformError,
    )

    ext_errors = (CCompilerError, DistutilsExecError, DistutilsPlatformError)

    class ve_build_ext(build_ext):
        # This class allows Cython building to fail.

        def run(self):
            try:
                super().run()
            except DistutilsPlatformError:
                raise BuildFailed()

        def build_extension(self, ext):
            try:
                super().build_extension(ext)
            except ext_errors as e:
                raise BuildFailed() from e
            except ValueError as e:
                # this can happen on Windows 64 bit, see Python issue 7511
                if "'path'" in str(e):
                    raise BuildFailed() from e
                raise

    def list_modules(dirname, pattern):
        filenames = glob.glob(os.path.join(dirname, pattern))

        module_names = []
        for name in filenames:
            module, ext = os.path.splitext(os.path.basename(name))
            if module != "__init__":
                module_names.append((module, ext))

        return module_names

    package_names = [p.replace("/", ".") for p in packages]

    modules_to_exclude = ["summit_rcm_hello_world.rest_api.utils.spectree.models"]

    cython_package_names = frozenset([])

    ext_modules = [
        Extension(
            package + "." + module,
            [os.path.join(*(package.split(".") + [module + ext]))],
        )
        for package in package_names
        for module, ext in list_modules(
            os.path.join(MYDIR, *package.split(".")),
            ("*.pyx" if package in cython_package_names else "*.py"),
        )
        if (package + "." + module) not in modules_to_exclude
    ]

    for ext_mod in ext_modules:
        ext_mod.cython_directives = {
            "language_level": "3",
            "always_allow_keywords": True,
        }

    cmdclass = {"build_ext": ve_build_ext}
    return cmdclass, ext_modules


def run_setup(CYTHON):
    if CYTHON:
        cmdclass, ext_modules = get_cython_options()
    else:
        cmdclass, ext_modules = {}, []
    setup(
        name="summit-rcm-hello-world-plugin",  # summit-rcm-NAME-OF-PLUGIN-plugin
        cmdclass=cmdclass,
        version="1.0",
        packages=packages,
        ext_modules=ext_modules,
    )


def status_msgs(*msgs):
    print("*" * 75, *msgs, "*" * 75, sep="\n")


if not CYTHON:
    run_setup(False)
elif os.environ.get("SUMMIT_RCM_DISABLE_CYTHON"):
    run_setup(False)
    status_msgs(
        "SUMMIT_RCM_DISABLE_CYTHON is set, skipping cython compilation.",
        "Pure-Python build succeeded.",
    )
else:
    try:
        run_setup(True)
    except BuildFailed as exc:
        status_msgs(
            exc.__cause__,
            "Cython compilation could not be completed, speedups are not enabled.",
            "Failure information, if any, is above.",
            "Retrying the build without the C extension now.",
        )

        run_setup(False)

        status_msgs(
            "Cython compilation could not be completed, speedups are not enabled.",
            "Pure-Python build succeeded.",
        )

``` 

6. Create the contents for the ``__init__.py`` of the plugin:
```python
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

```

7. Create the contents of the AT Commands or API files needed

Ex: AT Command
```python
#
# SPDX-License-Identifier: LicenseRef-Ezurio-Clause
# Copyright (C) 2024 Ezurio LLC.
#
"""
File that consists of the HelloWorld Command Functionality
"""
from typing import List, Tuple
from syslog import LOG_ERR, syslog
from summit_rcm.at_interface.commands.command import Command  # Must import Command base class
from summit_rcm_hello_world.services.hello_world_service import HelloWorldService


class HelloWorldCommand(Command):  # Must take in the Command base class and requires an execute, parse params, usage, signature, and name
    """
    AT Command to print 'Hello World'
    """

    NAME: str = "Print 'Hello World'"
    SIGNATURE: str = "at+hello"  # The AT input to call this command
    VALID_NUM_PARAMS: List[int] = [1]  # Number of parameters the command takes

    @staticmethod
    async def execute(params: str) -> Tuple[bool, str]:
        (valid, params_dict) = HelloWorldCommand.parse_params(params)  # Must parse the parameters to verify "valid" input
        if not valid:
            syslog(LOG_ERR, "Invalid Parameters")
            return (True, "ERROR")
        try:
            hello_world_str = HelloWorldService().get_hello_world()
            return (True, f"+HELLO: {hello_world_str}\r\nOK")  # Return must be a tuple of (bool, str)
        except Exception as exception:
            syslog(LOG_ERR, f"Error printing 'Hello World': {str(exception)}")
            return (True, "ERROR")

    @staticmethod
    def parse_params(params: str) -> Tuple[bool, dict]:
        valid = True
        params_dict = {}
        params_list = params.split(",")
        valid &= len(params_list) in HelloWorldCommand.VALID_NUM_PARAMS
        for param in params_list:
            valid &= param == ""
        return (valid, params_dict)

    @staticmethod
    def usage() -> str:
        return "AT+HELLO"

    @staticmethod
    def signature() -> str:
        return HelloWorldCommand.SIGNATURE

    @staticmethod
    def name() -> str:
        return HelloWorldCommand.NAME

```

Ex: Legacy Endpoint
```python
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
        resp.status = falcon.HTTP_200  # Must specify the status, content_type, and media of the response
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

```

Ex: V2 Endpoint
```python
#
# SPDX-License-Identifier: LicenseRef-Ezurio-Clause
# Copyright (C) 2024 Ezurio LLC.
#
"""
Module to support the printing of 'Hello World'
"""

from syslog import LOG_ERR, syslog
import falcon.asgi
from summit_rcm.settings import ServerConfig
from summit_rcm.rest_api.services.spectree_service import (
    DocsNotEnabledException,
    SpectreeService,
)
from summit_rcm_hello_world.services.hello_world_service import HelloWorldService

try:
    if not ServerConfig().rest_api_docs_enabled:
        raise DocsNotEnabledException()

    from spectree import Response
    from summit_rcm.rest_api.utils.spectree.models import (
        InternalServerErrorResponseModel,
        UnauthorizedErrorResponseModel,
    )
    from summit_rcm_hello_world.rest_api.utils.spectree.models import (
        HelloWorldResponseModel,
    )
    from summit_rcm.rest_api.utils.spectree.tags import system_tag
except (ImportError, DocsNotEnabledException):
    from summit_rcm.rest_api.services.spectree_service import DummyResponse as Response

    InternalServerErrorResponseModel = None
    UnauthorizedErrorResponseModel = None
    HelloWorldResponseModel = None
    system_tag = None


spec = SpectreeService()


class HelloWorldResource(object):
    """
    Resource to handle requests of 'Hello World'
    """

    @spec.validate(
        resp=Response(
            HTTP_200=HelloWorldResponseModel,
            HTTP_401=UnauthorizedErrorResponseModel,
            HTTP_500=InternalServerErrorResponseModel,
        ),
        security=SpectreeService().security,
        tags=[system_tag],
    )
    async def on_get(self, _: falcon.asgi.Request, resp: falcon.asgi.Response) -> None:
        """
        Retrieve 'Hello World' message
        """
        try:
            resp.media = {"Message": HelloWorldService().get_hello_world()}  # Must return the status, content_type, and media of the response
            resp.status = falcon.HTTP_200
            resp.content_type = falcon.MEDIA_JSON
        except Exception as exception:
            syslog(
                LOG_ERR,
                f"Unable to get 'Hello World': {str(exception)}",
            )
            resp.status = falcon.HTTP_500

```

**NOTE:** Due to the open source nature of Summit RCM, the addition of plugins creates a dynamically easy way for new endpoint/command additions and improvements to be made. Endpoints/commands can be created to reuse existing Summit RCM services in order to perform specific functions not currently offered. It can also allow for the creation of new services and unrelated endpoints that are needed for specific use-cases.
