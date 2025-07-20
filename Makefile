# Makefile for Portfolio Analyzer Multi-Agent System
VENV_NAME = venv
PYTHON = $(VENV_NAME)/bin/python
PIP = $(VENV_NAME)/bin/pip
REQUIREMENTS = requirements.txt

# Colors for output
GREEN = \033[0;32m
YELLOW = \033[1;33m
RED = \033[0;31m
NC = \033[0m # No Color

.PHONY: help setup install clean test run dev-setup

help: ## Show this help message
	@echo "Portfolio Analyzer Multi-Agent System"
	@echo "======================================"
	@echo "Available commands:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  $(GREEN)%-15s$(NC) %s\n", $$1, $$2}' $(MAKEFILE_LIST)

setup: ## Create virtual environment and install dependencies
	@echo "$(YELLOW)Creating virtual environment...$(NC)"
	python3 -m venv $(VENV_NAME)
	@echo "$(YELLOW)Installing dependencies...$(NC)"
	$(PIP) install --upgrade pip
	$(PIP) install -r $(REQUIREMENTS)
	@echo "$(GREEN)Setup complete! Run 'make activate' to activate the virtual environment.$(NC)"

activate: ## Instructions to activate virtual environment
	@echo "$(YELLOW)To activate the virtual environment, run:$(NC)"
	@echo "source $(VENV_NAME)/bin/activate"

install: ## Install/update dependencies
	$(PIP) install -r $(REQUIREMENTS)
	@echo "$(GREEN)Dependencies installed successfully!$(NC)"

dev-setup: setup ## Complete development setup including environment file
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "$(YELLOW)Created .env file from template. Please update it with your credentials.$(NC)"; \
	fi
	@mkdir -p reports
	@echo "$(GREEN)Development environment ready!$(NC)"

test-connection: ## Test Kite API connection
	$(PYTHON) -c "from kite_api.connector import test_connection; test_connection()"

run: ## Run the portfolio analyzer
	$(PYTHON) main.py

clean: ## Remove virtual environment and cache files
	@echo "$(YELLOW)Cleaning up...$(NC)"
	rm -rf $(VENV_NAME)
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -name "*.pyc" -delete
	@echo "$(GREEN)Cleanup complete!$(NC)"

install-system-deps: ## Install system dependencies (Ubuntu/Debian)
	sudo apt-get update
	sudo apt-get install -y python3 python3-venv python3-pip

freeze: ## Generate requirements.txt from current environment
	$(PIP) freeze > $(REQUIREMENTS)
	@echo "$(GREEN)Requirements frozen to $(REQUIREMENTS)$(NC)"

lint: ## Run code linting
	$(PIP) install flake8 black
	$(PYTHON) -m flake8 . --max-line-length=88 --exclude=venv
	$(PYTHON) -m black --check .

format: ## Format code with black
	$(PIP) install black
	$(PYTHON) -m black .

check-env: ## Check if all required environment variables are set
	$(PYTHON) -c "from config.settings import check_config; check_config()"
