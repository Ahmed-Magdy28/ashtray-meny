from django.urls import path, include
from rest_framework.routers import DefaultRouter
from user import views
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register('users', views.UserViewSet)           # Handles /api/users/
router.register('shops', views.ShopViewSet)           # Handles /api/shops/
router.register('products', views.ProductViewSet)     # Handles /api/products/
router.register('categories', views.CategoryViewSet)  # Handles /api/categories/
router.register('reviews', views.ReviewViewSet)       # Handles /api/reviews/
router.register('orders', views.OrderViewSet)         # Handles /api/orders/
router.register('wishlists', views.WishListViewSet)   # Handles /api/wishlists/

urlpatterns = [
    path('', include(router.urls)),  # Include all the registered routes
    path('user/create/', views.CreateUserView.as_view(), name='user-create'),  # User registration
    path('user/login/', views.LoginView.as_view(), name='user-login'),  # User login (JWT)
    path('user/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),  # Token refresh for JWT
]
