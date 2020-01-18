################################################################################
#
# web_ui_wifi
#
################################################################################

WEB_UI_WIFI_VERSION = 20200114
WEB_UI_WIFI_SITE_METHOD = local
WEB_UI_WIFI_SITE = ${TOPDIR}/package/rockchip/web_ui_wifi/src

define WEB_UI_WIFI_INSTALL_TARGET_CMDS
	mkdir -p ${TARGET_DIR}/var/www
	cp -rf $(@D)/* ${TARGET_DIR}/var/www
endef

$(eval $(generic-package))
