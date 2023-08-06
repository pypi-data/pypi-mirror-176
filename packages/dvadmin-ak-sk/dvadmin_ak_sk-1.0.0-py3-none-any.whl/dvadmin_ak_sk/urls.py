from rest_framework.routers import DefaultRouter

from dvadmin_ak_sk.views.ak_sk_manage import AkSkManageViewSet

router = DefaultRouter()
router.register(r'key_manage', AkSkManageViewSet)

urlpatterns = [
]
urlpatterns += router.urls
