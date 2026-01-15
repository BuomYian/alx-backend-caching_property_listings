from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache import cache
from django.http import JsonResponse
from .models import Property
from .serializers import PropertySerializer


class PropertyViewSet(viewsets.ModelViewSet):
    """
    API viewset for managing properties with caching support.
    """
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    search_fields = ['title', 'description', 'location']
    ordering_fields = ['created_at', 'price']
    ordering = ['-created_at']

    @method_decorator(cache_page(60 * 5))  # Cache for 5 minutes
    def list(self, request, *args, **kwargs):
        """
        List all properties with caching enabled.
        """
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60 * 5))  # Cache for 5 minutes
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a single property with caching enabled.
        """
        return super().retrieve(request, *args, **kwargs)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """
        Get cache statistics.
        """
        cache_key = 'property_stats'
        stats = cache.get(cache_key)

        if stats is None:
            total_properties = Property.objects.count()
            total_value = sum(p.price for p in Property.objects.all())

            stats = {
                'total_properties': total_properties,
                'total_value': str(total_value),
            }
            # Cache for 15 minutes
            cache.set(cache_key, stats, timeout=60 * 15)

        return Response(stats)


@cache_page(60 * 15)  # Cache for 15 minutes
def property_list(request):
    """
    View to display all properties with caching enabled.

    This view returns all properties cached in Redis for 15 minutes.
    The @cache_page decorator caches the entire HTTP response.

    Args:
        request: HTTP request object

    Returns:
        JsonResponse with all properties data
    """
    properties = Property.objects.all().order_by('-created_at')
    data = {
        'properties': [
            {
                'id': prop.id,
                'title': prop.title,
                'description': prop.description,
                'price': float(prop.price),
                'location': prop.location,
                'created_at': prop.created_at.isoformat(),
            }
            for prop in properties
        ],
        'total_count': properties.count(),
    }
    return JsonResponse(data)
