from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from api.cart.views import CartViewSet
from api.category.views import CategoryViewSet, SubCategoryViewSet
from api.comment.views import CommentViewSet
from api.product.views import ProductViewSet, ProductImageViewSet
from api.staff.views import StaffAPIViewSet
router = DefaultRouter() if settings.DEBUG else SimpleRouter()

# router.register("users", UserViewSet)
router.register(r'hodim', StaffAPIViewSet, basename='hodim')
router.register(r'category', CategoryViewSet, basename='category')
router.register(r'subcategory', SubCategoryViewSet, basename='subcategory')
router.register(r'product', ProductViewSet, basename='product')
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'comment', CommentViewSet, basename='comment')
router.register(r'product-image', ProductImageViewSet, basename='product-image')
urlpatterns = router.urls
