# Library Internship Project

This repository contains the ongoing internship work for the Library Management project, including Week 3, Week 4, Week 5 and Week 6 development.

The project includes a relational SQL Server database, Entity Framework Core integration, database-backed CRUD operations, Angular HTTP integration, JWT authentication, role-based authorization, protected frontend routes, a FastAPI AI service, local embeddings, Chroma vector search, Retrieval-Augmented Generation (RAG), LangChain LCEL pipelines, advanced retrieval, conversation memory, structured AI output, tool calling, resilient .NET-to-AI communication and end-to-end streamed AI responses.

---

# Project Structure

```text
library-internship-project
|
|-- backend
|   `-- WebApplication2
|
|-- frontend
|   `-- week2-library-angular
|
|-- sql
|   `-- week3-relational-schema.sql
|
|-- docs
|   `-- week3-auth-notes.md
|
|-- ai-scripts
|   |-- book_summary.py
|   `-- requirements.txt
|
|-- ai-service
|   |-- .gitignore
|   |-- main.py
|   |-- requirements.txt
|   |-- embedding_demo.py
|   |-- chroma_demo.py
|   |-- persistent_chroma_demo.py
|   |-- manual_rag_demo.py
|   |-- build_library_index.py
|   |-- library_books.json
|   |-- lcel_rag_demo.py
|   |-- advanced_retrieval_demo.py
|   |-- structured_memory_demo.py
|   |-- availability_tool_demo.py
|   `-- streaming_rag.py
|
|-- .github
|   |-- workflows
|   `-- PULL_REQUEST_TEMPLATE.md
|
|-- .gitignore
`-- README.md
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
- Added `AuthService` for JWT token management
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
- Integrated OpenRouter using the `openrouter/free` model route
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
- Uses the `openrouter/free` model route

## Week 5 Testing

- Embedding generation tested successfully
- Chroma semantic search tested successfully
- Persistent vector database tested successfully
- Manual RAG tested successfully
- Real library indexing tested successfully
- `/ask` endpoint tested successfully
- Source attribution verified

---

# Week 6 - LangChain, Tool Calling, Resilience and Streaming

Week 6 extends the existing RAG system with LangChain, improved retrieval, structured output, conversational memory, LLM tool calling, resilient service communication and real-time streamed responses.

## Part A - LangChain LCEL RAG Chain

- Rebuilt the RAG pipeline using LangChain Expression Language (LCEL)
- Used `RunnableLambda`
- Used `RunnablePassthrough`
- Used `ChatPromptTemplate`
- Connected the pipeline to OpenRouter
- Continued using local `all-MiniLM-L6-v2` embeddings
- Continued using the persistent real-library Chroma index
- Added a custom short-input guard
- Verified normal questions pass through the RAG chain
- Verified very short input is rejected before unnecessary LLM processing

Example short-input result:

```text
Question too short to answer meaningfully.
```

## Part B - Advanced Retrieval

- Added `RecursiveCharacterTextSplitter`
- Added configurable chunk size and chunk overlap
- Added LangChain-compatible local embedding support
- Added a Chroma retriever
- Added `MultiQueryRetriever`
- Compared normal single-query retrieval with multi-query retrieval
- Tested five different questions
- Observed that MultiQueryRetriever can improve recall by generating alternative query forms
- Also observed that broader retrieval can sometimes reduce precision by returning additional documents

## Part C - Structured Output and Conversation Memory

- Added Pydantic structured output
- Used LangChain `with_structured_output`
- Added `RunnableWithMessageHistory`
- Added `InMemoryChatMessageHistory`
- Added session-scoped conversational memory
- Verified follow-up questions work inside the same session
- Verified a fresh session does not reuse another session's context
- Added stricter prompting so vague references such as `it` are not guessed from unrelated library data
- Verified structured output successfully with the live model

Example same-session flow:

```text
User: Tell me about React Essentials
User: Who wrote it?

Answer: ali
```

Example fresh-session behavior:

```text
User: Who wrote it?

