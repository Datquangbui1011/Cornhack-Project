#!/usr/bin/env bash
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Fetch Prisma binaries for Linux (Render uses Ubuntu)
prisma py fetch --machine linux --engine-version 5.17.0

# Generate the Prisma client
prisma generate --schema=prisma/schema.prisma

# Apply database migrations (optional)
prisma migrate deploy --schema=prisma/schema.prisma