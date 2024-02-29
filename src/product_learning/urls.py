from product_learning.views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'products', ProductsViewSet, basename='products')
urlpatterns = router.urls

