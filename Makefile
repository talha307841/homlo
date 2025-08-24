.PHONY: help dev build up down logs seed test clean install

# Default target
help:
	@echo "Homlo - Pakistan-first Airbnb-style Marketplace"
	@echo ""
	@echo "Available commands:"
	@echo "  make dev          - Start development environment"
	@echo "  make build        - Build all Docker images"
	@echo "  make up           - Start all services"
	@echo "  make down         - Stop all services"
	@echo "  make logs         - Show logs for all services"
	@echo "  make seed         - Seed the database with sample data"
	@echo "  make test         - Run tests for both frontend and backend"
	@echo "  make clean        - Clean up Docker containers and volumes"
	@echo "  make install      - Install dependencies for local development"
	@echo "  make migrate      - Run database migrations"
	@echo "  make shell-api    - Open shell in API container"
	@echo "  make shell-web    - Open shell in web container"
	@echo "  make shell-db     - Open shell in database container"

# Development environment
dev:
	@echo "Starting development environment..."
	docker compose --profile dev up -d
	@echo "Development environment started!"
	@echo "Frontend: http://localhost:3000"
	@echo "Backend API: http://localhost:8000"
	@echo "API Docs: http://localhost:8000/docs"
	@echo "Mailhog: http://localhost:8025"
	@echo "MinIO Console: http://localhost:9001"

# Build all images
build:
	@echo "Building Docker images..."
	docker compose build --no-cache
	@echo "Build complete!"

# Start all services
up:
	@echo "Starting all services..."
	docker compose up -d
	@echo "All services started!"

# Stop all services
down:
	@echo "Stopping all services..."
	docker compose down
	@echo "All services stopped!"

# Show logs
logs:
	docker compose logs -f

# Seed database
seed:
	@echo "Seeding database..."
	docker compose exec api python scripts/seed.py
	@echo "Database seeded successfully!"

# Run tests
test:
	@echo "Running tests..."
	@echo "Backend tests..."
	docker compose exec api python -m pytest
	@echo "Frontend tests..."
	docker compose exec web npm test
	@echo "Tests completed!"

# Clean up
clean:
	@echo "Cleaning up Docker resources..."
	docker compose down -v --remove-orphans
	docker system prune -f
	@echo "Cleanup completed!"

# Install dependencies for local development
install:
	@echo "Installing dependencies..."
	@echo "Backend dependencies..."
	cd apps/api && pip install -r requirements.txt
	@echo "Frontend dependencies..."
	cd apps/web && npm install
	@echo "Dependencies installed!"

# Run database migrations
migrate:
	@echo "Running database migrations..."
	docker compose exec api alembic upgrade head
	@echo "Migrations completed!"

# Open shell in API container
shell-api:
	docker compose exec api bash

# Open shell in web container
shell-web:
	docker compose exec web bash

# Open shell in database container
shell-db:
	docker compose exec postgres psql -U homlo_user -d homlo

# Production deployment
prod:
	@echo "Starting production environment..."
	docker compose --profile production up -d
	@echo "Production environment started!"

# Health check
health:
	@echo "Checking service health..."
	@echo "API Health:"
	curl -f http://localhost:8000/healthz || echo "API is down"
	@echo "Web Health:"
	curl -f http://localhost:3000 || echo "Web is down"
	@echo "Database Health:"
	docker compose exec postgres pg_isready -U homlo_user || echo "Database is down"
	@echo "Redis Health:"
	docker compose exec redis redis-cli ping || echo "Redis is down"
	@echo "MinIO Health:"
	curl -f http://localhost:9000/minio/health/live || echo "MinIO is down"

# Backup database
backup:
	@echo "Creating database backup..."
	docker compose exec postgres pg_dump -U homlo_user homlo > backup_$(shell date +%Y%m%d_%H%M%S).sql
	@echo "Backup created!"

# Restore database
restore:
	@echo "Restoring database from backup..."
	@read -p "Enter backup file name: " backup_file; \
	docker compose exec -T postgres psql -U homlo_user -d homlo < $$backup_file
	@echo "Database restored!"
