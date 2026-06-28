# PES Assistant - Retirement Planning AI Assistant

A sophisticated multi-agent system for providing personalized retirement planning advice using semantic caching, conversation memory, intelligent document retrieval, and OAuth-secured external API integration.

## ✨ Latest Features (v2.0)

- ✅ **Execution Timer Decorator** - Auto-track function performance with `@execution_timer`
- ✅ **OAuth Token Management** - Secure API calls with automatic token caching
- ✅ **API Integration Framework** - Ready-to-use API helpers with error handling
- ✅ **Agent Fail-Safety** - Request timeouts, iteration limits, loop detection
- ✅ **Tool Response Validation** - Prevents bad responses from causing infinite loops
- ✅ **Conversation History Tracking** - Cached responses now logged in history

## 🏗️ Architecture Overview

### Agent Structure
```
ChatService (Orchestrator)
├── OrchestratorAgent
│   ├── DataAgent (Plan-specific data retrieval) [API-backed]
│   └── DocumentAgent (Document-based Q&A) [API-backed]
├── ConversationMemoryService (Context management)
├── SemanticCacheService (Response caching)
└── SessionManager (Session lifecycle)
```

### Key Components

#### 1. **Agents** (`app/agents/`)
- **BaseAgent**: Foundation class with timeout protection, error handling, and execution timing
- **OrchestratorAgent**: Routes user questions, detects infinite loops, tracks execution time
- **DataAgent**: Retrieves retirement plan data via external API with @execution_timer
- **DocumentAgent**: Searches and summarizes plan documents via external API
- **ConversationSummaryAgent**: Maintains conversation context with graceful error fallback

#### 2. **Services** (`app/services/`)
- **ChatService**: Main entry point with cached response logging
- **SemanticCacheService**: Detects similar questions, returns cached responses instantly
- **ConversationMemoryService**: Generates summaries every 10 messages
- **SessionManager**: Manages user sessions with complete conversation history
- **ResponseCacheService**: In-memory TTL-based response cache

#### 3. **Gateway** (`app/gateway/`)
- **AIGateway**: Request validation, error handling, retry logic (max 2 attempts)
- **APIHelper**: OAuth token manager, external API calls with header support
- **OAuthTokenManager**: Automatic token retrieval, caching, and refresh
- **PromptGuard**: Protects against prompt injection attacks
- **RequestValidator**: Validates chat requests
- **RetryPolicy**: Exponential backoff retry mechanism

#### 4. **LLM & Embeddings** (`app/llm/`)
- **ProviderFactory**: Creates LLM providers (Ollama, Bedrock, OpenAI)
- **EmbeddingProviderFactory**: Creates embedding providers for semantic caching
- **SemanticCache**: Stores question-response pairs with embeddings (Qdrant backend)

#### 5. **Vector Database** (`app/qdrant/`)
- **QdrantClientFactory**: Manages Qdrant vector DB connections
- **QdrantSemanticCacheRepository**: Stores and retrieves cached responses
- **QdrantCollectionManager**: Manages collections for embeddings

#### 6. **Utils** (`app/utils/`)
- **ExecutionTimer**: Decorator for auto-tracking function execution time
- **api_helper**: OAuth and external API integration utilities

## 📊 Data Flow

```
User Message
    ↓
[ChatService.chat()]
    ↓
[Check SemanticCache] → Hit? → Return cached response ✅
    ↓ Miss
[Add to conversation]
    ↓
[OrchestratorAgent.invoke()]
    ├→ [DataAgent] → GetPlanDataTool → Returns structured plan data
    └→ [DocumentAgent] → SearchDocumentsTool → Returns relevant documents
    ↓
[Combine responses] → LLM generates final answer
    ↓
[Update SemanticCache] → Store embedding + response
    ↓
[Update conversation history]
    ↓
[If messages >= 10] → [Generate summary]
    ↓
[Save session state]
    ↓
[Return response]
```

## 🔄 Semantic Caching Flow

**Similarity Detection:**
- Question converted to embedding (vector representation)
- Vector searched in Qdrant database
- Similarity threshold: 0.95 (95% match)
- If match found → Return cached response instantly

