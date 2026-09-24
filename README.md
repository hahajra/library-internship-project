# Library Internship Project

This repository contains the ongoing internship work for the Library Management project, including Week 3, Week 4 and Week 5 development.

The project now includes a relational SQL Server database, Entity Framework Core integration, database-backed CRUD operations, Angular HTTP integration, JWT authentication, role-based authorization, protected frontend routes, a FastAPI AI service, local embeddings, Chroma vector search and a Retrieval-Augmented Generation (RAG) pipeline.

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
│   ├── requirements.txt
│   ├── embedding_demo.py
│   ├── chroma_demo.py
│   ├── persistent_chroma_demo.py
│   ├── manual_rag_demo.py
│   ├── build_library_index.py
│   └── library_books.json
│
├── .github
│   ├── workflows
│   └── PULL_REQUEST_TEMPLATE.md
│
├── .gitignore
└── README.md
```

---

# Week 3 - Database and Angular Integration

## Database

- Created a relational SQL Server database
- Added tables and relationships for the Library Management system
- Integrated Entity Framework Core
- Configured database connection with ASP.NET Core
- Added database-backed CRUD operations

## Backend

- Added repository and service layers
- Connected API operations with SQL Server
- Added CRUD endpoints for books
- Added support for authors and categories
- Added initial user login foundation

## Angular

- Connected Angular frontend with ASP.NET Core API
- Added HTTP-based book operations
- Added book listing
- Added add book functionality
- Added edit and update functionality
- Added delete functionality
- Added basic UI integration with backend data

## AI Script

- Added a basic AI-powered book summary script
- Added Python requirements file
- Added initial AI experimentation for the Library project

---

# Week 4 - Authentication, Authorization and AI Integration

## Backend Authentication

- Implemented JWT-based authentication
- Added role-based authorization
- Added protected book operations
- Configured JWT authentication in ASP.NET Core
- Added Swagger Bearer token authentication support

## Angular Authentication

- Added login and logout functionality
- Added AuthService for JWT token management
- Added HTTP interceptor for Bearer tokens
- Added authentication route guard
- Protected library routes
- Added role detection for Admin users
- Integrated authentication with the existing Library Management UI

## Angular Library Operations

- Verified authenticated book loading
- Added authenticated Add Book functionality
- Added authenticated Edit and Update functionality
- Added authenticated Delete functionality
- Added Admin-based delete handling
- Added JWT token persistence
- Verified protected routes after application restart

## FastAPI AI Service

- Added a separate FastAPI AI service
- Added `/health` endpoint
- Added `/summarize` endpoint
- Integrated OpenRouter using the `openrouter/free` model
- Added structured JSON response parsing
- Added malformed LLM response handling
- Added `/test-malformed-response` endpoint
- Added `/genre` endpoint for book genre suggestions
- Added environment-variable support for API keys
- Added `.gitignore` protection for `.env` and `.venv`
- Added Python dependency requirements

## AI Features

- Summarizes input text using an LLM
- Returns structured JSON output
- Returns summary and key points
- Handles malformed LLM responses safely
- Suggests genres based on book title and description
- Uses the OpenRouter free model route for testing

## Security

- API key is stored in `.env`
- `.env` is ignored by Git
- Python virtual environment is ignored by Git
- JWT authentication protects backend operations
- Bearer tokens are attached through Angular HTTP interceptor

## Git and Collaboration

- Used feature branches for Week 4 development
- Created and merged pull requests
- Practiced resolving a Git merge conflict
- Added a reusable pull request template
- Used security and testing checklists in pull requests
- Verified branch-based development workflow
- Maintained a clean `main` branch after merging

---

# Week 5 - Embeddings, Vector Search and RAG

## Embeddings

- Added local sentence embeddings using `sentence-transformers`
- Used the `all-MiniLM-L6-v2` embedding model
- Generated 384-dimensional vectors
- Verified embedding generation successfully

## Chroma Vector Database

- Added Chroma vector database integration
- Added semantic search demo
- Added persistent Chroma storage
- Stored and retrieved embedded library documents
- Ignored generated Chroma database folders in Git

## RAG Pipeline

- Built a manual Retrieval-Augmented Generation pipeline
- Retrieved relevant documents using vector similarity
- Sent retrieved context to the OpenRouter LLM
- Grounded answers using retrieved library information
- Prevented unsupported book information from being invented

## Real Library Integration

- Added real library book indexing
- Created `library_books.json`
- Added `build_library_index.py`
- Created persistent real library vector index
- Indexed title, author and category information

## FastAPI RAG Endpoint

- Added `/ask` endpoint
- Accepts natural-language questions
- Retrieves relevant library context
- Sends retrieved context to the LLM
- Returns grounded answers
- Returns source documents with each answer
- Uses the `openrouter/free` model

## Week 5 Testing

- Embedding generation tested successfully
- Chroma semantic search tested successfully
- Persistent vector database tested successfully
- Manual RAG tested successfully
- Real library indexing tested successfully
- `/ask` endpoint tested successfully
- Source attribution verified

---

# Main Technologies

## Backend

- ASP.NET Core
- C#
- Entity Framework Core
- SQL Server
- JWT Authentication
- Swagger

## Frontend

- Angular
- TypeScript
- Angular HttpClient
- Route Guards
- HTTP Interceptors

## AI Service

- Python
- FastAPI
- OpenRouter
- httpx
- python-dotenv
- Pydantic
- sentence-transformers
- ChromaDB

## Embedding Model

```text
all-MiniLM-L6-v2
```

The model generates:

```text
384-dimensional embeddings
```

## Version Control

- Git
- GitHub
- Feature branches
- Pull requests
- Merge conflict resolution
- Git tags

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

- Summary
- Key points
- Model name

## Genre Suggestion

```text
POST /genre
```

Accepts:

- Book title
- Book description

Returns:

- Suggested genre

## Ask Library

```text
POST /ask
```

Accepts a natural-language question about the indexed library books.

Example:

```json
{
  "question": "Do you have a book about web development?"
}
```

The endpoint:

- Converts the question into an embedding
- Searches the Chroma vector database
- Retrieves relevant library information
- Sends the retrieved context to the LLM
- Returns a grounded answer
- Returns the retrieved source documents

## Malformed Response Test

```text
GET /test-malformed-response
```

Used to test error handling when an LLM returns invalid JSON.

---

# Embedding Demo

Run:

```cmd
python embedding_demo.py
```

This generates vector embeddings using:

```text
all-MiniLM-L6-v2
```

---

# Chroma Semantic Search Demo

Run:

```cmd
python chroma_demo.py
```

This:

- Creates embeddings
- Stores documents in Chroma
- Performs semantic similarity search
- Returns the closest matching documents

---

# Persistent Chroma Demo

Run:

```cmd
python persistent_chroma_demo.py
```

This stores the Chroma vector database persistently so it can be reused between runs.

---

# Manual RAG Demo

Run:

```cmd
python manual_rag_demo.py
```

The manual RAG flow is:

```text
User Question
      ↓
