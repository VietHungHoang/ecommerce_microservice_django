from django.contrib import admin
from django.urls import path, include
urlpatterns = [
    path('admin/', admin.site.urls),
    # Trỏ tất cả request tới '/api/' vào urls của app 'customers'
    path('api/', include('customers.urls')),
]
