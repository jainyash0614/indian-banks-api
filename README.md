# Indian Banks REST API

A FastAPI service exposing REST endpoints over Indian bank and branch data, built with modern Python practices and comprehensive testing.

## Assignment Solution Overview

### Problem Analysis
The assignment required creating a REST API service that could:
1. Serve bank and branch data from a provided CSV dataset
2. Provide endpoints to list banks and get branch details
3. Support filtering and search capabilities
4. Demonstrate clean code practices and comprehensive testing

### Solution Architecture

**Technology Stack:**
- **Framework**: FastAPI (modern, fast, auto-documentation)
- **Database**: SQLite (local development) + PostgreSQL (production)
- **ORM**: SQLAlchemy 2.0 with async-ready patterns
- **Validation**: Pydantic v2 for request/response schemas
- **Testing**: pytest with async HTTP client testing
- **Deployment**: Heroku-ready with Procfile

**Data Flow:**
1. **CSV Ingestion**: One-time import of `bank_branches.csv` into normalized database tables
2. **Database Design**: Two main tables (`banks`, `branches`) with proper foreign key relationships
3. **API Layer**: RESTful endpoints with query parameter filtering
4. **Response Serialization**: Pydantic models ensuring type safety and validation

**Key Design Decisions:**
- **Normalized Schema**: Separated banks and branches for efficient querying
- **Indexing Strategy**: Added indexes on frequently queried fields (bank_id, city, state)
- **Lazy Loading**: Bank details loaded on-demand for branch responses
- **Filter Support**: Query parameters for bank name search and branch filtering
- **Error Handling**: Proper HTTP status codes and descriptive error messages

### Implementation Details

**Database Models:**
- `Bank`: id (PK), name with branches relationship
- `Branch`: ifsc (PK), bank_id (FK), branch, address, city, district, state

**API Endpoints:**
- `GET /banks` - List all banks with optional name search
- `GET /branches/{ifsc}` - Get specific branch details including bank info
- `GET /banks/{bank_id}/branches` - List branches for a bank with filtering options

**Testing Strategy:**
- **Unit Tests**: Fast, isolated tests using in-memory SQLite
- **Integration Tests**: HTTP endpoint testing with httpx AsyncClient
- **Test Data**: Minimal seed data for consistent test results
- **Dependency Override**: Clean separation between test and production databases

### Code Quality Features

**Clean Code Practices:**
- Type hints throughout (Python 3.9+ compatible)
- Modular architecture with clear separation of concerns
- Consistent naming conventions and error handling
- Comprehensive docstrings and inline documentation

**Performance Optimizations:**
- Database indexes on query fields
- Efficient SQL queries with proper joins
- Connection pooling and session management
- Minimal memory footprint for large datasets

**Security & Reliability:**
- Input validation via Pydantic
- SQL injection protection via SQLAlchemy ORM
- Proper error handling and logging
- Health check endpoint for monitoring

## Setup

1. Create a virtualenv and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Run the server (auto-loads CSV into SQLite on first start):

```bash
uvicorn app.main:app --reload
```

- API: http://127.0.0.1:8000
- Docs: http://127.0.0.1:8000/docs

## REST Endpoints

- `GET /banks?q=<optional>`: List banks, optionally search by name
- `GET /branches/{ifsc}`: Get branch details by IFSC (includes bank)
- `GET /banks/{bank_id}/branches?branch=&city=&state=`: List branches for a bank with optional filters
- `GET /healthz`: Health check

## Tests

```bash
pytest -q
```

**Test Coverage:**
- Health check endpoint
- Bank listing with search
- Branch retrieval by IFSC
- Bank branches with filtering
- Error handling (404 cases)
- Schema validation
- Performance benchmarks

## Deploy (Heroku)

1. **Prepare for deployment:**
```bash
# Add Postgres driver
echo "psycopg2-binary==2.9.9" >> requirements.txt

# Initialize git and commit
git init
git add .
git commit -m "Initial commit for Heroku deployment"
```

2. **Create Heroku app:**
```bash
heroku create your-app-name
heroku buildpacks:add heroku/python
```

3. **Add PostgreSQL database:**
```bash
heroku addons:create heroku-postgresql:mini
```

4. **Load data into Heroku Postgres:**
```bash
heroku pg:psql < indian_banks/indian_banks.sql
```

5. **Configure environment:**
```bash
heroku config:set SKIP_STARTUP=1
```

6. **Deploy:**
```bash
git push heroku HEAD:main
heroku ps:scale web=1
```

7. **Verify deployment:**
```bash
heroku open
# Navigate to /docs for interactive API documentation
```

## Time Taken to Complete Assignment

**Total Development Time: 2.5 Days**

**Breakdown:**
- **Day 1**: Project setup, database design, basic API structure
- **Day 2**: CSV ingestion, endpoint implementation, testing framework
- **Day 3**: Testing, documentation, deployment preparation, final polish

**Key Milestones:**
- ✅ FastAPI application structure
- ✅ SQLAlchemy models and database schema
- ✅ CSV data ingestion pipeline
- ✅ REST API endpoints implementation
- ✅ Comprehensive test suite
- ✅ Heroku deployment configuration
- ✅ Documentation and README

**Technologies Learned/Applied:**
- FastAPI framework and modern Python patterns
- SQLAlchemy 2.0 with async patterns
- Pytest with async testing
- Heroku deployment and PostgreSQL integration
- Modern Python type hints and validation

## Future Enhancements

- **Pagination**: Add limit/offset for large result sets
- **Caching**: Redis integration for frequently accessed data
- **Authentication**: JWT-based API security
- **Rate Limiting**: API usage controls
- **Monitoring**: Prometheus metrics and health checks
- **CI/CD**: GitHub Actions for automated testing and deployment
