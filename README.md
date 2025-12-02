# Sistema de Relatos Cívicos

Console-based CRUD application for a civic reporting and benefit points system using PostgreSQL.

## Quick Start

```bash
# Complete setup
make setup

# Run application
make run
```

## Requirements

- Docker and Docker Compose
- Python 3.7+
- Make (optional)

## Available Commands

```bash
make help          # Show all commands
make setup         # First time setup
make run           # Run the application

# Database
make db-up         # Start PostgreSQL
make db-down       # Stop PostgreSQL
make db-shell      # Connect to database
make db-logs       # View logs
make db-reset      # Delete all data (destructive)
```

## Database Credentials

**Hardcoded in the application:**
- Database: `trabalho_db`
- User: `trabalho_user`
- Password: `trabalho_pass`
- Host: `localhost`
- Port: `5432`

## Project Structure

```
.
├── trabalho.py          # Main application
├── docker-compose.yml   # PostgreSQL container config
├── Makefile            # Development commands
├── requirements.txt    # Python dependencies
├── CLAUDE.md          # Detailed documentation
└── README.md          # This file
```

## Documentation

- **[CLAUDE.md](CLAUDE.md)** - Detailed architecture and development documentation
- **[DOCKER.md](DOCKER.md)** - Complete Docker container configuration and troubleshooting
