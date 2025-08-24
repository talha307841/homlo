-- Initialize PostgreSQL database for Homlo
-- This script runs when the PostgreSQL container starts for the first time

-- Enable PostGIS extension for geographic data
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS postgis_topology;

-- Create additional extensions for full-text search and other features
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Set timezone to Asia/Karachi
SET timezone = 'Asia/Karachi';

-- Create custom types
CREATE TYPE user_role AS ENUM ('guest', 'host', 'admin');
CREATE TYPE listing_type AS ENUM ('entire_home', 'private_room', 'shared_room', 'guest_house', 'farmhouse', 'studio', 'office', 'co_living', 'event_space');
CREATE TYPE booking_status AS ENUM ('pending', 'confirmed', 'cancelled', 'completed', 'rejected');
CREATE TYPE payment_status AS ENUM ('pending', 'processing', 'completed', 'failed', 'refunded');
CREATE TYPE payment_provider AS ENUM ('easypaisa', 'jazzcash', 'manual_cash', 'bank_transfer');
CREATE TYPE review_status AS ENUM ('pending', 'approved', 'rejected');
CREATE TYPE payout_status AS ENUM ('pending', 'processing', 'completed', 'failed');
CREATE TYPE verification_level AS ENUM ('none', 'email', 'phone', 'cnic');

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_phone ON users(phone);
CREATE INDEX IF NOT EXISTS idx_listings_location ON listings USING GIST(geog);
CREATE INDEX IF NOT EXISTS idx_listings_city ON listings(city);
CREATE INDEX IF NOT EXISTS idx_listings_type ON listings(type);
CREATE INDEX IF NOT EXISTS idx_bookings_dates ON bookings(check_in, check_out);
CREATE INDEX IF NOT EXISTS idx_bookings_status ON bookings(status);
CREATE INDEX IF NOT EXISTS idx_messages_thread_id ON messages(thread_id);
CREATE INDEX IF NOT EXISTS idx_reviews_listing_id ON reviews(listing_id);

-- Create functions for common operations
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create function to calculate distance between two points
CREATE OR REPLACE FUNCTION calculate_distance(
    lat1 double precision,
    lon1 double precision,
    lat2 double precision,
    lon2 double precision
)
RETURNS double precision AS $$
BEGIN
    RETURN ST_Distance(
        ST_SetSRID(ST_MakePoint(lon1, lat1), 4326)::geography,
        ST_SetSRID(ST_MakePoint(lon2, lat2), 4326)::geography
    );
END;
$$ LANGUAGE plpgsql;

-- Create function to check if dates overlap
CREATE OR REPLACE FUNCTION check_date_overlap(
    check_in1 date,
    check_out1 date,
    check_in2 date,
    check_out2 date
)
RETURNS boolean AS $$
BEGIN
    RETURN check_in1 < check_out2 AND check_in2 < check_out1;
END;
$$ LANGUAGE plpgsql;

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE homlo TO homlo_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO homlo_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO homlo_user;

-- Set default privileges for future objects
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO homlo_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO homlo_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON FUNCTIONS TO homlo_user;

-- Log successful initialization
DO $$
BEGIN
    RAISE NOTICE 'PostgreSQL database initialized successfully with PostGIS and custom functions';
END $$;
