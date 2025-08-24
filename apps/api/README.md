# Homlo API - Backend

FastAPI-based backend for the Homlo platform - Pakistan's premier Airbnb-style marketplace.

## 🚀 Features

- **FastAPI Framework**: Modern, fast web framework with automatic API documentation
- **PostgreSQL + PostGIS**: Robust database with geographic data support
- **Redis**: Caching and WebSocket broker
- **JWT Authentication**: Secure authentication with refresh token rotation
- **File Uploads**: MinIO integration for scalable object storage
- **Real-time Chat**: WebSocket-based messaging system
- **Background Tasks**: Celery integration for async processing
- **Payment Integration**: Easypaisa and JazzCash support
- **SMS/Email**: OTP verification and notifications
- **Geographic Search**: PostGIS-powered location-based queries
- **Rate Limiting**: API protection and abuse prevention
- **Monitoring**: Prometheus metrics and health checks

## 🏗️ Architecture

```
app/
├── api/                 # API endpoints and routers
│   └── v1/            # API version 1
├── core/               # Core configuration and utilities
├── models/             # SQLAlchemy database models
├── schemas/            # Pydantic request/response models
├── services/           # Business logic layer
├── tasks/              # Celery background tasks
├── utils/              # Utility functions
└── main.py             # Application entry point
```

## 🛠️ Tech Stack

- **Framework**: FastAPI 0.104.1
- **Database**: PostgreSQL 16 + PostGIS
- **ORM**: SQLAlchemy 2.0 + Alembic
- **Cache**: Redis 7
- **Task Queue**: Celery
- **Authentication**: JWT + Argon2
- **File Storage**: MinIO (S3 compatible)
- **Validation**: Pydantic v2
- **Testing**: pytest + pytest-asyncio
- **Code Quality**: Black, isort, Ruff

## 📋 Prerequisites

- Python 3.11+
- PostgreSQL 16+ with PostGIS extension
- Redis 7+
- MinIO (or S3-compatible storage)

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone <repository-url>
cd homlo/apps/api
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

```bash
cp env.example .env
# Edit .env with your configuration
```

### 5. Database Setup

```bash
# Create database
createdb homlo

# Run migrations
alembic upgrade head
```

### 6. Start the Application

```bash
# Development
uvicorn main:app --reload --port 8000

# Production
uvicorn main:app --host 0.0.0.0 --port 8000
```

## 🌍 Environment Variables

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/homlo

# JWT
JWT_SECRET_KEY=your-super-secret-jwt-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# Redis
REDIS_URL=redis://localhost:6379

# MinIO
MINIO_ROOT_USER=homlo
MINIO_ROOT_PASSWORD=homlo123
MINIO_ENDPOINT=localhost:9000
MINIO_BUCKET_NAME=homlo-assets

# SMS (Twilio)
SMS_PROVIDER=twilio
SMS_ACCOUNT_SID=your-account-sid
SMS_AUTH_TOKEN=your-auth-token
SMS_FROM_NUMBER=your-from-number

# Email
SMTP_HOST=localhost
SMTP_PORT=1025
SMTP_USERNAME=
SMTP_PASSWORD=
```

## 📚 API Documentation

Once the application is running, you can access:

- **Interactive API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

## 🗄️ Database Models

### Core Entities

- **Users**: Authentication, profiles, verification levels
- **Listings**: Properties with geographic data and amenities
- **Bookings**: Reservations with status tracking
- **Reviews**: Double-sided rating system
- **Messages**: Real-time chat functionality
- **Transactions**: Payment processing and tracking

### Key Features

- **Geographic Queries**: PostGIS integration for location-based search
- **Full-text Search**: PostgreSQL full-text search capabilities
- **Audit Logging**: Comprehensive change tracking
- **Soft Deletes**: Data preservation with logical deletion

## 🔐 Authentication & Security

### JWT Implementation

- **Access Tokens**: Short-lived (15 minutes) for API access
- **Refresh Tokens**: Long-lived (7 days) for token renewal
- **Token Rotation**: Automatic refresh token rotation
- **Blacklisting**: Redis-based token invalidation

### Security Features

- **Password Hashing**: Argon2 with high security parameters
- **Rate Limiting**: API endpoint protection
- **CORS Configuration**: Cross-origin request handling
- **Input Validation**: Pydantic-based request validation
- **SQL Injection Protection**: SQLAlchemy ORM usage

## 📁 File Management

### MinIO Integration

- **Pre-signed URLs**: Secure direct upload to storage
- **Image Processing**: Background task for thumbnail generation
- **File Validation**: MIME type and size restrictions
- **CDN Ready**: Public bucket configuration

### Supported Formats

- **Images**: JPEG, PNG, WebP
- **Documents**: PDF
- **Maximum Size**: 10MB per file

## 💬 Real-time Features

### WebSocket Implementation

- **Chat System**: Real-time messaging between users
- **Connection Management**: Redis-based connection tracking
- **Message Persistence**: Database storage with caching
- **Typing Indicators**: Real-time user activity

### Event Broadcasting

- **Booking Updates**: Real-time status changes
- **New Messages**: Instant chat notifications
- **System Alerts**: Platform-wide announcements

## 🔄 Background Tasks

### Celery Integration

- **Image Processing**: Thumbnail generation and optimization
- **Email Sending**: Asynchronous notification delivery
- **SMS Delivery**: OTP and alert messages
- **Data Cleanup**: Periodic maintenance tasks

### Task Scheduling

- **Periodic Tasks**: Automated cleanup and maintenance
- **Retry Logic**: Failed task handling with exponential backoff
- **Monitoring**: Task queue health and performance metrics

## 🧪 Testing

### Test Structure

```bash
tests/
├── unit/              # Unit tests
├── integration/       # Integration tests
├── fixtures/          # Test data and fixtures
└── conftest.py        # Test configuration
```

### Running Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=app --cov-report=html

# Specific test file
pytest tests/test_auth.py

# Watch mode
pytest --watch
```