Answer:
I do not have enough conversation context to know which book you mean.
```

Structured output includes:

```text
answer
confidence
sources
```

### Memory Limitation

Conversation history is currently stored only in Python process memory.

This means:

- memory is available while the FastAPI/Python process is running
- different session IDs keep separate histories
- conversation history is lost when the Python process restarts
- a persistent database-backed chat-history store could be added in a future version

---

# Week 6 Tool Calling

## Book Availability Field

A new availability field was added to the `Book` entity:

```text
IsAvailable
```

An Entity Framework Core migration was created to update the database.

## Availability Endpoint

The backend exposes:

```text
GET /api/Books/{id}/availability
```

Example response:

```json
{
  "bookId": 2,
  "title": "React Essentials",
  "isAvailable": false
}
```

## LLM Availability Tool

A LangChain tool was created for checking book availability.

The tool:

- accepts a book ID
- calls the ASP.NET Core availability endpoint
- receives the current availability value
- returns the tool result to the LLM
- allows the LLM to create the final natural-language response

Testing verified:

```text
Availability question -> tool called
Genre question        -> tool not called
```

This ensures the availability API is only used when the user's question actually requires live availability information.

---

# Week 6 Resilient .NET AI Client

The ASP.NET Core backend now communicates with FastAPI through a typed AI service client.

## Added Components

```text
IAiServiceClient
AiServiceClient
AskDto
AiAskResponse
AssistantController
```

## Endpoint

```text
POST /api/Assistant/ask
```

The endpoint is protected using JWT authentication.

## IHttpClientFactory

The AI service client is registered using:

```text
IHttpClientFactory
```

The FastAPI base address is configured through:

```text
AiService:BaseUrl
```

## Retry Policy

Transient AI service failures use an exponential retry policy.

Configured retry delays:

```text
2 seconds
4 seconds
8 seconds
```

## Timeout

The normal AI service client uses a request timeout to prevent requests from hanging indefinitely.

## Circuit Breaker

Repeated FastAPI failures open a circuit breaker temporarily.

Testing confirmed behavior similar to:

```text
AI retry 1 after 2 seconds.
AI retry 2 after 4 seconds.
AI circuit opened for 30 seconds.
AI retry 3 after 8 seconds.
AI service circuit breaker is open.
```

## Graceful Failure

When the FastAPI service is unavailable, the ASP.NET Core application remains running and returns a graceful service-unavailable response instead of crashing.

This was tested by:

1. running the ASP.NET Core backend
2. stopping FastAPI
3. calling the AI endpoint
4. observing retries
5. observing the circuit breaker open
6. verifying graceful failure handling

---

# Week 6 End-to-End Streaming

Week 6 adds real-time AI answer streaming through all application layers.

The streaming flow is:

```text
Angular
   |
   | authenticated POST request
   v
ASP.NET Core
/api/assistant/ask/stream
   |
   | streaming proxy
   v
FastAPI
/ask/stream
   |
   | OpenRouter streaming request
   v
OpenRouter
   |
   | streamed tokens
   v
FastAPI
   |
   | SSE events
   v
ASP.NET Core
   |
   | flushed response chunks
   v
Angular
   |
   v
Live AI answer
```

## FastAPI Streaming

FastAPI exposes:

```text
POST /ask/stream
```

The endpoint:

- retrieves relevant library documents
- sends grounded context to OpenRouter
- enables model streaming
- receives streamed content
- returns Server-Sent Event style data
- sends token events
- sends source events
- sends a final completion event
- supports optional artificial delay for testing
- detects disconnected clients

Example streamed events:

```text
data: {"type": "token", "content": "The"}

data: {"type": "token", "content": " author of React Essentials"}

data: {"type": "token", "content": " is ali."}

data: {"type": "sources", "sources": ["Title: React Essentials. Author: ali. Category: Web Development."]}

