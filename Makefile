.PHONY: help install db-up db-down db-restart db-logs db-shell run clean reset migrate-schema migrate-data migrate-all run-queries migrate-reset migrate-verify

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install Python dependencies
	pip install -r requirements.txt

db-up: ## Start PostgreSQL container
	docker-compose up -d
	@echo "Waiting for PostgreSQL to be ready..."
	@sleep 3
	@docker-compose ps

db-down: ## Stop PostgreSQL container
	docker-compose down

db-restart: ## Restart PostgreSQL container
	docker-compose restart
	@echo "Waiting for PostgreSQL to be ready..."
	@sleep 3

db-logs: ## Show PostgreSQL container logs
	docker-compose logs -f postgres

db-shell: ## Connect to PostgreSQL shell
	docker exec -it trabalho_postgres psql -U trabalho_user -d trabalho_db

db-reset: ## Stop container and remove all data (DESTRUCTIVE)
	docker-compose down -v
	@echo "All database data has been removed!"

migrate-schema: db-up ## Create database schema from migrations/esquema.sql
	@echo "Creating database schema..."
	@docker exec -i trabalho_postgres psql -U trabalho_user -d trabalho_db < migrations/esquema.sql
	@echo "✓ Schema created successfully!"

migrate-data: ## Populate initial data from migrations/dados.sql
	@echo "Populating initial data..."
	@docker exec -i trabalho_postgres psql -U trabalho_user -d trabalho_db < migrations/dados.sql
	@echo "✓ Data populated successfully!"

migrate-all: migrate-schema migrate-data ## Run complete migration (schema + data)
	@echo ""
	@echo "✓ Migration complete! Database ready."
	@echo ""

run-queries: ## Execute sample queries from migrations/consultas.sql
	@echo "Running sample queries..."
	@echo ""
	@docker exec -i trabalho_postgres psql -U trabalho_user -d trabalho_db < migrations/consultas.sql

migrate-reset: db-reset db-up migrate-all ## Full database rebuild (DESTRUCTIVE)
	@echo ""
	@echo "✓ Database completely rebuilt!"
	@echo ""

run: ## Run the application (starts DB if not running)
	@docker-compose ps | grep -q trabalho_postgres || make db-up
	python3 trabalho.py

clean: ## Remove Python cache files
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true

setup: install db-up ## Complete setup (install deps + start database)
	@echo ""
	@echo "Setup complete! Run 'make run' to start the application."

status: ## Show status of PostgreSQL container
	@docker-compose ps