Create Query Embedding
      ↓
Search Chroma
      ↓
Retrieve Relevant Context
      ↓
Send Context + Question to LLM
      ↓
Grounded Answer
```

---

# Building the Real Library Index

The real library book data is stored in:

```text
library_books.json
```

To build the vector index, run:

```cmd
python build_library_index.py
```

The script:

- Reads library book data
- Creates document text from title, author and category
- Generates embeddings
- Stores them in a persistent Chroma collection

The generated vector database folders are ignored by Git.

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

# Security Notes

The following should never be committed:

```text
.env
.venv
API keys
Generated Chroma databases
```

The AI service `.gitignore` protects these files and folders.

---

# Week 4 Status

Week 4 includes:

- JWT authentication
- Role-based authorization
- Angular login/logout
- Angular AuthService
- HTTP interceptor
- Route guard
- Protected routes
- Admin role handling
- Authenticated CRUD
- FastAPI AI service
- OpenRouter integration
- Summarization
- Structured JSON responses
- Malformed response handling
- Genre suggestion
- Git merge conflict practice
- Pull request workflow
- Pull request template

Week 4 development is complete.

---

# Week 5 Status

Week 5 includes:

- Local sentence embeddings
- `all-MiniLM-L6-v2`
- 384-dimensional vectors
- ChromaDB integration
- Semantic search
- Persistent vector storage
- Manual RAG
- Real library indexing
- Grounded LLM answers
- `/ask` FastAPI endpoint
- Source attribution
- Generated vector database Git ignore rules
- Feature branch and pull request workflow

Week 5 development is complete.