# Django Property Listing Application with Redis Caching

A comprehensive Django-based property listing application that demonstrates advanced caching strategies, containerized services, and production-ready patterns for high-traffic real estate platforms.

## Table of Contents

- [Overview](#overview)
- [Learning Objectives](#learning-objectives)
- [Key Concepts](#key-concepts)
- [Technology Stack](#technology-stack)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Local Development Setup](#local-development-setup)
  - [Docker Setup](#docker-setup)
- [Configuration](#configuration)
  - [Environment Variables](#environment-variables)
  - [Redis Configuration](#redis-configuration)
  - [Django Settings](#django-settings)
- [Usage](#usage)
  - [Running the Application](#running-the-application)
  - [Creating and Managing Listings](#creating-and-managing-listings)
  - [Monitoring Cache Performance](#monitoring-cache-performance)
- [Caching Strategies](#caching-strategies)
  - [View-Level Caching](#view-level-caching)
  - [Queryset-Level Caching](#queryset-level-caching)
  - [Cache Invalidation with Signals](#cache-invalidation-with-signals)
- [Real-World Use Case](#real-world-use-case)
- [API Reference](#api-reference)
- [Performance Metrics](#performance-metrics)
- [Docker Compose Setup](#docker-compose-setup)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Overview

This project implements a Django-based property listing application that serves as a practical blueprint for building high-performance, scalable web applications. It demonstrates how to effectively implement multi-level caching strategies using Redis while maintaining data consistency and monitoring performance metrics.

The application models a real estate listing platform where:
- **Property listings** are frequently accessed but rarely modified
- **Database load** must be minimized during peak traffic periods
- **Data consistency** must be maintained despite caching layers
- **Performance metrics** are monitored to optimize cache effectiveness

This project is designed for developers who want to understand and implement professional-grade caching solutions in Django applications, mirroring patterns used in production environments for platforms like Zillow, Redfin, and other high-traffic listing services.

## Learning Objectives

Upon completing this project, you will be able to:

1. **Implement Multi-Level Caching**: Set up and configure both view-level and low-level queryset caching strategies
2. **Integrate Redis Cache Backend**: Configure and utilize Redis as the primary cache backend for Django
3. **Containerize Services**: Use Docker to manage PostgreSQL and Redis dependencies in a development environment
4. **Maintain Cache Consistency**: Implement Django signals to automatically invalidate caches when data changes
5. **Analyze Cache Metrics**: Monitor and interpret Redis cache hit/miss ratios and performance statistics
6. **Optimize Database Queries**: Structure queries and caching patterns to minimize database load
7. **Structure Django Projects**: Organize code for maintainability, scalability, and professional standards

## Key Concepts

### Multi-Level Caching

The application implements caching at multiple levels:

- **View-Level Caching**: Caches entire HTTP responses for expensive endpoints
- **Queryset-Level Caching**: Caches database query results at the ORM level
- **Object-Level Caching**: Caches individual model instances or computed properties
- **Cache Hierarchies**: Implements cache invalidation across multiple levels

### Cache Invalidation Techniques

- **Time-Based Expiration**: Automatic expiration of cache entries after a specified duration
- **Event-Based Invalidation**: Using Django signals to invalidate cache when related objects change
- **Selective Invalidation**: Invalidating specific cache keys while preserving others
- **Cache Warming**: Pre-populating cache with frequently accessed data

### Database Optimization

- **Query Optimization**: Reducing N+1 query problems through caching and prefetching
- **Lazy Loading Prevention**: Using `select_related()` and `prefetch_related()` with caching
- **Aggregate Caching**: Caching expensive aggregation queries
- **Connection Pooling**: Leveraging PostgreSQL connection pooling for efficiency

### Containerization Best Practices

- **Service Isolation**: Running PostgreSQL and Redis in separate containers
- **Environment Consistency**: Matching development and production environments
- **Volume Management**: Persisting database and cache data across container lifecycle
- **Network Configuration**: Secure communication between services

## Technology Stack

### Backend Framework
- **Django 3.2+** - Web framework for building the application
- **Django REST Framework** - API development (optional)
- **django-redis** - Django cache backend for Redis integration

### Databases & Caching
- **PostgreSQL 13+** - Primary relational database for persistent storage
- **Redis 6.0+** - In-memory data store for caching
- **psycopg2** - PostgreSQL adapter for Python

### Development & Deployment
- **Docker** - Containerization platform
- **Docker Compose** - Multi-container orchestration
- **Python 3.8+** - Programming language
- **Gunicorn** - WSGI application server

### Monitoring & Logging
- **Python logging** - Built-in logging for cache metrics
- **django-debug-toolbar** - Development performance monitoring
- **Redis CLI** - Manual cache inspection and debugging

## Features

### Core Application Features

✅ **Property Listing Management**
- Create, read, update, and delete property listings
- Search and filter listings by location, price, and features
- View detailed property information

✅ **Multi-Level Caching**
- Automatic view-level caching for list and detail endpoints
- Queryset-level caching for database queries
- Cache warming for popular listings
- Configurable cache timeouts

✅ **Cache Invalidation**
- Automatic cache invalidation on listing creation/update
- Signal-based cache clearing for related objects
- Selective cache invalidation for modified data
- Cache key versioning for zero-downtime updates

✅ **Performance Monitoring**
- Cache hit/miss ratio tracking
- Query execution time logging
- Redis memory usage monitoring
- Response time metrics

✅ **Containerized Environment**
- Docker Compose configuration for PostgreSQL and Redis
- Development and production-ready configurations
- Automatic service health checks
- Volume management for data persistence

✅ **Professional Code Structure**
- Modular application architecture
- Separation of concerns (models, views, services, caching)
- Comprehensive error handling
- Logging and debugging utilities

## Project Structure

```
alx-backend-caching_property_listings/
├── django_app/                          # Main Django project
│   ├── manage.py                        # Django management script
│   ├── requirements.txt                 # Python dependencies
│   ├── .env.example                     # Environment variables template
│   ├── config/                          # Project configuration
│   │   ├── settings.py                  # Django settings
│   │   ├── urls.py                      # URL routing
│   │   ├── wsgi.py                      # WSGI configuration
│   │   └── cache_config.py              # Cache configuration
│   ├── apps/
│   │   └── listings/                    # Property listings app
│   │       ├── models.py                # PropertyListing model
│   │       ├── views.py                 # View functions and caching logic
│   │       ├── urls.py                  # App-specific URLs
│   │       ├── serializers.py           # DRF serializers
│   │       ├── services.py              # Business logic and cache operations
│   │       ├── cache_utils.py           # Cache helper functions
│   │       ├── signals.py               # Django signals for cache invalidation
│   │       └── admin.py                 # Django admin configuration
│   └── utils/
│       ├── cache_metrics.py             # Cache performance tracking
│       ├── logging_config.py            # Logging configuration
│       └── decorators.py                # Custom decorators for caching
├── docker/                              # Docker configuration files
│   ├── Dockerfile                       # Django application image
│   ├── docker-compose.yml               # Multi-container setup
│   ├── nginx.conf                       # Nginx reverse proxy (optional)
│   └── entrypoint.sh                    # Container startup script
├── tests/                               # Test suite
│   ├── test_models.py                   # Model tests
│   ├── test_views.py                    # View tests
│   ├── test_caching.py                  # Caching behavior tests
│   └── test_cache_invalidation.py       # Cache invalidation tests
├── docs/                                # Documentation
│   ├── CACHING_STRATEGY.md              # Detailed caching documentation
│   ├── CACHE_INVALIDATION.md            # Cache invalidation patterns
│   ├── PERFORMANCE.md                   # Performance optimization guide
│   └── API.md                           # API documentation
├── .gitignore                           # Git ignore patterns
├── .dockerignore                        # Docker ignore patterns
├── README.md                            # This file
└── CONTRIBUTING.md                      # Contributing guidelines
```

## Installation

### Prerequisites

Ensure you have the following installed:

- **Python 3.8+** ([Download](https://www.python.org/downloads/))
- **Docker & Docker Compose** ([Download](https://www.docker.com/products/docker-desktop))
- **Git** ([Download](https://git-scm.com/))
- **PostgreSQL 13+** (for local development without Docker)
- **Redis 6.0+** (for local development without Docker)

### Local Development Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/BuomYian/alx-backend-caching_property_listings.git
   cd alx-backend-caching_property_listings
   ```

2. **Create a Virtual Environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r django_app/requirements.txt
   ```

4. **Set Up Environment Variables**

   ```bash
   cp django_app/.env.example django_app/.env
   # Edit .env file with your configuration
   ```

5. **Run Database Migrations**

   ```bash
   cd django_app
   python manage.py migrate
   ```

6. **Create a Superuser**

   ```bash
   python manage.py createsuperuser
   ```

7. **Run Development Server**

   ```bash
   python manage.py runserver
   ```

   Access the application at `http://localhost:8000`

### Docker Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/BuomYian/alx-backend-caching_property_listings.git
   cd alx-backend-caching_property_listings
   ```

2. **Configure Environment Variables**

   ```bash
   cp django_app/.env.example django_app/.env
   ```

3. **Build and Start Containers**

   ```bash
   docker-compose up --build
   ```

4. **Run Migrations in Container**

   ```bash
   docker-compose exec web python manage.py migrate
   ```

5. **Create a Superuser**

   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

6. **Access the Application**

   - Web Application: `http://localhost:8000`
   - Django Admin: `http://localhost:8000/admin`
   - Redis CLI: `docker-compose exec redis redis-cli`

## Configuration

### Environment Variables

Create a `.env` file in the `django_app` directory with the following variables:

```env
# Django Configuration
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
DB_ENGINE=django.db.backends.postgresql
DB_NAME=property_listings_db
DB_USER=postgres
DB_PASSWORD=postgres_password
DB_HOST=db
DB_PORT=5432

# Redis Configuration
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=

# Cache Configuration
CACHE_TIMEOUT=300  # 5 minutes
CACHE_KEY_PREFIX=property_listings_
CACHE_VERSION=1

# Logging
LOG_LEVEL=INFO
```

### Redis Configuration

Redis caching is configured through Django's cache backend. The default configuration in `settings.py`:

```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379/0',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'PARSER_KWARGS': {
                'max_connections': 50,
            },
            'SOCKET_CONNECT_TIMEOUT': 5,
            'SOCKET_TIMEOUT': 5,
            'COMPRESSOR': 'django_redis.compressors.zlib.ZlibCompressor',
            'IGNORE_EXCEPTIONS': True,
        },
        'TIMEOUT': 300,
    }
}
```

### Django Settings

Key Django settings for caching:

```python
# Cache Configuration
CACHE_TIMEOUT = int(os.getenv('CACHE_TIMEOUT', 300))
CACHE_KEY_PREFIX = os.getenv('CACHE_KEY_PREFIX', 'pl_')
CACHE_VERSION = int(os.getenv('CACHE_VERSION', 1))

# Session Configuration (uses Redis)
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

# Logging Configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'logs/cache_metrics.log',
        },
    },
    'loggers': {
        'cache_metrics': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
    },
}
```

## Usage

### Running the Application

#### With Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f web

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

#### Local Development

```bash
# Activate virtual environment
source venv/bin/activate

# Start Django development server
cd django_app
python manage.py runserver

# In another terminal, start Redis (if not using Docker)
redis-server

# In another terminal, start PostgreSQL (if not using Docker)
```

### Creating and Managing Listings

#### Via Django Admin

1. Navigate to `http://localhost:8000/admin`
2. Log in with your superuser credentials
3. Click on "Listings" to manage property listings
4. Create, edit, or delete listings

#### Via API (if DRF is implemented)

```bash
# Get all listings (cached)
curl http://localhost:8000/api/listings/

# Get specific listing (cached)
curl http://localhost:8000/api/listings/1/

# Create new listing
curl -X POST http://localhost:8000/api/listings/ \
  -H "Content-Type: application/json" \
  -d '{"title":"Beautiful House","price":500000,...}'

# Update listing (invalidates cache)
curl -X PUT http://localhost:8000/api/listings/1/ \
  -H "Content-Type: application/json" \
  -d '{"title":"Updated Title",...}'

# Delete listing (invalidates cache)
curl -X DELETE http://localhost:8000/api/listings/1/
```

### Monitoring Cache Performance

#### View Cache Metrics

```bash
# Access cache metrics via Django shell
python manage.py shell

>>> from utils.cache_metrics import CacheMetrics
>>> metrics = CacheMetrics()
>>> metrics.get_hit_ratio()
>>> metrics.get_memory_usage()
>>> metrics.get_cache_stats()
```

#### Monitor Redis Directly

```bash
# Connect to Redis CLI
docker-compose exec redis redis-cli

# Get cache statistics
> INFO stats

# Monitor cache key space
> INFO keyspace

# View specific keys
> KEYS property_listings_*

# Check memory usage
> INFO memory

# Flush cache (use with caution!)
> FLUSHDB
```

#### Check Django Debug Toolbar

Add `django-debug-toolbar` to view detailed cache statistics:

1. Navigate to any page in development mode
2. Click the debug toolbar on the right side
3. Navigate to the "Cache" section to see hit/miss statistics

## Caching Strategies

### View-Level Caching

Caches entire HTTP responses for expensive endpoints.

**Example: Caching the listings list view**

```python
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from .models import PropertyListing

# Function-based view with caching
@cache_page(60 * 5)  # Cache for 5 minutes
def listing_list(request):
    listings = PropertyListing.objects.all()
    return render(request, 'listings/list.html', {'listings': listings})

# Class-based view with caching
@method_decorator(cache_page(60 * 5), name='dispatch')
class PropertyListingListView(ListView):
    model = PropertyListing
    paginate_by = 20
```

**Benefits:**
- Reduces database queries significantly
- Minimal code changes required
- Entire HTTP response cached (including HTML rendering)
- Ideal for static or slowly changing content

**Drawbacks:**
- Less granular control over what's cached
- Cache invalidation affects entire page
- Not suitable for user-specific content

### Queryset-Level Caching

Caches database query results at the ORM level.

**Example: Caching queryset results**

```python
from django.core.cache import cache
from .models import PropertyListing

def get_featured_listings():
    cache_key = 'featured_listings'
    listings = cache.get(cache_key)
    
    if listings is None:
        listings = PropertyListing.objects.filter(
            is_featured=True
        ).select_related('agent').prefetch_related('images')
        cache.set(cache_key, listings, timeout=60 * 15)  # 15 minutes
    
    return listings
```

**Benefits:**
- Granular control over query caching
- Cache can be invalidated per queryset
- Allows combining multiple cached queries
- Efficient memory usage with serialization

**Drawbacks:**
- More code required for each cached query
- Cache key management becomes complex
- Potential for stale data if invalidation is missed

### Cache Invalidation with Signals

Automatically invalidates cache when related data changes.

**Example: Signal-based cache invalidation**

```python
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import PropertyListing

@receiver(post_save, sender=PropertyListing)
def invalidate_listing_cache(sender, instance, created, **kwargs):
    """Invalidate cache when a listing is saved"""
    # Invalidate specific listing cache
    cache.delete(f'listing_{instance.id}')
    
    # Invalidate listings list cache
    cache.delete('property_listings_list')
    cache.delete('featured_listings')
    
    # Invalidate agent's listings cache
    cache.delete(f'agent_{instance.agent_id}_listings')

@receiver(post_delete, sender=PropertyListing)
def invalidate_listing_delete_cache(sender, instance, **kwargs):
    """Invalidate cache when a listing is deleted"""
    cache.delete(f'listing_{instance.id}')
    cache.delete('property_listings_list')
    cache.delete(f'agent_{instance.agent_id}_listings')
```

**Benefits:**
- Automatic cache invalidation with data changes
- Ensures data consistency
- Reduces risk of stale data
- Centralized invalidation logic

**Drawbacks:**
- Signal handlers add overhead on write operations
- Complex signal chains can be hard to debug
- Potential for missing cache keys to invalidate

## Real-World Use Case

### Scenario: High-Traffic Real Estate Listing Platform

**Challenge:** A property listing platform experiences 10,000+ concurrent users during peak hours, with listings being accessed 100+ times per second but modified only a few times per day.

**Database Impact Without Caching:**
- 100 requests/second × 5 queries per page = 500 queries/second
- Each query takes ~100ms on average
- Database CPU usage: 80-90%
- Response time: 500-800ms

**Solution with Multi-Level Caching:**

1. **View-Level Cache (5 minutes)**
   - Cache entire listing list page
   - Cache listing detail page
   - Reduces queries to database by 95%+
   - Response time: 50-100ms

2. **Queryset-Level Cache (15 minutes)**
   - Cache featured listings
   - Cache listings by location
   - Cache agent's listings
   - Handles dynamic filters efficiently

3. **Object-Level Cache (1 hour)**
   - Cache individual listing objects
   - Cache computed properties (days on market, price trends)
   - Cache related objects (agent info, images)

4. **Signal-Based Invalidation**
   - When listing is updated, invalidate only affected caches
   - Other listings remain cached
   - New listings are cached immediately

**Results:**
- Database CPU usage: 10-15% (down from 80%)
- Response time: 50-100ms (down from 500-800ms)
- Concurrent users served per database connection: 10x increase
- Infrastructure cost reduction: 60-70%

## API Reference

### List All Listings

```http
GET /api/listings/
```

**Query Parameters:**
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20)
- `location`: Filter by location
- `min_price`: Minimum price filter
- `max_price`: Maximum price filter
- `bedrooms`: Filter by number of bedrooms

**Response:**

```json
{
  "count": 150,
  "next": "http://api.example.com/listings/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Beautiful Family Home",
      "price": 450000,
      "location": "San Francisco, CA",
      "bedrooms": 4,
      "bathrooms": 2.5,
      "square_feet": 3000,
      "is_featured": true,
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

### Get Single Listing

```http
GET /api/listings/{id}/
```

**Response:**

```json
{
  "id": 1,
  "title": "Beautiful Family Home",
  "description": "A stunning 4-bedroom home...",
  "price": 450000,
  "location": "San Francisco, CA",
  "bedrooms": 4,
  "bathrooms": 2.5,
  "square_feet": 3000,
  "lot_size": 7500,
  "year_built": 2015,
  "agent": {
    "id": 1,
    "name": "John Smith",
    "email": "john@example.com",
    "phone": "+1-555-123-4567"
  },
  "images": [
    {
      "id": 1,
      "url": "https://example.com/images/1.jpg",
      "order": 1
    }
  ],
  "is_featured": true,
  "days_on_market": 15,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### Create Listing

```http
POST /api/listings/
Content-Type: application/json

{
  "title": "New Property",
  "description": "Description here",
  "price": 350000,
  "location": "Oakland, CA",
  "bedrooms": 3,
  "bathrooms": 2,
  "square_feet": 2000,
  "lot_size": 5000,
  "year_built": 2010,
  "agent_id": 1,
  "is_featured": false
}
```

### Update Listing

```http
PUT /api/listings/{id}/
Content-Type: application/json

{
  "title": "Updated Title",
  "price": 375000,
  "is_featured": true
}
```

**Note:** Updates invalidate all related caches automatically.

### Delete Listing

```http
DELETE /api/listings/{id}/
```

**Note:** Deletion invalidates all related caches automatically.

## Performance Metrics

### Cache Hit Ratio

The percentage of requests served from cache vs. database.

- **Target:** 90%+ for production
- **Acceptable:** 70-90%
- **Poor:** <70%

**Monitor with:**

```python
from utils.cache_metrics import CacheMetrics

metrics = CacheMetrics()
hit_ratio = metrics.get_hit_ratio()
print(f"Cache hit ratio: {hit_ratio}%")
```

### Response Time Benchmarks

Typical response times at different cache levels:

| Scenario | Response Time | Database Queries |
|----------|---------------|------------------|
| Cold cache (DB query) | 150-300ms | 5 queries |
| Warm cache (Redis hit) | 10-50ms | 0 queries |
| View-level cache | 5-20ms | 0 queries |

### Memory Usage

Redis memory usage guidelines:

- **Development:** 100MB - 500MB
- **Production (10K users):** 500MB - 2GB
- **Large scale (100K+ users):** 2GB - 10GB+

Monitor with:

```bash
redis-cli INFO memory
```

### Database Load Reduction

With proper caching:

- **CPU usage reduction:** 70-80%
- **Connection usage reduction:** 60-70%
- **Query count reduction:** 90-95%

## Docker Compose Setup

### docker-compose.yml Configuration

```yaml
version: '3.8'

services:
  web:
    build:
      context: .
      dockerfile: docker/Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
      - DB_HOST=db
      - REDIS_HOST=redis
    depends_on:
      - db
      - redis
    volumes:
      - ./django_app:/app
    command: gunicorn config.wsgi:application --bind 0.0.0.0:8000

  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=property_listings_db
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:6-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
  redis_data:
```

## Testing

### Run Tests

```bash
# Run all tests
python manage.py test

# Run specific test module
python manage.py test apps.listings.tests.test_caching

# Run with verbose output
python manage.py test -v 2

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

### Test Categories

**Unit Tests:** Test individual functions and methods
```bash
python manage.py test apps.listings.tests.test_models
```

**Integration Tests:** Test interactions between components
```bash
python manage.py test apps.listings.tests.test_views
```

**Cache Tests:** Test caching behavior and invalidation
```bash
python manage.py test apps.listings.tests.test_caching
```

## Troubleshooting

### Issue: Redis Connection Error

**Problem:** `ConnectionError: Error 111 connecting to localhost:6379`

**Solution:**
```bash
# Check if Redis is running
redis-cli ping

# If using Docker, check container status
docker-compose ps redis

# Restart Redis
docker-compose restart redis
```

### Issue: Database Connection Error

**Problem:** `OperationalError: could not connect to server`

**Solution:**
```bash
# Check PostgreSQL status
docker-compose ps db

# Check database credentials in .env file
# Restart database container
docker-compose restart db

# Check PostgreSQL logs
docker-compose logs db
```

### Issue: Cache Not Being Invalidated

**Problem:** Listings are updated but cache shows old data

**Solution:**
1. Verify signals are properly connected in `apps.py`
2. Check Redis connection is working
3. Manually clear cache:
   ```bash
   python manage.py shell
   >>> from django.core.cache import cache
   >>> cache.clear()
   ```
4. Check logs for signal execution errors

### Issue: High Memory Usage in Redis

**Problem:** Redis consuming too much memory

**Solution:**
1. Check cache timeout settings in `settings.py`
2. Reduce `CACHE_TIMEOUT` value
3. Implement cache eviction policies:
   ```bash
   redis-cli CONFIG SET maxmemory-policy allkeys-lru
   ```
4. Monitor memory usage:
   ```bash
   redis-cli INFO memory
   ```

### Issue: Slow Response Times Despite Caching

**Problem:** Pages still loading slowly despite cache

**Solution:**
1. Check cache hit ratio:
   ```python
   metrics = CacheMetrics()
   print(metrics.get_hit_ratio())
   ```
2. Verify cache is actually being used (check debug logs)
3. Check for N+1 query problems with debug toolbar
4. Ensure `select_related()` and `prefetch_related()` are used
5. Profile views with Django debug toolbar

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Write or update tests as needed
5. Ensure all tests pass (`python manage.py test`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

### Code Standards

- Follow PEP 8 style guide
- Write meaningful commit messages
- Include docstrings for all functions and classes
- Write tests for new features
- Update documentation as needed

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Additional Resources

### Documentation

- [Django Caching Documentation](https://docs.djangoproject.com/en/3.2/topics/cache/)
- [django-redis Documentation](https://github.com/jazzband/django-redis)
- [Redis Documentation](https://redis.io/documentation)
- [Docker Documentation](https://docs.docker.com/)

### Related Articles

- [Effective Caching Strategies for Django Applications](https://docs.djangoproject.com/en/3.2/topics/cache/optimization/)
- [Real Estate Tech Stack Insights](https://www.example.com)
- [Scaling Web Applications with Redis](https://www.example.com)

### Community

- [Django Community](https://www.djangoproject.com/community/)
- [Stack Overflow - Django Tag](https://stackoverflow.com/questions/tagged/django)
- [Reddit - r/django](https://www.reddit.com/r/django/)

## Support

For issues, questions, or suggestions:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review existing [GitHub Issues](https://github.com/BuomYian/alx-backend-caching_property_listings/issues)
3. Create a new GitHub Issue with detailed information
4. Contact the development team

---

**Last Updated:** January 2026

**Version:** 1.0.0

**Maintainers:** BuomYian and Contributors
