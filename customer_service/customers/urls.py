# customers/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet, AddressViewSet

# Tạo router và đăng ký viewsets với nó.
router = DefaultRouter()
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'addresses', AddressViewSet, basename='address')

# API URLs được xác định tự động bởi router.
urlpatterns = [
    path('', include(router.urls)),
]