#!/bin/sh

# Wait for the Postgres service to be ready
echo "⏳ Waiting for PostgreSQL to be available at $DATABASE_URL..."

until pg_isready -h db -p 5432 -U user; do
  sleep 1
done

echo "✅ PostgreSQL is up - starting Flask app"
exec python run.py
