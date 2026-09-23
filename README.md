# Library Internship Project

This repository contains the ongoing internship work for the Library Management project, including Week 3 and Week 4 development.

The project now includes a relational SQL Server database, Entity Framework Core integration, database-backed CRUD operations, Angular HTTP integration, JWT authentication, role-based authorization, protected frontend routes, and a FastAPI AI service with summarization and genre suggestion endpoints.

---

# Project Structure

```text
library-internship-project
│
├── backend
│   └── WebApplication2
│
├── frontend
│   └── week2-library-angular
│
├── sql
│   └── week3-relational-schema.sql
│
├── docs
│   └── week3-auth-notes.md
│
├── ai-scripts
│   ├── book_summary.py
│   └── requirements.txt
│
├── ai-service
│   ├── .gitignore
│   ├── main.py
│   └── requirements.txt
│
├── .github
│   ├── workflows
│   └── PULL_REQUEST_TEMPLATE.md
│
├── .gitignore
└── README.md
````

---

# Week 3 - Database and Angular Integration

## Database

* Created a relational SQL Server database
* Added tables and relationships for the Library Management system
* Integrated Entity Framework Core
* Configured database connection with ASP.NET Core
* Added database-backed CRUD operations

## Backend

* Added repository and service layers
* Connected API operations with SQL Server
* Added CRUD endpoints for books
* Added support for authors and categories
* Added initial user login foundation

## Angular

* Connected Angular frontend with ASP.NET Core API
* Added HTTP-based book operations
* Added book listing
* Added add book functionality
* Added edit and update functionality
* Added delete functionality
* Added basic UI integration with backend data

## AI Script

* Added a basic AI-powered book summary script
* Added Python requirements file
* Added initial AI experimentation for the Library project

---

# Week 4 - Authentication, Authorization and AI Integration

## Backend Authentication

* Implemented JWT-based authentication
* Added role-based authorization
* Added protected book operations
* Configured JWT authentication in ASP.NET Core
* Added Swagger Bearer token authentication support

## Angular Authentication

* Added login and logout functionality
* Added AuthService for JWT token management
* Added HTTP interceptor for Bearer tokens
* Added authentication route guard
* Protected library routes
* Added role detection for Admin users
* Integrated authentication with the existing Library Management UI

## Angular Library Operations

* Verified authenticated book loading
* Added authenticated Add Book functionality
* Added authenticated Edit and Update functionality
* Added authenticated Delete functionality
* Added Admin-based delete handling
* Added JWT token persistence
* Verified protected routes after application restart

## FastAPI AI Service

* Added a separate FastAPI AI service
* Added `/health` endpoint
* Added `/summarize` endpoint
* Integrated OpenRouter using the `openrouter/free` model
* Added structured JSON response parsing
* Added malformed LLM response handling
* Added `/test-malformed-response` endpoint
* Added `/genre` endpoint for book genre suggestions
* Added environment-variable support for API keys
* Added `.gitignore` protection for `.env` and `.venv`
* Added Python dependency requirements

## AI Features

* Summarizes input text using an LLM
* Returns structured JSON output
* Returns summary and key points
* Handles malformed LLM responses safely
* Suggests genres based on book title and description
* Uses the OpenRouter free model route for testing

## Security

* API key is stored in `.env`
* `.env` is ignored by Git
* Python virtual environment is ignored by Git
* JWT authentication protects backend operations
* Bearer tokens are attached through Angular HTTP interceptor

## Git and Collaboration

* Used feature branches for Week 4 development
* Created and merged pull requests
* Practiced resolving a Git merge conflict
* Added a reusable pull request template
* Used security and testing checklists in pull requests
* Verified branch-based development workflow
* Maintained a clean `main` branch after merging

---

# Main Technologies

## Backend

* ASP.NET Core
* C#
* Entity Framework Core
* SQL Server
* JWT Authentication
* Swagger

## Frontend

* Angular
* TypeScript
* Angular HttpClient
* Route Guards
* HTTP Interceptors

## AI Service

* Python
* FastAPI
* OpenRouter
* httpx
* python-dotenv
* Pydantic

## Version Control

* Git
* GitHub
* Feature branches
* Pull requests
* Merge conflict resolution
* Git tags

---

# Running the Backend

Navigate to the backend project directory and run:

```cmd
dotnet run
```

The backend currently runs on:

```text
https://localhost:7038
```

Swagger can be opened at:

```text
https://localhost:7038/swagger
```

---

# Running the Angular Frontend

Navigate to:

```text
frontend\week2-library-angular
```

Then run:

```cmd
npm install
ng serve
```

Open:

```text
http://localhost:4200
```

---

# Running the FastAPI AI Service

Navigate to:

```text
ai-service
```

Activate the virtual environment:

```cmd
.venv\Scripts\activate
```

Run:

```cmd
python -m uvicorn main:app --reload
```

Open Swagger:

```text
http://127.0.0.1:8000/docs
```

---

# FastAPI Endpoints

## Health Check

```text
GET /health
```

Checks whether the AI service is running.

## Summarization

```text
POST /summarize
```

Accepts text and returns:

* Summary
* Key points
* Model name

## Genre Suggestion

```text
POST /genre
```

Accepts:

* Book title
* Book description

Returns:

* Suggested genre

## Malformed Response Test

```text
GET /test-malformed-response
```

Used to test error handling when an LLM returns invalid JSON.

---

# Environment Variables

Create an `.env` file inside:

```text
ai-service
```

Add:

```text
OPENROUTER_API_KEY=your_api_key_here
```

The `.env` file must not be committed to Git.

---

# Week 4 Status

Week 4 includes:

* JWT authentication
* Role-based authorization
* Angular login/logout
* Angular AuthService
* HTTP interceptor
* Route guard
* Protected routes
* Admin role handling
* Authenticated CRUD
* FastAPI AI service
* OpenRouter integration
* Summarization
* Structured JSON responses
* Malformed response handling
* Genre suggestion
* Git merge conflict practice
* Pull request workflow
* Pull request template

Week 4 development is complete.

```
```