**Benefits:**
- Eliminates duplicate LLM calls
- Reduces API costs
- Improves response latency
- Handles paraphrased questions

## 💾 Conversation Memory

**Triggered At:** Every 10 messages

**Process:**
1. ConversationSummaryAgent analyzes conversation
2. Preserves:
   - Participant goals
   - Important plan details
   - Decisions made
   - Outstanding questions
3. Creates concise summary for context window

## ✅ Fail-Safety & Robustness Enhancements (Implemented)

### Timeout Protection
| Feature | Status | Details |
|---------|--------|---------|
| Request-level timeouts | ✅ DONE | 30s default (configurable) |
| Agent execution timeouts | ✅ DONE | Per-agent timeout in BaseAgent |
| Tool execution timeouts | ✅ DONE | 15s default for tool calls |
| Graceful timeout handling | ✅ DONE | AgentTimeoutException raised |

### Error Handling & Validation
| Feature | Status | Details |
|---------|--------|---------|
| BaseAgent error handling | ✅ DONE | Try/catch in _execute methods |
| Tool response validation | ✅ DONE | Empty response detection |
| Graceful fallbacks | ✅ DONE | ConversationSummaryAgent uses previous summary |
| Exception propagation | ✅ DONE | Proper error messages logged |

### Loop Prevention
| Feature | Status | Details |
|---------|--------|---------|
| Loop detection logging | ✅ DONE | Tracks repeated agent calls |
| Detection threshold | ✅ DONE | Warns after 4+ repeated calls |
| Manual iteration limits | ⚠️ CONFIG | Set max_iterations in LLM agent config |

### API Integration
| Feature | Status | Details |
|---------|--------|---------|
| OAuth token management | ✅ DONE | Automatic token retrieval & caching |
| API helpers | ✅ DONE | `call_external_api()` with error handling |
| Header-based auth | ✅ DONE | plan_number, user_id in headers |
| Scope-based OAuth | ✅ DONE | Sends only scope in token request |

## 🔧 New Utilities

### Execution Timer Decorator
```python
from app.utils.execution_timer import execution_timer

@execution_timer
async def my_function():
    # Auto-logs execution time
    pass

# Logs:
# [TIMER] Starting execution: my_function
# [TIMER] Completed: my_function (Duration: 0.1234s)
```

### OAuth & API Calls
```python
from app.gateway.api_helper import call_external_api

response = await call_external_api(
    http_client,
    endpoint="https://api.pes.com/eligibility",
    method="GET",
    headers={"plan_number": "12345", "user_id": "user123"}
    # OAuth token auto-injected if OAUTH_ENABLED=true
)
```

## 🚀 Setup & Deployment

### Prerequisites
- Python 3.9+
- Docker & Docker Compose
- Qdrant vector database
- LLM Provider (Ollama, Bedrock, or OpenAI)
- External PES API endpoint (optional - for production data)

### Quick Start
```bash
# 1. Install dependencies
pip install -r requirement.txt

# 2. Configure environment
cp .env.example .env
# Edit .env with your settings:
# - LLM provider configuration
# - OAuth settings (if using external APIs)
# - API endpoints
# - Agent timeouts

# 3. Start services
docker-compose up -d

# 4. Run application
python app/main.py
```

### Configuration Guide

#### For Development (No External APIs)
```bash
# .env
OAUTH_ENABLED=false
EXTERNAL_API_PES_BASE_URL=  # Leave empty - will use mock data
```

#### For Production (With OAuth)
```bash
# .env
OAUTH_ENABLED=true
OAUTH_TOKEN_URL=https://your-auth-server.com/token
OAUTH_SCOPE=apiscope
EXTERNAL_API_PES_BASE_URL=https://api.pes.com
EXTERNAL_API_DOCUMENTS_BASE_URL=https://api.documents.com

# Agent settings
AGENT_TIMEOUT_SECONDS=30
ENABLE_LOOP_DETECTION=true
```

