from rest_framework.routers import DefaultRouter

from .views import OrderItemViewSet


router = DefaultRouter()
router.register('', OrderItemViewSet, 'items')

urlpatterns = router.urls