#!/bin/bash

set -e  # Exit on error

case "$1" in
    start)
        echo "🐘 Starting PostgreSQL development database..."
        docker-compose -f docker-compose.dev.yml up -d postgres
        echo "⏳ Waiting for database to be ready..."
        timeout 30 bash -c 'until docker-compose -f docker-compose.dev.yml exec postgres pg_isready -U hammer_dev_user -d hammer_dev; do sleep 1; done'
        echo "✅ Database is ready!"
        ;;
    stop)
        echo "🛑 Stopping development database..."
        docker-compose -f docker-compose.dev.yml down
        ;;
    reset)
        echo "🔄 Resetting development database (this will delete all data)..."
        read -p "Are you sure? [y/N] " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            docker-compose -f docker-compose.dev.yml down -v
            docker-compose -f docker-compose.dev.yml up -d postgres
            echo "⏳ Waiting for database to be ready..."
            timeout 30 bash -c 'until docker-compose -f docker-compose.dev.yml exec postgres pg_isready -U hammer_dev_user -d hammer_dev; do sleep 1; done'
            echo "✅ Database reset complete!"
        fi
        ;;
    status)
        docker-compose -f docker-compose.dev.yml ps postgres
        ;;
    logs)
        docker-compose -f docker-compose.dev.yml logs -f postgres
        ;;
    shell)
        echo "🐘 Connecting to PostgreSQL shell..."
        docker-compose -f docker-compose.dev.yml exec postgres psql -U hammer_dev_user -d hammer_dev
        ;;
    *)
        echo "Usage: $0 {start|stop|reset|status|logs|shell}"
        echo ""
        echo "Commands:"
        echo "  start  - Start the development database"
        echo "  stop   - Stop the development database"
        echo "  reset  - Reset database (deletes all data)"
        echo "  status - Show database container status"
        echo "  logs   - Show database logs"
        echo "  shell  - Connect to PostgreSQL shell"
        exit 1
        ;;
esac