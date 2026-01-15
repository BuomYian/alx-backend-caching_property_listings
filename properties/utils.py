"""
Utility functions for caching property data.
"""
import logging
from django.core.cache import cache
from django_redis import get_redis_connection
from .models import Property

logger = logging.getLogger(__name__)


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


def get_redis_cache_metrics():
    """
    Retrieve and analyze Redis cache hit/miss metrics.

    This function:
    1. Connects to Redis via django_redis
    2. Gets keyspace_hits and keyspace_misses from Redis INFO
    3. Calculates hit ratio (hits / (hits + misses))
    4. Logs metrics and returns a dictionary

    Returns:
        dict: Contains the following keys:
            - 'keyspace_hits' (int): Number of cache hits
            - 'keyspace_misses' (int): Number of cache misses
            - 'hit_ratio' (float): Hit ratio as percentage (0.0 to 100.0)
            - 'total_requests' (int): Total cache requests (hits + misses)
    """
    try:
        # Connect to Redis
        redis_conn = get_redis_connection('default')

        # Get Redis INFO stats
        info = redis_conn.info()

        # Extract hits and misses
        keyspace_hits = info.get('keyspace_hits', 0)
        keyspace_misses = info.get('keyspace_misses', 0)

        # Calculate total requests and hit ratio
        total_requests = keyspace_hits + keyspace_misses
        hit_ratio = (keyspace_hits / total_requests *
                     100) if total_requests > 0 else 0.0

        # Create metrics dictionary
        metrics = {
            'keyspace_hits': keyspace_hits,
            'keyspace_misses': keyspace_misses,
            'hit_ratio': hit_ratio,
            'total_requests': total_requests,
        }

        # Log metrics
        logger.info(
            f"Redis Cache Metrics - Hits: {keyspace_hits}, Misses: {keyspace_misses}, "
            f"Hit Ratio: {hit_ratio:.2f}%, Total Requests: {total_requests}"
        )

        return metrics

    except Exception as e:
        logger.error(f"Error retrieving Redis cache metrics: {str(e)}")
        return {
            'keyspace_hits': 0,
            'keyspace_misses': 0,
            'hit_ratio': 0.0,
            'total_requests': 0,
            'error': str(e),
        }
