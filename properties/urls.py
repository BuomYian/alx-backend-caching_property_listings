from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PropertyViewSet, property_list

# Create a router and register the viewset
router = DefaultRouter()
router.register(r'api', PropertyViewSet, basename='property-api')

urlpatterns = [
    path('', property_list, name='property-list'),
    path('api/', include(router.urls)),
]
