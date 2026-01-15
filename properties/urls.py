from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PropertyViewSet

# Create a router and register the viewset
router = DefaultRouter()
router.register(r'', PropertyViewSet, basename='property')

urlpatterns = [
    path('', include(router.urls)),
]
