from application import settings

# ================================================= #
# ***************** 插件配置区开始 *******************
# ================================================= #
# 路由配置
plugins_url_patterns = [
    {"re_path": r'api/dvadmin_ak_sk/', "include": "dvadmin_ak_sk.urls"},
]
# app 配置
apps = ['dvadmin_ak_sk']
# 共享app配置(用于租户管理)
tenant_shared_apps = []
# 配置中间件
authentication_classes = ['dvadmin_ak_sk.libs.authentication.AkSkAuthentication']
# ================================================= #
# ******************* 插件配置区结束 *****************
# ================================================= #


# ********** 赋值到 settings 中 **********
settings.INSTALLED_APPS += [app for app in apps if app not in settings.INSTALLED_APPS]
settings.TENANT_SHARED_APPS += tenant_shared_apps
settings.REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"] = tuple(
    list(settings.REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"]) + authentication_classes)
# ********** 注册路由 **********
settings.PLUGINS_URL_PATTERNS += plugins_url_patterns
