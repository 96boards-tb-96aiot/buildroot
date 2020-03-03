################################################################################
#
# web_ui_python
#
################################################################################

WEB_UI_PYTHON_VERSION = 20200114
WEB_UI_PYTHON_SITE_METHOD = local
WEB_UI_PYTHON_SITE = ${TOPDIR}/package/rockchip/web_ui_python/webui
WEB_UI_PYTHON_EXTER_FILE = $(TOPDIR)/package/rockchip/web_ui_python

define WEB_UI_PYTHON_INSTALL_TARGET_CMDS
	mkdir -p ${TARGET_DIR}/usr/lib/webui
	cp -rf $(@D)/* ${TARGET_DIR}/usr/lib/webui
	$(INSTALL) -D -m 755 $(WEB_UI_PYTHON_EXTER_FILE)/S43webserver  $(TARGET_DIR)/etc/init.d/S43webserver
	$(INSTALL) -D -m 755 $(WEB_UI_PYTHON_EXTER_FILE)/toybrick.conf  $(TARGET_DIR)/etc/toybrick.conf 
endef

$(eval $(generic-package))
