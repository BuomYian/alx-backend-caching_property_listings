"""
Signal handlers for cache invalidation when Property objects change.
"""
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Property


@receiver(post_save, sender=Property)
def invalidate_property_cache_on_save(sender, instance, created, **kwargs):
    """
    Invalidate the all_properties cache when a Property is created or updated.

    This signal handler is triggered after a Property object is saved (created or updated).
    It removes the 'all_properties' cache key from Redis to ensure the next request
    fetches fresh data from the database.

    Args:
        sender: The model class (Property)
        instance: The instance of the model being saved
        created: Boolean indicating if this is a new object (True) or update (False)
        **kwargs: Additional keyword arguments
    """
    cache.delete('all_properties')


@receiver(post_delete, sender=Property)
def invalidate_property_cache_on_delete(sender, instance, **kwargs):
    """
    Invalidate the all_properties cache when a Property is deleted.

    This signal handler is triggered after a Property object is deleted.
    It removes the 'all_properties' cache key from Redis to ensure the next request
    fetches fresh data from the database.

    Args:
        sender: The model class (Property)
        instance: The instance of the model being deleted
        **kwargs: Additional keyword arguments
    """
    cache.delete('all_properties')
