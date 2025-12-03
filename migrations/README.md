# Database Migrations

SQL migration files for Sistema de Relatos Cívicos (Civic Reporting System).

## Overview

This directory contains all database schema, initial data, and sample queries for the civic reporting system. The migration system ensures repeatable, version-controlled database setup.

## Files

### esquema.sql
Complete database schema with 11 interconnected tables organized into functional domains:

**Core User System:**
- `Usuario` - Base user table (CPF, name, email, birth date, role)
- `Funcionario` - Municipal employees (sector, city)
- `Cidadao` - Citizens (points balance)

**Reporting System:**
- `CategoriaReport` - Report categories (defines point values)
- `Report` - Civic issue reports (title, location, status, description)
- `Midia` - Media attachments (photos, videos)
- `HistoricoAtualizado` - Audit trail of employee updates

**Interaction System:**
- `Interacao` - Base interactions on reports
- `Comentario` - User comments
- `Avaliacao` - User ratings (1-5 stars)

**Benefits System:**
- `Beneficios` - Available rewards catalog
- `CidadaoBeneficio` - Citizen benefit redemptions

**Features:**
- Primary/Foreign key constraints for referential integrity
- CHECK constraints for data validation (CPF format, role values, status values, rating range)
- Performance indexes on foreign keys and common filter columns
- Cascade delete rules for dependent data
- Brazilian CPF format validation (XXX.XXX.XXX-XX)

### dados.sql
Initial data population with 30+ records (exceeds minimum of 22 required).

**Data Scenarios Demonstrated:**
1. **Complete Report Lifecycle:** Citizen Maria reports pothole → Employee João updates status → Resolved → Citizen evaluation
2. **Points System:** Citizens accumulate points from reports, different balances demonstrated
3. **Benefit Redemption:** Citizens redeem benefits (transport discounts), points deducted
4. **Multiple Employees:** Different sectors (Infrastructure, Public Health) in different cities
5. **Citizen Engagement:** Comments and ratings on reports
6. **Audit Trail:** Historical record of all employee updates to reports

**Record Counts:**
- Usuario: 4 (2 citizens, 2 employees)
- Cidadao: 2
- Funcionario: 2
- CategoriaReport: 3
- Beneficios: 2
- Report: 3 (various statuses)
- Midia: 3
- HistoricoAtualizado: 3
- Interacao: 3
- Comentario: 2
- Avaliacao: 1
- CidadaoBeneficio: 2

### consultas.sql
5 complex business queries demonstrating advanced SQL techniques:

**Query 1: Citizen Ranking by Engagement** (Medium Complexity)
- Techniques: INNER JOIN, GROUP BY, HAVING, ORDER BY
- Purpose: Identify most active civic contributors
- Business Value: Recognize and reward engaged citizens

**Query 2: Employee Workload Analysis** (High Complexity)
- Techniques: LEFT OUTER JOIN, complex aggregations, CASE, NULLIF
- Purpose: Evaluate employee efficiency and workload distribution
- Business Value: Resource allocation and capacity planning

**Query 3: Unused Benefits** (Medium Complexity)
- Techniques: NOT IN subquery (non-correlated)
- Purpose: Identify benefits never redeemed
- Business Value: Review and optimize benefits catalog

**Query 4: High-Engagement Reports** (High Complexity)
- Techniques: Correlated subquery, nested non-correlated subquery
- Purpose: Find reports with above-average citizen interaction
- Business Value: Identify issues requiring priority attention

**Query 5: Category Performance Analysis** (High Complexity)
- Techniques: LEFT OUTER JOIN, multiple aggregations, temporal calculations
- Purpose: Analyze resolution efficiency by report category
- Business Value: Identify problematic categories and process bottlenecks

**Academic Requirements Fulfilled:**
- ✅ Inner joins (Queries 1, 2)
- ✅ Outer joins (LEFT OUTER JOIN in Queries 2, 5)
- ✅ GROUP BY + HAVING (Queries 1, 2, 5)
- ✅ Correlated subqueries (Query 4)
- ✅ Non-correlated subqueries (Queries 3, 4)
- ✅ All queries optimized with proper indexes

## Quick Start

```bash
# Complete database setup (fresh install)
make migrate-all

# Individual migration steps
make migrate-schema     # Create schema only
make migrate-data       # Populate data only (requires schema)
make run-queries        # Execute sample queries

# Reset everything and rebuild
make migrate-reset

# Verify migration success
make migrate-verify
```

## Execution Order

**IMPORTANT:** Always execute in this order to respect foreign key dependencies:

1. `esquema.sql` - Creates all tables with constraints
2. `dados.sql` - Populates data in correct dependency order
3. `consultas.sql` - Executes queries (read-only, can run anytime after data)

The `make migrate-all` command handles this automatically.

## Troubleshooting

### Error: relation "usuario" does not exist
**Solution:** Run schema migration first:
```bash
make migrate-schema
```

### Error: insert or update on table violates foreign key constraint
**Solution:** Data insertion order is wrong. Use the complete migration:
```bash
make migrate-reset
make migrate-all
```

### Error: could not connect to server
**Solution:** Start PostgreSQL:
```bash
make db-up
```

### Want to start fresh
**Solution:** Complete rebuild:
```bash
make migrate-reset
```

## Integration with Python Application

The Python application (`trabalho.py`) validates database state on startup:

- Checks if tables exist
- Checks if data is populated
- Provides helpful error messages with correct commands

**Before running the application:**
```bash
make migrate-all  # Ensure database is ready
make run          # Start application
```

## Academic Compliance

This migration system fulfills all academic requirements:

✅ **Requirement 1:** Complete schema (esquema.sql) with all 11 entities, constraints, and indexes
✅ **Requirement 2:** Initial data (dados.sql) with minimum 2 tuples per table (30+ total)
✅ **Requirement 3:** 5+ complex queries (consultas.sql) with diverse SQL features
✅ **Documentation:** All files thoroughly commented with purpose and complexity notes
✅ **Efficiency:** Queries optimized with strategic indexes defined in schema

## Validation Commands

```bash
# Count all records
make migrate-verify

# Check specific table
make db-shell
\d usuario              # Show table structure
SELECT COUNT(*) FROM usuario;  # Count records
\q                      # Exit
```

## File Sizes

- esquema.sql: ~260 lines (11 tables + indexes + documentation)
- dados.sql: ~150 lines (30+ records + scenarios)
- consultas.sql: ~180 lines (5 queries + documentation)

## Version History

- v1.0 (2024-12-02): Initial migration system with complete schema, data, and queries
