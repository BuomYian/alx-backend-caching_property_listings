"""
Utility functions for caching property data.
"""
from django.core.cache import cache
from .models import Property


def get_all_properties():
    """
    Get all properties from cache or database.

    This function implements low-level caching by:
    1. Checking if 'all_properties' exists in Redis cache
    2. If not found, fetching all properties from the database
    3. Storing the queryset in Redis for 1 hour (3600 seconds)
    4. Returning the queryset

    Cache Strategy:
    - Cache Key: 'all_properties'
    - Cache Duration: 1 hour (3600 seconds)
    - Cache Backend: Redis (configured in settings)

    Returns:
        QuerySet: All Property objects, either from cache or database
    """
    # Try to get properties from cache
    all_properties = cache.get('all_properties')

    # If not in cache, fetch from database
    if all_properties is None:
        all_properties = Property.objects.all()
        # Store in cache for 1 hour
        cache.set('all_properties', all_properties, 3600)

    return all_properties
