# Project Initialization Guide

This guide documents the complete setup of the Django property listing application with Redis caching and containerized PostgreSQL.

## What Was Initialized

### 1. Django Project Structure
- **Project Name:** `alx_backend_caching_property_listings`
- **Main App:** `properties`
- **Framework:** Django 3.2.18
- **Database:** PostgreSQL
- **Cache:** Redis with django-redis

### 2. Project Files Created

#### Core Django Files
- `manage.py` - Django management script
- `alx_backend_caching_property_listings/settings.py` - Django settings with PostgreSQL and Redis configuration
- `alx_backend_caching_property_listings/urls.py` - URL routing configuration
- `alx_backend_caching_property_listings/wsgi.py` - WSGI application entry point
- `alx_backend_caching_property_listings/asgi.py` - ASGI application entry point

#### Properties App Files
- `properties/models.py` - Property model with fields: title, description, price, location, created_at
- `properties/views.py` - RESTful API views with caching decorators
- `properties/serializers.py` - DRF serializers for Property model
- `properties/admin.py` - Django admin configuration
- `properties/urls.py` - App-specific URL routing
- `properties/migrations/0001_initial.py` - Initial database migration

#### Configuration Files
- `requirements.txt` - Python dependencies
- `docker-compose.yml` - PostgreSQL and Redis service definitions
- `Dockerfile` - Application container image
- `.env` - Environment variables (local development)
- `.env.example` - Environment variables template
- `.gitignore` - Git ignore patterns

### 3. Database Configuration

**PostgreSQL Connection Details:**
```
Engine: django.db.backends.postgresql
Database: property_listings_db
User: postgres
Password: postgres
Host: db (Docker) / localhost (local)
Port: 5432
```

The database is configured to use environment variables for flexibility.

### 4. Redis/Cache Configuration

**Redis Connection Details:**
```
Backend: django_redis.cache.RedisCache
Location: redis://redis:6379/0 (Docker) / redis://localhost:6379/0 (local)
Timeout: 300 seconds (5 minutes)
Key Prefix: property_listings_
```

**Cache Features Enabled:**
- Compression using zlib
- Connection pooling (max 50 connections)
- Socket timeout configuration
- Exception handling (ignores Redis connection errors gracefully)

### 5. Session Configuration

Sessions are configured to use Redis backend for distributed session management:
- Session Engine: `django.contrib.sessions.backends.cache`
- Session Cache Alias: `default` (Redis)

### 6. REST Framework Setup

Installed and configured `djangorestframework` with:
- Pagination: 20 items per page
- Search fields on list views
- Ordering capabilities
- Proper serialization of model data

### 7. CORS Configuration

Cross-Origin Resource Sharing enabled for:
- `http://localhost:3000`
- `http://localhost:8000`
- `http://127.0.0.1:3000`
- `http://127.0.0.1:8000`

## Environment Variables

### Docker Deployment
When running with Docker, the `.env.example` file shows Docker-specific configuration:
```
DB_HOST=db          # Docker service name
REDIS_URL=redis://redis:6379/0
```

### Local Development
For local development, use the `.env` file with:
```
DB_HOST=localhost   # Local machine
REDIS_URL=redis://localhost:6379/0
```

## Running the Application

### Option 1: Docker Compose (Recommended)
```bash
# Start services
docker-compose up --build

# In another terminal, run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Access application
# Web: http://localhost:8000
# Admin: http://localhost:8000/admin
# API: http://localhost:8000/api/properties/
```

### Option 2: Local Development

#### Prerequisites
- PostgreSQL running locally
- Redis running locally

#### Steps
```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with localhost values

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver

# In another terminal, start Redis
redis-server
```

## API Endpoints

### Properties Endpoints
- `GET /api/properties/` - List all properties (paginated, cached)
- `POST /api/properties/` - Create new property
- `GET /api/properties/{id}/` - Get specific property (cached)
- `PUT /api/properties/{id}/` - Update property
- `DELETE /api/properties/{id}/` - Delete property
- `GET /api/properties/stats/` - Get property statistics (cached)

### Admin Panel
- `GET /admin/` - Django admin interface

## Database Schema

### Property Model
```
- id (BigAutoField, Primary Key)
- title (CharField, max_length=200)
- description (TextField)
- price (DecimalField, max_digits=10, decimal_places=2)
- location (CharField, max_length=100)
- created_at (DateTimeField, auto_now_add=True)
```

### Indexes
Properties are ordered by `-created_at` by default for efficient querying.

## Caching Strategy

### View-Level Caching
- List endpoint: 5-minute cache
- Detail endpoint: 5-minute cache
- Stats endpoint: 15-minute cache

### Implementation Details
- Uses `@cache_page` decorator from Django
- Automatic cache invalidation through signals (can be added)
- Redis stores all cached data with compression

## Logging Configuration

Logs are configured to output to:
1. **Console** - All INFO level logs
2. **File** - Cache metrics in `logs/cache_metrics.log`

Log level can be controlled via `LOG_LEVEL` environment variable.

## Docker Services

### PostgreSQL Service
- **Image:** postgres:latest
- **Container Name:** property_listings_db
- **Port:** 5432
- **Volume:** postgres_data (persists data)
- **Health Check:** Enabled

### Redis Service
- **Image:** redis:latest
- **Container Name:** property_listings_redis
- **Port:** 6379
- **Volume:** redis_data (persists data)
- **Persistence:** Enabled (RDB snapshots)
- **Health Check:** Enabled

### Network
Both services are connected on the `alx_network` bridge network for internal communication.

## Next Steps

1. **Add Signal Handlers** - Implement cache invalidation on property updates
2. **Create Test Suite** - Unit and integration tests for caching
3. **Implement Cache Metrics** - Monitor cache hit/miss ratios
4. **Add Filtering** - Location, price range filters with caching
5. **Deploy to Production** - Use proper SECRET_KEY, DEBUG=False

## Troubleshooting

### PostgreSQL Connection Failed
```bash
# Ensure PostgreSQL is running
docker-compose ps db

# Check logs
docker-compose logs db
```

### Redis Connection Failed
```bash
# Ensure Redis is running
docker-compose ps redis

# Test Redis connection
docker-compose exec redis redis-cli ping
```

### Django Database Errors
```bash
# Run migrations
python manage.py migrate

# Check migration status
python manage.py showmigrations
```

## References

- Django Documentation: https://docs.djangoproject.com/en/3.2/
- django-redis: https://github.com/jazzband/django-redis
- Django REST Framework: https://www.django-rest-framework.org/
- Docker Compose: https://docs.docker.com/compose/
