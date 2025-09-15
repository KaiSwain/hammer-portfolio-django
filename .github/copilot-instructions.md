# Copilot Instructions for Hammer Portfolio Django

## Project Overview
This is a student portfolio management system with Django REST API backend (`back/`) and Next.js frontend (`front/`). The system generates PDF certificates and AI-powered personality summaries for students in training programs.

## Core Architecture

### Backend Structure (`back/`)
- **Django App**: `hammer_backendapi` - main business logic
- **Models**: Student with foreign key relationships to lookup tables (GenderIdentity, DiscAssessment, etc.)
- **Views Structure**: Organized by feature (`students.py`, `certificates.py`, `ai_summary.py`, `health.py`)
- **Certificate Generation**: PDF generation using PyMuPDF with template at `static/Certificates_Master.pdf`
- **AI Integration**: OpenAI API for personality summaries (configured via `OPENAI_API_KEY`)
- **Authentication**: Token-based auth with Django REST Framework

### Frontend Structure (`front/`)
- **Next.js 15**: App router with feature-based organization in `src/app/`
- **API Service**: Centralized in `src/app/services/api.js` with token management pattern
- **Token Auth**: localStorage JSON object format: `{"token": "actual-token"}`

## Key Development Patterns

### Environment Configuration
- **Development**: Uses `.env.development` files in both `back/` and `front/`
- **Production**: Environment variables via hosting platform (Railway/DigitalOcean)
- **Settings Logic**: `back/hammer_backendproject/settings.py` auto-detects mode based on `DJANGO_DEBUG`
- **CORS**: Frontend URL configured via `NEXT_PUBLIC_API_URL` environment variable

### API Architecture Patterns
- **URL Structure**: `/api/` prefix for all API endpoints in `hammer_backendproject/urls.py`
- **ViewSets**: Use Django REST Framework ViewSets for CRUD operations (see `StudentViewSet`)
- **Authentication Header**: `Authorization: Token {token}` for authenticated requests
- **Serializer Depth**: Uses `depth=1` for nested foreign key objects in responses
- **Error Logging**: Centralized logging to `back/logs/django.log`

### Certificate Generation Workflow
- **Multiple Types**: Portfolio, NCCER, OSHA, HammerMath, Employability, Workforce
- **Template**: Single PDF template at `static/Certificates_Master.pdf` with coordinate-based text placement
- **API Pattern**: POST to `/api/generate/{type}/` with student data payload
- **Bulk Generation**: `/api/generate/all/` generates all certificate types
- **Data Flow**: Frontend → API → PDF generator → Base64 response

### Student Data Model
- **Core Model**: `hammer_backendapi/models/models.py` - Student with foreign keys to lookup tables
- **Lookup Tables**: GenderIdentity, DiscAssessment, SixteenTypeAssessment, EnneagramResult, etc.
- **Serializer Depth**: Uses `depth=1` in serializers for nested object data
- **Foreign Key Endpoints**: `/api/details/` provides dropdown options for form fields

## Essential Commands

### Development Setup
```bash
# Backend setup with dependencies
cd back && python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py populate_assessment_data  # Initialize lookup tables

# Frontend setup
cd front && npm install && npm run dev
```

### Production Deployment
```bash
./deploy.sh deploy  # Complete production deployment with backups
python manage.py setup_production --admin-email admin@domain.com --admin-password secure-pass
```

### Testing & Debugging
```bash
# Health checks (both load balancer and API endpoints)
curl http://localhost:8000/health/          # Load balancer health
curl http://localhost:8000/api/health/      # API health with database check

# Test specific functionality
python back/test_pdf_generation.py         # Test certificate generation
python back/test_ai_summary.py            # Test OpenAI integration
```

## Common Integration Points

### API Authentication
- **Frontend**: Token stored in localStorage as `{"token": "actual-token"}`
- **Backend**: `Authorization: Token {token}` header required for most endpoints
- **Login**: POST to `/api/login/` returns token object
- **API Service Pattern**: Use `getHeaders()` in `src/app/services/api.js` for consistent auth

### Student Management
- **CRUD**: Full REST API via `StudentViewSet` at `/api/students/`
- **Foreign Keys**: Use `/api/details/` to get dropdown options for forms
- **Validation**: Serializers handle nested object creation/updates
- **Data Structure**: Student objects include nested lookup table data via `depth=1`

### PDF Generation
- **Lazy Loading**: PDF generator imported only when needed to avoid startup issues
- **Error Handling**: All PDF errors logged to `back/logs/django.log` with stack traces
- **Template System**: Single master template with coordinate-based text placement
- **Response Format**: PDFs returned as base64 for frontend processing

## Docker & Production Notes

### Container Structure
- **Production**: `docker-compose.prod.yml` with PostgreSQL, Redis, Nginx
- **Development**: `docker-compose.yml` for local development
- **Health Checks**: All services have health check configurations

### Management Commands
- **setup_production**: Creates superuser and default data
- **populate_assessment_data**: Initializes lookup table data
- **Custom commands**: Located in `back/hammer_backendapi/management/commands/`

## File Structure Conventions
- **Static Files**: `back/static/` for PDF templates and CSS
- **Media Files**: `back/media/` for uploads
- **Logs**: `back/logs/django.log` for application logs
- **Migrations**: Auto-generated in `back/hammer_backendapi/migrations/`

## AI-Specific Features
- **OpenAI Integration**: Personality summaries via `views/ai_summary.py`
- **Template Rendering**: HTML templates in `back/templates/` for AI-generated content
- **Model Configuration**: Uses GPT-4o-mini by default (configurable via `OPENAI_MODEL`)

When modifying this codebase, always check the existing patterns in URLs (`urls.py`), serializers, and views before adding new functionality. The system uses consistent naming conventions and structured error handling throughout.