# Quick Start Guide

## 🚀 Start Development Server (5 minutes)

```bash
# 1. Navigate to project
cd /home/buomyian/alx-backend-caching_property_listings

# 2. Activate virtual environment
source .venv/bin/activate

# 3. Start Redis (optional, in another terminal)
redis-server

# 4. Start Django server
python manage.py runserver

# 5. Open in browser
# http://localhost:8000/api/properties/
# http://localhost:8000/admin/
```

**Admin Login**:
- Username: `admin`
- Email: `admin@example.com`

---

## 🐳 Start with Docker (10 minutes)

```bash
# 1. Navigate to project
cd /home/buomyian/alx-backend-caching_property_listings

# 2. Start all services
docker-compose up -d

# 3. Run migrations (in another terminal)
docker-compose exec web python manage.py migrate

# 4. Create superuser
docker-compose exec web python manage.py createsuperuser

# 5. Open in browser
# http://localhost:8000
```

**Stop services**:
```bash
docker-compose down
```

---

## 📊 API Endpoints

### Properties
```bash
# List properties (paginated, cached)
GET http://localhost:8000/api/properties/

# Get single property (cached)
GET http://localhost:8000/api/properties/{id}/

# Create property
POST http://localhost:8000/api/properties/
Content-Type: application/json
{
  "title": "Beautiful House",
  "description": "A wonderful property",
  "price": "500000.00",
  "location": "San Francisco, CA"
}

# Update property (invalidates cache)
PUT http://localhost:8000/api/properties/{id}/

# Delete property (invalidates cache)
DELETE http://localhost:8000/api/properties/{id}/

# Get statistics (cached)
GET http://localhost:8000/api/properties/stats/
```

### Admin Panel
```
GET http://localhost:8000/admin/
```

---

## 🛠️ Common Commands

### Django Management
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Shell access
python manage.py shell

# Run tests
python manage.py test

# Check configuration
python manage.py check

# View routes
python manage.py show_urls
```

### Database
```bash
# Reset database (delete all data)
rm db.sqlite3
python manage.py migrate

# Access SQLite database
sqlite3 db.sqlite3
```

### Redis
```bash
# Check Redis connection
redis-cli ping

# View all cache keys
redis-cli KEYS "*"

# View cache statistics
redis-cli INFO stats

# Clear cache
redis-cli FLUSHDB

# Monitor cache in real-time
redis-cli MONITOR
```

---

## 📝 Sample Data Creation

```bash
python manage.py shell
```

```python
from properties.models import Property
from decimal import Decimal

# Create properties
properties_data = [
    {
        "title": "Modern Downtown Apartment",
        "description": "Stunning city views with modern amenities",
        "price": Decimal("750000.00"),
        "location": "San Francisco, CA"
    },
    {
        "title": "Spacious Family Home",
        "description": "4 bedrooms, 2.5 baths on a quiet street",
        "price": Decimal("550000.00"),
        "location": "Oakland, CA"
    },
    {
        "title": "Cozy Studio",
        "description": "Perfect for first-time buyers",
        "price": Decimal("350000.00"),
        "location": "Berkeley, CA"
    }
]

for data in properties_data:
    Property.objects.create(**data)
    
print(f"Created {Property.objects.count()} properties")
```

---

## 🔍 Debugging

### Check Caching
```bash
# Monitor Redis in real-time
redis-cli MONITOR

# Check what's cached
redis-cli KEYS "property_listings_*"

# Get cached value
redis-cli GET "property_listings_key"
```

### Django Debug
```bash
# Enable all logging
# Edit settings.py:
LOGGING = {
    'loggers': {
        'django': {'level': 'DEBUG'},
    }
}

# Check migrations
python manage.py showmigrations

# Validate configuration
python manage.py check --deploy
```

### Database Debug
```bash
# View migrations status
python manage.py showmigrations properties

# View database schema
.schema  # in sqlite3 shell

# Check table structure
sqlite3 db.sqlite3
> .schema properties_property
```

---

## 📦 Environment Configuration

### Development (.env)
```env
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
CACHE_TIMEOUT=300
```

### Production (.env)
```env
DEBUG=False
ALLOWED_HOSTS=example.com,www.example.com
DB_ENGINE=django.db.backends.postgresql
DB_NAME=property_listings_db
DB_USER=postgres
DB_PASSWORD=<strong-password>
DB_HOST=db
DB_PORT=5432
REDIS_URL=redis://redis:6379/0
SECRET_KEY=<strong-secret-key>
```

---

## 🔗 Important Files

| File | Purpose |
|------|---------|
| `manage.py` | Django management script |
| `requirements.txt` | Python dependencies |
| `.env` | Environment variables |
| `docker-compose.yml` | Docker services configuration |
| `alx_backend_caching_property_listings/settings.py` | Django settings |
| `properties/models.py` | Data models |
| `properties/views.py` | API views |
| `properties/serializers.py` | DRF serializers |

---

## 📊 Performance Tips

1. **Verify caching is working**:
   ```bash
   # First request: check response time (slower)
   curl -w "@-" -o /dev/null -s http://localhost:8000/api/properties/
   
   # Second request: should be faster (cached)
   curl -w "@-" -o /dev/null -s http://localhost:8000/api/properties/
   ```

2. **Monitor Redis memory**:
   ```bash
   redis-cli INFO memory
   ```

3. **Check query count**:
   ```python
   from django.db import connection
   from django.test.utils import CaptureQueriesContext
   
   with CaptureQueriesContext(connection) as context:
       # Your code here
       pass
   print(f"Queries: {len(context.captured_queries)}")
   ```

---

## 🚨 Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError` | Activate venv: `source .venv/bin/activate` |
| Redis connection failed | Start Redis: `redis-server` or use Docker |
| PostgreSQL connection failed | Use SQLite (default) or `docker-compose up` |
| Database locked | Close other connections: `python manage.py shell` |
| Permission denied | Check file permissions, run as user (not sudo) |

---

## 📖 Documentation Links

- Complete Setup: [SETUP.md](SETUP.md)
- Project Details: [README.md](README.md)
- Full Initialization: [INITIALIZATION_COMPLETE.md](INITIALIZATION_COMPLETE.md)
- Django Docs: https://docs.djangoproject.com/
- DRF Docs: https://www.django-rest-framework.org/

---

**Ready to go! Happy coding! 🎉**