### Key Configuration Options
```python
# LLM Settings
llm_provider = "ollama"  # or "bedrock", "openai"
model_name = "llama3.2"
temperature = 0.2

# Cache Settings
semantic_cache_similarity_threshold = 0.95
response_cache_ttl_minutes = 30

# Retry Settings
retry_max_attempts = 2
retry_initial_delay = 0.5
retry_backoff_multiplier = 2.0

# Session Settings
session_timeout_minutes = 30

# Agent Robustness
agent_timeout_seconds = 30
enable_loop_detection = true
loop_detection_threshold = 4

# OAuth & APIs
oauth_enabled = false
oauth_token_url = None
oauth_scope = None
external_api_pes_base_url = None
external_api_documents_base_url = None
```

## 📡 API Endpoints

### Chat Endpoints

#### Start Session
```bash
POST /api/chat/start
{
  "plan_num": "12345",
  "user_id": "user123"
}
```
Response:
```json
{
  "session_id": "sess_xxx",
  "correlation_id": "corr_xxx",
  "message": "Session started successfully"
}
```

#### Chat
```bash
POST /api/chat
{
  "session_id": "sess_xxx",
  "message": "What's my retirement age?"
}
```
Response:
```json
{
  "session_id": "sess_xxx",
  "response": "Based on your plan, your retirement age is 65..."
}
```

#### End Session
```bash
POST /api/chat/end
{
  "session_id": "sess_xxx"
}
```

#### Health Check
```bash
GET /api/health
```

### External PES API Endpoints

The system calls these endpoints to fetch retirement plan data:

```
GET  /information          Headers: plan_number
GET  /eligibility          Headers: plan_number, user_id
GET  /payroll              Headers: plan_number, user_id
GET  /contribution         Headers: plan_number, user_id
GET  /investment           Headers: plan_number, user_id
GET  /vesting              Headers: plan_number, user_id
GET  /loans                Headers: plan_number, user_id
GET  /withdrawals          Headers: plan_number, user_id
GET  /services             Headers: plan_number, user_id
GET  /adp-features         Headers: plan_number
```

### External Document API Endpoint

```

```

## 📈 Monitoring & Logging

### Log Levels
- **Log Level**: Configured in `app/config/logging.py`
- **Logs Location**: `logs/pes-assistant.log`

### Key Metrics Tracked
- Request latency
- Cache hit rate
- Agent execution time (via @execution_timer)
- Error counts by type
- OAuth token retrieval time
- External API call duration

### Execution Timer Output
All functions decorated with `@execution_timer` output timing information:
```
[TIMER] Starting execution: data_agent.get_eligibility
[TIMER] Completed: data_agent.get_eligibility (Duration: 0.2345s)
```

This helps identify performance bottlenecks:
- Functions taking >5s indicate potential LLM latency
- Functions taking >10s indicate external API delays
- Functions taking >15s trigger tool timeout

### View Logs
```bash
# View real-time logs
tail -f logs/pes-assistant.log

# Filter timer logs only
grep "\[TIMER\]" logs/pes-assistant.log

# Filter by agent
grep "agent\|Agent" logs/pes-assistant.log

# Filter errors
grep "ERROR\|Exception" logs/pes-assistant.log
```

### Performance Optimization Tips
1. If agent execution slow (>5s):
   - Check LLM provider latency
   - Verify network connectivity
   - Monitor external API response times

2. If cache hit rate low (<80%):
   - Questions may be too specific
   - Reduce semantic_cache_similarity_threshold to 0.85
   - Increase RESPONSE_CACHE_TTL_MINUTES

3. If tool calls timeout (>15s):
   - Increase TOOL_TIMEOUT_SECONDS
   - Optimize external API endpoints
   - Add caching at external API layer

## 🔐 OAuth & API Integration

### Overview
The PES Assistant supports OAuth 2.0 for secure API calls to external services. OAuth is **optional** and can be toggled via the `OAUTH_ENABLED` setting.

### OAuth Flow

1. **Token Request** (Scope-Only Body):
   ```
   POST /token HTTP/1.1
   Host: auth-server.com
   Content-Type: application/json
   
   {"scope": "read write"}
   ```

