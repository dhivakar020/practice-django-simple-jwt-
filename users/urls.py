from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('login_page/', views.login_page, name='login_page'),
    path('signup/', views.signup_page, name='login_page'),  # This maps to the login page view  # This maps to the login page view
    #path('logout/', views.logout_view, name='logout'),
    path('rider-dashboard/', views.rider_dashboard, name='rider_dashboard'),
    path('driver-dashboard/', views.driver_dashboard, name='driver_dashboard'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # JWT token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh JWT token
]