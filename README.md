# Homlo - Pakistan-first Airbnb-style Marketplace

A peer-to-peer marketplace for renting apartments, houses, rooms, and commercial spaces in Pakistan, built with modern web technologies and Pakistan-specific features.

## 🚀 Features

- **User Authentication**: Secure JWT-based auth with phone OTP and CNIC verification
- **Property Listings**: Complete CRUD operations for hosts with Pakistan-specific amenities
- **Booking System**: Request, approve, and manage reservations with PKR pricing
- **Real-time Chat**: Integrated messaging using WebSockets
- **Review System**: Double-sided ratings and reviews
- **Search & Discovery**: Advanced filtering with map view and location-based search
- **Pakistan Market Focus**: PKR pricing, local cities, Easypaisa/JazzCash integration
- **Multi-language**: English and Urdu (RTL) support

## 🏗️ Tech Stack

- **Frontend**: Next.js 14 (App Router), TypeScript, TailwindCSS, shadcn/ui
- **Backend**: FastAPI (Python 3.11+), SQLAlchemy 2.0, PostgreSQL 16 + PostGIS
- **Database**: PostgreSQL with PostGIS for geo queries
- **Real-time**: FastAPI WebSockets with Redis broker
- **Authentication**: JWT with refresh rotation, Argon2 password hashing
- **File Storage**: MinIO (S3 compatible) for images and documents
- **Payments**: Easypaisa, JazzCash, manual cash, bank transfer
- **Search**: PostGIS for geo queries and full-text search
- **i18n**: Next-intl for English/Urdu support

## 📁 Project Structure

```
homlo/
├── apps/
│   ├── web/           # Next.js frontend application
│   └── api/           # FastAPI backend server
├── packages/
│   ├── ui/            # Shared UI components
│   └── config/        # Shared configuration
├── infra/             # Docker, nginx, provisioning scripts
├── docker-compose.yml # Complete containerization
└── README.md          # This file
```

## 🐳 Quick Start with Docker

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd homlo
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   cp apps/api/.env.example apps/api/.env
   cp apps/web/.env.example apps/web/.env
   # Edit the .env files with your configuration
   ```

3. **Start all services**
   ```bash
   docker compose up -d
   ```

4. **Seed the database**
   ```bash
   make seed
   ```

5. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs
   - Mailhog (dev): http://localhost:8025
   - MinIO Console: http://localhost:9001

## 🔧 Manual Setup

### Prerequisites
- Node.js 20+
- Python 3.11+
- PostgreSQL 16+ with PostGIS
- Redis 7+
- MinIO

### Backend Setup
```bash
cd apps/api
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your configuration
uvicorn main:app --reload --port 8000
```

### Frontend Setup
```bash
cd apps/web
npm install
cp .env.example .env
# Edit .env with your configuration
npm run dev
```

## 🌍 Environment Variables

### Root (.env)
```env
# Database
POSTGRES_DB=homlo
POSTGRES_USER=homlo_user
POSTGRES_PASSWORD=homlo_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Redis
REDIS_URL=redis://localhost:6379

# MinIO
MINIO_ROOT_USER=homlo
MINIO_ROOT_PASSWORD=homlo123
MINIO_BUCKET_NAME=homlo-assets
```

### Backend (apps/api/.env)
```env
# Database
DATABASE_URL=postgresql://homlo_user:homlo_password@localhost:5432/homlo

# JWT
JWT_SECRET_KEY=your-super-secret-jwt-key-change-this-in-production
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

# SMS (for OTP)
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

### Frontend (apps/web/.env)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
NEXT_PUBLIC_MINIO_ENDPOINT=http://localhost:9000
NEXT_PUBLIC_MINIO_BUCKET=homlo-assets
```

## 📱 User Roles

- **Guest**: Browse listings, make bookings, chat with hosts, leave reviews
- **Host**: Create listings, manage bookings, respond to inquiries, receive payments
- **Admin**: Moderate content, manage disputes, approve payouts, system administration

## 🔐 Security Features

- JWT-based authentication with refresh rotation
- Argon2 password hashing
- CNIC verification for hosts (masked input)
- Phone number verification via OTP
- Input validation and sanitization
- CSRF protection and CORS configuration
- Rate limiting on sensitive endpoints

## 🚀 Deployment

The application is containerized and ready for production deployment. The `docker-compose.yml` file includes:

- Production-ready Next.js build
- FastAPI backend with Uvicorn
- PostgreSQL database with PostGIS
- Redis for caching and WebSocket broker
- MinIO for object storage
- Nginx reverse proxy (optional)

## 📄 License

This project is proprietary software for commercial use.

## 🤝 Contributing

This is a commercial project. Please contact the development team for contribution guidelines.
