"""
Properties app for managing property listings with caching support.

This app provides:
- Property model for storing property listings
- API endpoints for CRUD operations
- Low-level caching for property querysets
- Signal-based cache invalidation
"""
default_app_config = 'properties.apps.PropertiesConfig'