2. **Token Response**:
   ```json
   {
     "access_token": "eyJhbGciOiJIUzI1NiIs...",
     "token_type": "Bearer",
     "expires_in": 3600
   }
   ```

3. **API Call with Token**:
   ```
   GET /eligibility HTTP/1.1
   Host: api.pes.com
   Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
   plan_number: 12345
   user_id: user123
   ```

### Configuration

#### Minimal (No OAuth)
```bash
OAUTH_ENABLED=false
```

#### Full (With OAuth)
```bash
OAUTH_ENABLED=true
OAUTH_TOKEN_URL=https://auth-server.com/oauth/token
OAUTH_SCOPE=read write
EXTERNAL_API_PES_BASE_URL=https://api.pes.com
EXTERNAL_API_DOCUMENTS_BASE_URL=https://api.documents.com
```

### Parameter Passing Strategy

**Headers** (for dynamic parameters):
```python
headers={
    "plan_number": "12345",
    "user_id": "user_john"
}
```

**OAuth Body** (scope-only):
```python
json={"scope": "read write"}
```

### Usage Example

```python
from app.gateway.api_helper import call_external_api

# Automatic OAuth token injection (if OAUTH_ENABLED=true)
response = await call_external_api(
    http_client,
    endpoint="https://api.pes.com/eligibility",
    method="GET",
    headers={"plan_number": "12345", "user_id": "user123"}
)
```

### Token Caching

- Tokens are cached in memory during application runtime
- Automatic refresh when token expires
- No persistent storage (single-server deployment)
- Consider Redis for distributed deployments

### See Also
- [OAuth & API Setup Guide](OAUTH_API_SETUP.md) - Comprehensive guide
- [OAuth & API Quick Reference](OAUTH_API_QUICK_REFERENCE.md) - Quick checklist

## 🔐 Security

1. **Prompt Injection Guard**: Validates user input for malicious patterns
2. **Session Validation**: All requests validated for active sessions
3. **OAuth Token Security**: Tokens never logged or exposed in responses
4. **Request Rate Limiting**: (Can be added via APIGateway)
5. **Error Sanitization**: Internal errors not exposed to client
6. **HTTPS Only**: All OAuth and API calls should use HTTPS in production

## 🐛 Troubleshooting

### Agent Timeout
```
Error: Agent execution timeout after 30 seconds
Action: Increase agent_timeout_seconds in .env or check LLM performance
Example: AGENT_TIMEOUT_SECONDS=60
```

### Infinite Loop Detected
```
Warning: Possible infinite loop detected: 'data_agent_tool' called 5 times
Action: Check agent logs for repeated tool calls
Fix: Set ENABLE_LOOP_DETECTION=false to disable warnings (not recommended)
```

### OAuth Token Request Failed
```
Error: OAuth token request failed
Causes:
1. OAUTH_TOKEN_URL not configured correctly
2. OAuth server is down
3. OAUTH_SCOPE is invalid

Action:
1. Verify OAUTH_TOKEN_URL is accessible
2. Check OAuth server status
3. Validate OAUTH_SCOPE format
4. Set OAUTH_ENABLED=false to skip OAuth
```

### API Endpoint Not Reachable
```
Error: external_api_pes_base_url not configured
Action: Set EXTERNAL_API_PES_BASE_URL in .env with your API endpoint
Example: EXTERNAL_API_PES_BASE_URL=https://api.pes.com
```

### Cache Miss Rate High
```
Action: Lower semantic_cache_similarity_threshold from 0.95 to 0.85
Note: This will catch more similar questions but may reduce precision
Example: SEMANTIC_CACHE_SIMILARITY_THRESHOLD=0.85
```

### Tool Response Empty or Invalid
```
Warning: Tool returned empty data for query
Action: Check if external API is returning valid data
Fix: Validate API response format in DocumentRepository/PESRepository
```

### Out of Memory
```
Action: Reduce response_cache_ttl_minutes or clear Qdrant collections
Command: python -m app.qdrant.qdrant_initializer --clear
Alternative: Increase server memory or reduce RESPONSE_CACHE_TTL_MINUTES
```