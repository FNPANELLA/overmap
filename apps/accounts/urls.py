# apps/accounts/urls.py
from django.urls import path
from .views import UserRegistrationView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,)

urlpatterns = [
    # Endpoint para que un usuario se registre
    path('register/', UserRegistrationView.as_view(), name='register'),
    
    # Endpoint para que un usuario inicie sesión (obtiene tokens)
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # Endpoint para refrescar un token de acceso
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

