from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from api.cart.views import CartViewSet, WishlistViewSet
from api.category.views import CategoryViewSet, SubCategoryViewSet
from api.comment.views import CommentViewSet
from api.order.views import OrderViewSet
from api.product.views import ProductViewSet, ProductImageViewSet, RemainingProductViewSet
from api.staff.views import StaffAPIViewSet
from api.uom.views import UomGroupViewSet, UomViewSet
from api.warehouse.views import WarehouseViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

# router.register("users", UserViewSet)
router.register(r'hodim', StaffAPIViewSet, basename='hodim')
router.register(r'category', CategoryViewSet, basename='category')
router.register(r'subcategory', SubCategoryViewSet, basename='subcategory')
router.register(r'product', ProductViewSet, basename='product')
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'comment', CommentViewSet, basename='comment')
router.register(r'product-image', ProductImageViewSet, basename='product-image')
router.register(r'order', OrderViewSet, basename='order')
router.register(r'wishlist', WishlistViewSet, basename='wishlist')
router.register(r'uom-group', UomGroupViewSet, basename='uom-group')
router.register(r'uom', UomViewSet, basename='uom')
router.register(r'warehouse', WarehouseViewSet, basename='warehouse')
router.register(r'remaining-product', RemainingProductViewSet, basename='remaining-product')
urlpatterns = router.urls