### Test Database

Tests use a separate database to avoid affecting development data:

```bash
# Create test database
createdb homlo_test

# Set test environment
export DATABASE_TEST_URL=postgresql://user:password@localhost:5432/homlo_test
```

## 📊 Monitoring & Health

### Health Endpoints

- **Health Check**: `/healthz` - Basic service health
- **Ready Check**: `/readyz` - Service readiness (database, Redis)
- **Metrics**: `/metrics` - Prometheus metrics

### Metrics Collection

- **Request Count**: Total API requests by endpoint
- **Response Time**: Request latency distribution
- **Error Rates**: Failed request tracking
- **Resource Usage**: Database and Redis performance

## 🚀 Deployment

### Docker

```bash
# Build image
docker build -t homlo-api .

# Run container
docker run -p 8000:8000 homlo-api
```

### Production Considerations

- **Environment Variables**: Secure configuration management
- **Database Connection Pooling**: Optimized connection handling
- **Logging**: Structured logging with rotation
- **Monitoring**: Application performance monitoring
- **Backup**: Automated database backups
- **SSL/TLS**: HTTPS termination and certificate management

## 🔧 Development

### Code Quality

```bash
# Format code
black .
isort .

# Lint code
ruff check .
ruff format .

# Type checking
mypy .
```

### Pre-commit Hooks

```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

### Database Migrations

```bash
# Create migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

## 📖 API Endpoints

### Authentication

- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/refresh` - Token refresh
- `POST /api/v1/auth/logout` - User logout

### Users

- `GET /api/v1/users/me` - Current user profile
- `PUT /api/v1/users/me` - Update profile
- `GET /api/v1/users/{user_id}` - Get user profile

### Listings

- `GET /api/v1/listings` - Search listings
- `POST /api/v1/listings` - Create listing
- `GET /api/v1/listings/{listing_id}` - Get listing details
- `PUT /api/v1/listings/{listing_id}` - Update listing
- `DELETE /api/v1/listings/{listing_id}` - Delete listing

### Bookings

- `POST /api/v1/bookings` - Create booking
- `GET /api/v1/bookings` - User bookings
- `PUT /api/v1/bookings/{booking_id}` - Update booking
- `POST /api/v1/bookings/{booking_id}/cancel` - Cancel booking

### Chat

- `GET /api/v1/chat/threads` - Get chat threads
- `GET /api/v1/chat/threads/{thread_id}/messages` - Get messages
- `POST /api/v1/chat/threads/{thread_id}/messages` - Send message

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

### Development Guidelines

- Follow PEP 8 style guidelines
- Write comprehensive docstrings
- Include type hints for all functions
- Add tests for new features
- Update documentation as needed

## 📄 License

This project is proprietary software for commercial use.

## 🆘 Support

For technical support or questions:

- **Documentation**: Check the API docs at `/docs`
- **Issues**: Report bugs via GitHub Issues
- **Team**: Contact the development team

## 🔗 Related Links

- [Frontend Application](../web/README.md)
- [Project Documentation](../../README.md)
- [Docker Setup](../../docker-compose.yml)
- [API Documentation](http://localhost:8000/docs)
