#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SQL_FILE="$SCRIPT_DIR/seed.sql"

if [ -f "../../.env" ]; then
    export $(grep -v '^#' ../../.env | xargs)
fi

POSTGRES_USER=${POSTGRES_USER:-postgres}
POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-postgres}
POSTGRES_SERVER=${POSTGRES_SERVER:-localhost}
POSTGRES_DB=${POSTGRES_DB:-db}

export PGPASSWORD=$POSTGRES_PASSWORD

psql -h $POSTGRES_SERVER -U $POSTGRES_USER -d $POSTGRES_DB -f $SQL_FILE

echo "Database seeded successfully"
