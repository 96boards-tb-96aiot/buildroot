FACE_SERVICE_SITE = $(TOPDIR)/../app/face
FACE_SERVICE_SITE_METHOD = local
FACE_SERVICE_INSTALL_STAGING = YES

# add dependencies
FACE_SERVICE_DEPENDENCIES = hal adk messenger rkrga rkfb camerahal rkcamera process_units

# add package dependencies & opts
ifeq ($(BR2_PACKAGE_SQLITE),y)
    FACE_SERVICE_DEPENDENCIES += sqlite
    FACE_SERVICE_CONF_OPTS += -DUSE_SQLITE=1
endif

ifeq ($(BR2_PACKAGE_DATABASE),y)
    FACE_SERVICE_DEPENDENCIES += database
    FACE_SERVICE_CONF_OPTS += -DUSE_DATABASE=1
endif

ifeq ($(BR2_PACKAGE_RKFACE),y)
ifeq ($(BR2_PACKAGE_RKFACE_DETECTION),y)
    FACE_SERVICE_DEPENDENCIES += rkface
    FACE_SERVICE_CONF_OPTS += -DUSE_RKFACE_DETECT=1
endif
ifeq ($(BR2_PACKAGE_RKFACE_RECOGNITION),y)
    FACE_SERVICE_DEPENDENCIES += rkface
    FACE_SERVICE_CONF_OPTS += -DUSE_RKFACE_RECOGNIZE=1
endif

ifeq ($(BR2_PACKAGE_RKLIVE_DETECTION_2D),y)
    FACE_SERVICE_DEPENDENCIES += rkface
    FACE_SERVICE_CONF_OPTS += -DUSE_RKLIVE_DETECT_2D=1
endif

ifeq (${RK_HAS_DEPTH_CAMERA},y)
    FACE_SERVICE_DEPENDENCIES += rkface
    FACE_SERVICE_CONF_OPTS += -DUSE_RKLIVE_DETECT_3D=1
endif
endif

ifeq ($(BR2_PACKAGE_FACE_SERVICE_USE_UVC),y)
    FACE_SERVICE_DEPENDENCIES += mpp librkuvc
    FACE_SERVICE_CONF_OPTS += -DUSE_UVC=1
endif

ifeq ($(BR2_PACKAGE_FACE_SERVICE_USE_MJPEG_CAMERA),y)
    FACE_SERVICE_DEPENDENCIES += mpp
    FACE_SERVICE_CONF_OPTS += -DUSE_MJPEG_CAMERA=1
endif

ifeq ($(BR2_PACKAGE_FACE_SERVICE_FACE_CAPTURE),y)
    FACE_SERVICE_DEPENDENCIES += mpp rkmedia
    FACE_SERVICE_CONF_OPTS += -DUSE_FACE_CAPTURE=1
endif

ifeq ($(BR2_PACKAGE_FACE_SERVICE_H264_ENCODE),y)
    FACE_SERVICE_DEPENDENCIES += mpp rkmedia
    FACE_SERVICE_CONF_OPTS += -DUSE_H264_ENCODER=1
endif

ifeq ($(BR2_PACKAGE_RV1108_VENDOR_STORAGE),y)
    FACE_SERVICE_DEPENDENCIES += rv1108_vendor_storage
    FACE_SERVICE_CONF_OPTS += -DUSE_VENDOR_STORAGE=1
endif

FACE_SERVICE_CONF_OPTS += \
    -DDISPLAY_RESOLUTION=$(call qstrip,$(RK_UI_RESOLUTION)) \
    -DMAX_FEATURE_OF_USER=$(BR2_PACKAGE_FACE_SERVICE_MAX_FEATURE_OF_USER) \
    -DBOARD_VERSION=$(call qstrip,rv1108-$(RK_TARGET_BOARD_VERSION)) \
    -DSTORAGE_TYPE=$(RK_STORAGE_TYPE)

define FACE_SERVICE_INSTALL_INIT_SYSV
    $(INSTALL) -m 0644 -D package/rockchip/rv1108_package/app/face_service/face_service.conf \
                    $(TARGET_DIR)/etc/face_service.conf
endef

$(eval $(cmake-package))
