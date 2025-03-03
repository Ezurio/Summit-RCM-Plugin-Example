#####################################################################
# Summit Remote Control Manager (RCM) Hello World Plugin
#####################################################################

SUMMIT_RCM_HELLO_WORLD_PLUGIN_VERSION = local
SUMMIT_RCM_HELLO_WORLD_PLUGIN_SITE = $(BR2_EXTERNAL_SUMMIT_SOM_PATH)/externals/summit-rcm/summit_rcm/plugins/hello_world
SUMMIT_RCM_HELLO_WORLD_PLUGIN_SITE_METHOD = local
SUMMIT_RCM_HELLO_WORLD_PLUGIN_LICENSE = Ezurio
SUMMIT_RCM_HELLO_WORLD_PLUGIN_LICENSE_FILES = LICENSE.ezurio
SUMMIT_RCM_HELLO_WORLD_PLUGIN_SETUP_TYPE = setuptools
SUMMIT_RCM_HELLO_WORLD_PLUGIN_DEPENDENCIES = python3 summit-rcm

ifeq ($(BR2_PACKAGE_HOST_PYTHON_CYTHON),y)
SUMMIT_RCM_HELLO_WORLD_PLUGIN_DEPENDENCIES += host-python-cython
endif

SUMMIT_RCM_HELLO_WORLD_PLUGIN_EXTRA_PACKAGES = \
	summit_rcm_hello_world \
	summit_rcm_hello_world/services

ifeq ($(BR2_PACKAGE_SUMMIT_RCM_AT_INTERFACE),y)
	SUMMIT_RCM_HELLO_WORLD_PLUGIN_EXTRA_PACKAGES += summit_rcm_hello_world/at_interface/commands
endif
ifeq ($(BR2_PACKAGE_SUMMIT_RCM_REST_API_V2_ROUTES),y)
    SUMMIT_RCM_HELLO_WORLD_PLUGIN_EXTRA_PACKAGES += summit_rcm_hello_world/rest_api/v2/system
endif
ifeq ($(BR2_PACKAGE_SUMMIT_RCM_REST_API_LEGACY_ROUTES),y)
    SUMMIT_RCM_HELLO_WORLD_PLUGIN_EXTRA_PACKAGES += summit_rcm_hello_world/rest_api/legacy
endif

SUMMIT_RCM_HELLO_WORLD_PLUGIN_ENV = SUMMIT_RCM_HELLO_WORLD_PLUGIN_EXTRA_PACKAGES='$(SUMMIT_RCM_HELLO_WORLD_PLUGIN_EXTRA_PACKAGES)'

$(eval $(python-package))
