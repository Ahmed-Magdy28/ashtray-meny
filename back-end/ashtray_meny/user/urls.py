from django.urls import path, include
from rest_framework.routers import DefaultRouter
from user import views

router = DefaultRouter()
router.register('users', views.UserViewSet)           # Handles /api/users/
router.register('shops', views.ShopViewSet)           # Handles /api/shops/
router.register('products', views.ProductViewSet)     # Handles /api/products/
router.register('categories', views.CategoryViewSet)  # Handles /api/categories/
router.register('reviews', views.ReviewViewSet)       # Handles /api/reviews/
router.register('orders', views.OrderViewSet)         # Handles /api/orders/
router.register('wishlists', views.WishListViewSet)   # Handles /api/wishlists/

urlpatterns = [
    path('', include(router.urls)),
    # Includes all the registered routes under /api/
]