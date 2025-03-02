#!/usr/bin/env bash
set -o errexit

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Generate Prisma client
prisma generate --schema=prisma/schema.prisma

# Apply database migrations
prisma migrate deploy --schema=prisma/schema.prisma