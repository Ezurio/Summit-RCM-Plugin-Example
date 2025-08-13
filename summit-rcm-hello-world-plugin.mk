#####################################################################
# Summit Remote Control Manager (RCM) Hello World Plugin
#####################################################################

SUMMIT_RCM_HELLO_WORLD_PLUGIN_VERSION = local
SUMMIT_RCM_HELLO_WORLD_PLUGIN_SITE = $(SUMMIT_RCM_HELLO_WORLD_PLUGIN_PKGDIR)/src
SUMMIT_RCM_HELLO_WORLD_PLUGIN_SITE_METHOD = local
SUMMIT_RCM_HELLO_WORLD_PLUGIN_LICENSE = Ezurio
SUMMIT_RCM_HELLO_WORLD_PLUGIN_LICENSE_FILES = LICENSE.ezurio
SUMMIT_RCM_HELLO_WORLD_PLUGIN_SETUP_TYPE = pep517
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

ifeq ($(BR2_PACKAGE_SUMMIT_RCM_REST_API_DOCS),y)
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

SUMMIT_RCM_HELLO_WORLD_PLUGIN_ENV = SUMMIT_RCM_HELLO_WORLD_PLUGIN_EXTRA_PACKAGES='$(SUMMIT_RCM_HELLO_WORLD_PLUGIN_EXTRA_PACKAGES)'

$(eval $(python-package))
$(eval $(host-python-package))
