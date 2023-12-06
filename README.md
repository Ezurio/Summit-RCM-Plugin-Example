# Summit-RCM-Plugin-Example
Summit RCM Plugin Example Repo

This repo is meant as a working example of creating a simple plugin for Summit-RCM

## Getting Started
1. Create the directory tree for a Summit-RCM Plugin:
```bash
.
├── plugins  # Root plugins directory
│   └── hello_world  # Name of the plugin
│       ├── setup.py
│       └── summit_rcm_hello_world  # summit_rcm_NAME_OF_PLUGIN
│           ├── __init__.py
│           ├── at_interface  # If the plugin includes an AT Command
│           │   └── commands
│           │       ├── __init__.py
│           │       └── hello_world_command.py
│           ├── rest_api
│           │   ├── legacy
│           │   │   ├── __init__.py
│           │   │   └── hello_world.py
│           │   └── v2
│           │       └── system
│           │           ├── __init__.py
│           │           └── hello_world.py
│           └── services
│               ├── __init__.py
│               └── hello_world_service.py
```

2. Create the directory for a Summit-RCM package in NAME_OF_EXTERNAL-external/package/:
```bash
└── NAME_OF_EXTERNAL-external
    └── package
		├── Config.in  # Config.in file for any packages, which will be modified later
        └── summit-rcm-hello-world-plugin  # summit-rcm-NAME-OF-PLUGIN-plugin
            ├── Config.in  # Config.in for the plugin
            └── summit-rcm-hello-world-plugin.mk  # Makefile for the plugin
```
 
3. Update the NAME_OF_EXTERNAL-external/package/Config.in file seen above to include the plugin Config.in:
```bash
source "$BR2_EXTERNAL_NAME_OF_EXTERNAL_PATH/package/summit-rcm-hello-world-plugin/Config.in"
```

4. Create the content of the Config.in file for the plugin, which will include any configuration options/dependencies:
```bash
config BR2_PACKAGE_SUMMIT_RCM_HELLO_WORLD_PLUGIN  # Name of Plugin
	bool "Hello World plugin for Summit RCM"
	depends on BR2_PACKAGE_SUMMIT_RCM  # Dependent on Summit-RCM
	default y
	help
		Add Hello World configuration support to Summit RCM.
```

5. Create the content of the Makefile for the plugin:
```bash
#####################################################################
# Summit Remote Control Manager (RCM) Hello World Plugin
#####################################################################

SUMMIT_RCM_HELLO_WORLD_PLUGIN_VERSION = local  # All Makefile parameters will be in the form of SUMMIT_RCM_NAME_OF_PLUGIN_PLUGIN_THE_PARAMETER
SUMMIT_RCM_HELLO_WORLD_PLUGIN_SITE = PATH_TO_EXTERNAL_SPECIFIC_PLUGINS_DIRECTORY/plugins/hello_world  # Location of plugin code
SUMMIT_RCM_HELLO_WORLD_PLUGIN_SITE_METHOD = local
SUMMIT_RCM_HELLO_WORLD_PLUGIN_SETUP_TYPE = setuptools
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

SUMMIT_RCM_HELLO_WORLD_PLUGIN_ENV = SUMMIT_RCM_HELLO_WORLD_PLUGIN_EXTRA_PACKAGES='$(SUMMIT_RCM_HELLO_WORLD_PLUGIN_EXTRA_PACKAGES)'  # Sets the environment to the extra packages

$(eval $(python-package))  # Run the setup.py file for the plugin
```

5. Create the contents of the setup.py file for the plugin:
```python
#!/usr/bin/python

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
environment_variable_value = os.environ.get("SUMMIT_RCM_HELLO_WORLD_PLUGIN_EXTRA_PACKAGES", "")  # Get the plugin extra packages
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

    modules_to_exclude = []

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
        ext_modules=ext_modules
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

6. Create the contents for the __init__.py of the plugin:
```python
"""Init File to setup the Hello World Plugin"""
from syslog import syslog, LOG_ERR


def get_at_commands():  # Must be named "get_at_commands()"
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
        syslog(LOG_ERR, f"Error Importing Hello World AT Commands: {str(exception)}")
    return at_commands  # Return a list of AT Commands


async def get_legacy_routes():  # Must be async and named "get_legacy_routes()"
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
        syslog(LOG_ERR, f"Error Importing Hello World legacy routes: {str(exception)}")
    return routes  # Return a dict of API routes and API Resources


async def get_v2_routes():  # Must be async and named "get_legacy_routes()"
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
        syslog(LOG_ERR, f"Error Importing Hello World v2 routes: {str(exception)}")
    return routes  # Return a dict of API routes and API Resources
```

7. Create the contents of the AT Commands or API files needed

Ex: AT Command
```python
"""
File that consists of the HelloWorld Command Functionality
"""
from typing import List, Tuple
from syslog import LOG_ERR, syslog
from summit_rcm.at_interface.commands.command import Command  # Must import Command base class
from summit_rcm_hello_world.services.hello_world_service import HelloWorldService


class HelloWorldCommand(Command):  # Must take in the Command base class and requires an execute, parse params, usage, signature, and name function
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
        resp.status = falcon.HTTP_200  # Must specify the status, content_type, and media of the response
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
```

Ex: V2 Endpoint
```python
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
            resp.media["Message"] = HelloWorldService().get_hello_world()  # Must return the status, content_type, and media of the response
            resp.status = falcon.HTTP_200
            resp.content_type = falcon.MEDIA_JSON
        except Exception as exception:
            syslog(
                LOG_ERR,
                f"Unable to get 'Hello World': {str(exception)}",
            )
            resp.status = falcon.HTTP_500
```

**NOTE:** Due to the open source nature of Summit-RCM, the addition of plugins creates a dynamically easy way for new endpoint/command additions and improvements to be made. Endpoints/commands can be created to reuse existing Summit-RCM services in order to perform specific functions not currently offered. It can also allow for the creation of new services and unrelated endpoints that are needed for specific use-cases.