data: {"type": "done", "completed": true}
```

## Direct Streaming Test

Streaming was tested directly with:

```cmd
curl.exe -N -X POST http://127.0.0.1:8000/ask/stream -H "Content-Type: application/json" -d "{\"question\":\"Who wrote React Essentials?\",\"delay_ms\":150}"
```

The response arrived progressively rather than as one complete response.

## ASP.NET Core Streaming Proxy

The .NET backend exposes:

```text
POST /api/assistant/ask/stream
```

The streaming proxy uses:

```text
HttpCompletionOption.ResponseHeadersRead
```

This prevents the backend from waiting for the entire FastAPI response before beginning to forward data.

A dedicated streaming `HttpClient` is used with an infinite client timeout while cancellation is handled using the request cancellation token.

## FlushAsync

The .NET streaming proxy uses:

```text
Response.Body.FlushAsync()
```

after streamed event boundaries.

This ensures buffered response data is pushed to the browser progressively.

Testing included:

1. streaming with `FlushAsync`
2. temporarily removing/commenting out `FlushAsync`
3. comparing buffering behavior
4. restoring `FlushAsync`
5. rebuilding the backend successfully

The final implementation keeps `FlushAsync` enabled.

## Angular Streaming UI

A new authenticated route was added:

```text
/assistant
```

The Angular AI Assistant:

- uses native `fetch()`
- attaches the JWT Bearer token
- reads `response.body` using a stream reader
- decodes incoming chunks with `TextDecoder`
- processes SSE-style event blocks
- displays tokens while they arrive
- displays sources after completion
- shows streaming status
- supports configurable artificial delay
- supports clearing the current conversation display

## Stream Cancellation

Angular uses:

```text
AbortController
```

to cancel an active streaming request.

Cancellation was tested successfully.

The UI displays:

```text
Streaming was cancelled.
```

when the user stops an active response.

## Artificial Delay Test

The stream supports artificial delay values such as:

```text
0 ms
100 ms
150 ms
300 ms
500 ms
```

A 500 ms delay was used to clearly verify that tokens were being delivered progressively through:

```text
OpenRouter
-> FastAPI
-> ASP.NET Core
-> Angular
```

---

# Week 6 Git Workflow

Week 6 development used separate feature branches:

```text
feature/langchain-rag-chain
feature/availability-tool
feature/resilient-ai-client
feature/streaming-chat-ui
```

Each feature was developed independently and merged through a pull request.

Merged Week 6 pull requests:

```text
PR #14 - LangChain RAG, advanced retrieval and memory
PR #15 - Availability tool calling
PR #16 - Resilient .NET AI service client
PR #17 - End-to-end AI streaming
```

## Interactive Rebase

Interactive rebase was practiced on an isolated branch.

Four small commits were created and then consolidated using:

```cmd
git rebase -i HEAD~4
```

The commits were squashed into:

```text
practice: demonstrate interactive rebase and squash
```

Because the branch had already been pushed before the rebase, the rewritten history was updated safely using:

```cmd
git push --force-with-lease
```

The temporary practice branch was deleted after the exercise.

The `main` branch was never rebased.

---

# Week 6 Testing Summary

The following Week 6 functionality was tested:

- LCEL RAG chain
- short-input guard
- recursive text splitting
- normal retriever
- MultiQueryRetriever
- same-session conversation memory
- fresh-session isolation
- structured Pydantic output
- live structured-output model response
- book availability API
- LLM tool selection
- tool result returned to the model
- genre question correctly avoiding the availability tool
- typed .NET AI client
- successful .NET-to-FastAPI request
- exponential retries
- request timeout configuration
- circuit breaker
- graceful AI service failure handling
- direct FastAPI streaming
- streamed source events
- .NET streaming proxy
- `ResponseHeadersRead`
- `FlushAsync`
- Angular live token rendering
- artificial streaming delay
- stream cancellation
- final .NET build
- final Angular build
- interactive rebase
- `--force-with-lease`

---

# Known Limitations

## In-Memory Conversation History

Conversation memory currently uses in-memory Python storage.

Restarting the Python AI service removes conversation history.

A future implementation could use:

- Redis
- SQL Server
- another persistent chat-history store

## Free LLM Routing

The project uses the OpenRouter free model route for development and testing.

Because free routing may select different underlying models, response wording and output quality can vary between requests.

The RAG, retrieval, streaming, service integration and source-attribution logic remain independent of that variation.

## Local Development URLs

The project currently uses local development addresses such as:

```text
http://127.0.0.1:8000
https://localhost:7038
http://localhost:4200
```

Production deployment would require environment-specific configuration.

---

# Main Technologies

## Backend

- ASP.NET Core
- C#
- .NET 8
- Entity Framework Core
- SQL Server
- JWT Authentication
- Swagger
- `IHttpClientFactory`
- Polly retry policies
- Circuit breaker
- HTTP response streaming

## Frontend

- Angular
- TypeScript
- Angular HttpClient
- Native Fetch API
- ReadableStream
- TextDecoder
- AbortController
- Route Guards
- HTTP Interceptors

## AI Service

- Python
- FastAPI
- OpenRouter
- LangChain
- LangChain LCEL
- `httpx`
- `python-dotenv`
- Pydantic
- `sentence-transformers`
- ChromaDB
- Server-Sent Event style streaming

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
- Interactive rebase
- Squash workflow
- `--force-with-lease`
- Merge conflict resolution
- Git tags

---

# Running the Backend

Navigate to:

```text
backend\WebApplication2\WebApplication2
```

Run:

```cmd
dotnet run
```

The backend development URL is:

```text
https://localhost:7038
```

Swagger:

```text
https://localhost:7038/swagger
```

---

# Running the Angular Frontend

Navigate to:

```text
frontend\week2-library-angular
```

Install dependencies if required:

```cmd
npm install
```

Run:

```cmd
npm start
```

Open:

```text
http://localhost:4200
```

After login, the AI Assistant is available at:

```text
http://localhost:4200/assistant
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

