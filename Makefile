.PHONY: help install db-up db-down db-restart db-logs db-shell run clean reset

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
