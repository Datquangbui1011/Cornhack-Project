#!/usr/bin/env bash
set -o errexit

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Fetch Linux binaries (Render uses Ubuntu)
prisma py fetch --platform linux --engine-version 5.17.0

# Generate Prisma client
prisma generate --schema=prisma/schema.prisma

# Apply database migrations
prisma migrate deploy --schema=prisma/schema.prisma