FastAPI documentation:

```text
http://127.0.0.1:8000/docs
```

---

# Important FastAPI Endpoints

## Health

```text
GET /health
```

## Summarization

```text
POST /summarize
```

## Genre Suggestion

```text
POST /genre
```

## Standard RAG Question

```text
POST /ask
```

Example:

```json
{
  "question": "Who wrote React Essentials?"
}
```

## Streaming RAG Question

```text
POST /ask/stream
```

Example:

```json
{
  "question": "Who wrote React Essentials?",
  "delay_ms": 150
}
```

## Malformed Response Test

```text
GET /test-malformed-response
```

---

# Important ASP.NET Core AI Endpoints

## Standard AI Proxy

```text
POST /api/Assistant/ask
```

Requires JWT authentication.

## Streaming AI Proxy

```text
POST /api/assistant/ask/stream
```

Requires JWT authentication.

## Book Availability

```text
GET /api/Books/{id}/availability
```

---

# Building the Real Library Index

The real library book data is stored in:

```text
library_books.json
```

Build the vector index with:

```cmd
python build_library_index.py
```

The script:

- reads library book data
- creates document text from title, author and category
- generates embeddings
- stores the embeddings in the persistent real-library Chroma collection

Generated vector database folders are ignored by Git.

---

# Environment Variables

Create:

```text
ai-service\.env
```

Add:

```text
OPENROUTER_API_KEY=your_api_key_here
```

The `.env` file must never be committed.

---

# Security Notes

The following should never be committed:

```text
.env
.venv
API keys
generated Chroma databases
JWT secrets
```

Authentication-sensitive values should be stored through environment variables, user secrets or development configuration rather than hard-coded into source control.

---

# Week 4 Status

Week 4 development is complete.

---

# Week 5 Status

Week 5 development is complete.

---

# Week 6 Status

Week 6 includes:

- LangChain LCEL RAG
- custom input guard
- recursive text splitting
- advanced retrieval
- MultiQueryRetriever
- structured output
- session-scoped conversation memory
- availability tool calling
- public book-availability API
- Entity Framework availability migration
- typed .NET AI client
- `IHttpClientFactory`
- exponential retry
- timeout handling
- circuit breaker
- graceful FastAPI failure handling
- FastAPI response streaming
- ASP.NET Core streaming proxy
- `ResponseHeadersRead`
- `FlushAsync`
- Angular AI Assistant
- native fetch streaming
- JWT-authenticated streaming requests
- live token rendering
- source display
- artificial delay testing
- stream cancellation
- interactive rebase
- squash workflow
- `--force-with-lease`
- feature branches
- reviewed pull-request workflow

Week 6 development is complete.