# DevOps Assistant - Architecture Walkthrough

**Purpose:** Technical walkthrough document for VP/Architect level presentation
**Duration:** 1 hour meeting
**Audience:** Architects, Vice Presidents, Technical Leadership
**Date Created:** February 2026

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [High-Level Architecture](#2-high-level-architecture)
3. [Request Flow - Step by Step](#3-request-flow---step-by-step)
4. [Base Agent vs Orchestrator](#4-base-agent-vs-orchestrator)
5. [Multi-Model Switching](#5-multi-model-switching)
6. [Conversation History & Caching](#6-conversation-history--caching)
7. [Memory Implementation](#7-memory-implementation)
8. [Security & Guardrails](#8-security--guardrails)
9. [TR API Standard Framework Usage](#9-tr-api-standard-framework-usage)
10. [Feature Implementation Status](#10-feature-implementation-status)
11. [Anticipated Technical Questions](#11-anticipated-technical-questions)
12. [Demo Scenarios](#12-demo-scenarios)

---

## 1. Executive Summary

### What is DevOps Assistant?

The DevOps Assistant is a **Software 3.0 application** - instead of traditional if/else logic, Claude AI acts as the reasoning engine that decides which tools to call based on natural language understanding.

**Key Stats:**
- **51 Python source files** organized in 11 modules
- **22 test files** covering unit, integration, and E2E scenarios
- **30 tools** across 3 specialized agents
- **Enterprise-grade security** with JWT, guardrails, and rate limiting

### The Problem It Solves

Today, when an issue occurs in production or QA:
- Engineers open Datadog to search logs
- Switch to APM for traces
- Check metrics dashboards
- Jump to kubectl or Lens for Kubernetes status
- Manually correlate timestamps across all sources

**DevOps Assistant eliminates this context-switching** by combining all capabilities into one natural language interface.

### Technology Stack

| Component | Technology |
|-----------|------------|
| LLM Engine | Claude Opus 4.5 via TR AI Platform |
| API Framework | FastAPI + Uvicorn (async) |
| Authentication | JWT (RS256/384/512) via TR SSO |
| Kubernetes | Official Python client (EKS) |
| Observability | Datadog API (Logs v2, Spans v2, Metrics v2) |
| Caching | TTLCache (in-memory) |
| Streaming | Server-Sent Events (SSE) |

---

## 2. High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           CLIENT LAYER                                  │
│     Audit DevOps Portal (React) │ Streamlit UI (Dev/Testing)            │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼ HTTP (JWT Bearer Token)
┌─────────────────────────────────────────────────────────────────────────┐
│                         API LAYER (FastAPI)                             │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌───────────┐ ┌─────────────┐   │
│  │   CORS   │ │Rate Limit│ │ Request  │ │JWT Auth   │ │ Guardrails  │   │
│  │  Check   │ │ 100/min  │ │ Logging  │ │RS256/384  │ │  (NeMo)     │   │
│  └──────────┘ └──────────┘ └──────────┘ └───────────┘ └─────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                       SESSION LAYER                                     │
│              SessionManager (TTLCache: 1hr, 1000 sessions)              │
│                    Maintains conversation state per user                 │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      ORCHESTRATOR AGENT                                 │
│                                                                         │
│   3-Level Routing Strategy:                                             │
│   1. Explicit @mentions (@datadog, @k8s, @cert) → Direct route          │
│   2. Weighted keyword scoring (Cert=2.0, DD=1.5, K8s=1.0) → Best match  │
│   3. Fallback → DatadogAgent (most common use case)                     │
└─────────────────────────────────────────────────────────────────────────┘
                    │                   │                   │
         ┌──────────┘                   │                   └──────────┐
         ▼                              ▼                              ▼
┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐
│  DATADOG AGENT  │         │    K8S AGENT    │         │   CERT AGENT    │
│   (19 tools)    │         │   (10 tools)    │         │   (1 tool)      │
│                 │         │                 │         │                 │
│ • Logs (4)      │         │ • get_pods      │         │ • check_cert_   │
│ • Traces (5)    │         │ • describe_pod  │         │   expiry        │
│ • Metrics (6)   │         │ • get_events    │         │                 │
│ • Correlation(4)│         │ • get_hpa       │         │                 │
└─────────────────┘         │ • rollout_status│         └─────────────────┘
         │                  │ • get_pvcs      │                  │
         │                  │ • search_res.   │                  │
         │                  └─────────────────┘                  │
         │                           │                           │
         └───────────────────────────┼───────────────────────────┘
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         BASE AGENT (Abstract)                           │
│                                                                         │
│   The Agentic Loop (max 10 iterations):                                 │
│   ┌─────────────────────────────────────────────────────────────────┐   │
│   │  1. Add user message to conversation history                    │   │
│   │  2. Prepare context (auto-truncate if >80% of 200K limit)       │   │
│   │  3. Call Claude API → Get response                              │   │
│   │  4. IF stop_reason == "end_turn" → Return text response         │   │
│   │  5. IF stop_reason == "tool_use" → Execute tools                │   │
│   │  6. Add tool results to conversation                            │   │
│   │  7. LOOP back to step 2 (until max 10 iterations)               │   │
│   └─────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
                                     │
                    ┌────────────────┼────────────────┐
                    ▼                ▼                ▼
            ┌───────────┐    ┌───────────┐    ┌───────────┐
            │TR AI      │    │Kubernetes │    │ Datadog   │
            │Platform   │    │ API (EKS) │    │ API       │
            │(Claude)   │    │           │    │           │
            └───────────┘    └───────────┘    └───────────┘
```

---

## 3. Request Flow - Step by Step

| Step | Component | Action | File Location |
|------|-----------|--------|---------------|
| 1 | Portal | User sends message with JWT token | Client-side |
| 2 | CORS | Validate origin (audit-devops-portal.*.thomsonreuters.com) | `api/main.py` |
| 3 | Rate Limiter | Check 100 req/min limit per user (employee_id) | `api/main.py` |
| 4 | JWT Auth | Validate RS256 signature, extract user context | `api/middleware/jwt_auth.py` |
| 5 | Input Guardrails | Check for prompt injection (52+ patterns), PII, blocked topics | `guardrails/guardrails_service.py` |
| 6 | SessionManager | Get/create session (TTLCache, 1hr expiry) | `api/services/chat_service.py` |
| 7 | Model Selector | Select model based on context size (Opus-first strategy) | `framework/model_selector.py` |
| 8 | Orchestrator | Route to appropriate agent via keyword scoring | `framework/orchestrator.py` |
| 9 | BaseAgent | Execute agentic loop with Claude (max 10 iterations) | `framework/base_agent.py` |
| 10 | Tool Executor | Execute K8s/Datadog API calls (with caching) | `tools/*.py`, `cache.py` |
| 11 | Output Guardrails | Mask sensitive data (passwords, tokens, SSN, cards) | `guardrails/guardrails_service.py` |
| 12 | Response | Return JSON with message + session_id | `api/routes/v1/chat.py` |

### Detailed Flow Diagram

```
User Query: "Show me error logs for pricing-service"
                    │
                    ▼
┌─────────────────────────────────────────────────────────────┐
│ POST /v1/chat                                               │
│ Authorization: Bearer <JWT>                                 │
│ {"message": "Show me error logs for pricing-service"}       │
└─────────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────┐
│ MIDDLEWARE PIPELINE                                         │
│ ✓ CORS: Origin allowed                                      │
│ ✓ Rate Limit: 45/100 requests used                          │
│ ✓ JWT: Valid RS256, user=john.smith@tr.com                  │
│ ✓ Guardrails: No injection detected                         │
└─────────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────┐
│ SESSION MANAGER                                             │
│ Session: emp12345-a1b2c3d4 (existing, last active 5m ago)   │
│ Agent: OrchestratorAgent (with registered sub-agents)       │
└─────────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────┐
│ ORCHESTRATOR ROUTING                                        │
│ Keywords found: "error" (DD 1.5), "logs" (DD 1.5)           │
│ Scores: Datadog=15.0, K8s=0, Cert=0                         │
│ Decision: Route to DatadogAgent                             │
└─────────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────┐
│ DATADOG AGENT - AGENTIC LOOP                                │
│                                                             │
│ Iteration 1:                                                │
│   → Claude: "Use get_error_logs tool"                       │
│   → Execute: get_error_logs(service="pricing-service")      │
│   → Result: 15 error logs found                             │
│                                                             │
│ Iteration 2:                                                │
│   → Claude: "Here's what I found..." (stop_reason=end_turn) │
│   → Return response                                         │
└─────────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────┐
│ OUTPUT GUARDRAILS                                           │
│ ✓ No passwords detected                                     │
│ ✓ No API keys detected                                      │
│ ✓ No PII detected                                           │
└─────────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────┐
│ RESPONSE                                                    │
│ {                                                           │
│   "response": "I found 15 error logs for pricing-service...",│
│   "session_id": "emp12345-a1b2c3d4",                        │
│   "model_used": "claude-opus-4-5-20251101"                  │
│ }                                                           │
└─────────────────────────────────────────────────────────────┘
```

---

## 4. Base Agent vs Orchestrator

### Orchestrator Agent

**Purpose:** Traffic cop - routes user queries to the most appropriate specialized agent

**File:** `k8s-assistant/k8s_assistant/framework/orchestrator.py`

**Key Characteristics:**
- **No LLM calls** - Uses rule-based keyword scoring
- **Fast and predictable** - Deterministic routing
- **Maintains agent registry** - Knows about all specialized agents

**Routing Algorithm:**

```python
def _route_to_agent(self, message: str) -> Tuple[str, List[str], str]:
    # STEP 1: Check for explicit @mention
    if "@datadog" in message.lower():
        return ('datadog-agent', ['@datadog'], 'EXPLICIT')

    # STEP 2: Weighted keyword scoring
    scores = {}

    # Certificate keywords (weight 2.0 - most specific)
    cert_score = score_keywords(message, CERT_KEYWORDS, weight=2.0)

    # Datadog keywords (weight 1.5 - observability focus)
    dd_score = score_keywords(message, DATADOG_KEYWORDS, weight=1.5)

    # K8s keywords (weight 1.0 - infrastructure)
    k8s_score = score_keywords(message, K8S_KEYWORDS, weight=1.0)

    # STEP 3: Pick highest scoring agent
    winner = max(scores.items(), key=lambda x: x[1])

    # STEP 4: Default to DatadogAgent if no matches
    return winner or ('datadog-agent', [], 'DEFAULT')
```

### Base Agent

**Purpose:** Worker - provides common infrastructure for all specialized agents

**File:** `k8s-assistant/k8s_assistant/framework/base_agent.py`

**Key Characteristics:**
- **Abstract base class** - DatadogAgent, K8sAgent, CertAgent inherit from it
- **Calls Claude API** - Uses TR AI Platform Common Token APIs
- **Manages tool execution** - Registry pattern for tools
- **Handles conversation loop** - Max 10 iterations per request

**The Agentic Loop:**

```python
async def _execute_with_tools(self, messages, context):
    max_iterations = 10
    iteration = 0

    while iteration < max_iterations:
        iteration += 1

        # 1. Prepare context (auto-truncate if needed)
        prepared_messages = prepare_context_for_api(messages, ...)

        # 2. Call Claude
        response = self.client.messages.create(
            model=self.model_name,
            messages=prepared_messages,
            tools=self.tool_schemas
        )

        # 3. Check stop reason
        if response.stop_reason == "end_turn":
            return response.text  # Done!

        if response.stop_reason == "tool_use":
            # 4. Execute tools
            for tool_call in response.tool_calls:
                result = await self._execute_tool(tool_call.name, tool_call.input)

            # 5. Add results to conversation
            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tool_results})

            # 6. Loop continues...

    return "Max iterations exceeded"
```

### Comparison Table

| Aspect | Orchestrator Agent | Base Agent |
|--------|-------------------|------------|
| **Purpose** | Traffic cop - routes to specialists | Worker - does the actual work |
| **LLM Calls** | None (rule-based routing) | Yes (calls Claude for reasoning) |
| **Tools** | None | 10-19 specialized tools per agent |
| **Decision Logic** | Keyword scoring + weights | AI decides which tools to use |
| **Inheritance** | Standalone class | Abstract base (agents inherit) |
| **Latency** | ~1ms (just string matching) | ~2-30s (LLM + tool execution) |

### Why This Design?

1. **Separation of Concerns**: Routing is deterministic and fast; reasoning is AI-driven
2. **Cost Efficiency**: Simple routing doesn't need expensive LLM calls
3. **Maintainability**: Add new keywords without touching agent code
4. **Predictability**: Routing behavior is testable and debuggable
5. **Extensibility**: Easy to add new agents without modifying orchestrator logic

---

## 5. Multi-Model Switching

### Current Implementation Status: PARTIALLY IMPLEMENTED

**File:** `k8s-assistant/k8s_assistant/framework/model_selector.py`

### What's Designed vs What's Active

| Feature | Designed | Active |
|---------|----------|--------|
| Haiku for simple queries (98% cost savings) | Yes | **NO** |
| Sonnet for medium queries (80% cost savings) | Yes | **Only for large context** |
| Opus for complex queries | Yes | **DEFAULT for everything** |
| Context-based switching | Yes | **YES** |

### Current Strategy: Opus-First with Context Awareness

```python
class ModelSelector:
    # Token thresholds for model switching
    SONNET_THRESHOLD = 150_000   # Switch to Sonnet above this
    TRUNCATION_THRESHOLD = 180_000  # ContextManager truncates above this

    def select_model_for_context(self, tokens: int) -> str:
        if tokens < self.SONNET_THRESHOLD:
            # Standard context - use Opus for best quality
            return "claude-opus-4-5-20251101"
        elif tokens < self.TRUNCATION_THRESHOLD:
            # Large context - use Sonnet (still capable, cheaper)
            return "claude-sonnet-4-20250514"
        else:
            # Very large context - use Opus, ContextManager will truncate
            return "claude-opus-4-5-20251101"
```

### Why Opus-First?

From the code comments:
> "This approach prioritizes response quality over cost optimization."

**Rationale:**
1. DevOps queries require high accuracy (misdiagnosis is costly)
2. Tool selection needs sophisticated reasoning
3. Cost savings from Haiku (~$0.25/1M tokens) don't justify quality risk
4. Context-based switching handles the 200K token limit

### Model Specifications

| Model | Context Window | Cost (Input/1M) | Cost (Output/1M) | Use Case |
|-------|---------------|-----------------|------------------|----------|
| Haiku 3.5 | 200K | $0.25 | $1.25 | Simple queries (not used) |
| Sonnet 4 | 200K | $3.00 | $15.00 | Large context fallback |
| Opus 4.5 | 200K | $15.00 | $75.00 | Default (quality priority) |

### How to Test Model Switching

```python
# Create a conversation with >150K tokens
# Check logs for: "Model selected for context... using Sonnet"

# In the logs, you'll see:
# INFO: Model selected for context
# extra: {"model": "claude-sonnet-4-20250514", "tokens": 165000, "reason": "large context"}
```

---

## 6. Conversation History & Caching

### Two-Layer Caching System

#### Layer 1: Session/Conversation Memory (Short-term)

**File:** `k8s-assistant/k8s_assistant/api/services/chat_service.py`

```python
class SessionManager:
    def __init__(self, ttl_seconds: int = 3600, max_sessions: int = 1000):
        # TTLCache: 1 hour TTL, max 1000 concurrent sessions
        self._sessions: TTLCache = TTLCache(maxsize=max_sessions, ttl=ttl_seconds)
```

**What's Stored Per Session:**
- OrchestratorAgent instance (with registered sub-agents)
- User context (from JWT)
- Created/last activity timestamps
- Conversation history (via BaseAgent)

#### Layer 2: API Response Caching (K8s/Datadog)

**File:** `k8s-assistant/k8s_assistant/cache.py`

| Resource Type | TTL | Rationale |
|---------------|-----|-----------|
| Pods | 30 seconds | Pod status changes frequently |
| Metrics | 15 seconds | Real-time data needs freshness |
| Namespace | 5 minutes | Rarely changes |
| Certificates | 5 minutes | Changes are infrequent |
| HPA | 30 seconds | Scaling events are time-sensitive |
| Rollouts | 30 seconds | Deployment status matters |
| PVCs | 60 seconds | Storage is relatively stable |

```python
# Cache decorator usage
@cached(cache_type="pods")
def get_pods(namespace: str):
    # K8s API call (cached for 30s)
    return k8s_client.list_pods(namespace)
```

### Context Window Management

**File:** `k8s-assistant/k8s_assistant/framework/context_manager.py`

**Problem:** Claude has 200K token limit. Long conversations can exceed this.

**Solution:** Automatic context management with smart truncation.

```python
class ContextManager:
    MODEL_LIMITS = {
        "claude-opus-4-5-20251101": 200_000,
        "claude-sonnet-4-20250514": 200_000,
    }

    # Safety margins
    SOFT_LIMIT_PERCENT = 0.80  # 160K tokens - Start warning
    HARD_LIMIT_PERCENT = 0.95  # 190K tokens - Must truncate

    def truncate_messages(self, messages, target_tokens, ...):
        # Strategy:
        # 1. Always keep: system prompt + tools
        # 2. Always keep: last 6 messages
        # 3. Remove: oldest messages first
        # 4. If still over: truncate large tool results
```

**Truncation Order:**
1. Keep system prompt (always)
2. Keep tool schemas (always)
3. Keep last 6 messages (recent context)
4. Drop oldest messages first
5. If still over, truncate large tool results (keep first/last 4000 chars)

---

## 7. Memory Implementation

### Three-Tier Memory System

**File:** `k8s-assistant/k8s_assistant/memory/memory_service.py`

| Tier | Type | Implementation | Persistence | Status |
|------|------|----------------|-------------|--------|
| **Tier 1** | Short-term (Conversation) | `ConversationMemory` class | In-memory (session) | **IMPLEMENTED** |
| **Tier 2** | Long-term (Incidents) | `IncidentMemory` class | In-memory only | **IMPLEMENTED (no persistence)** |
| **Tier 3** | User Memory (Preferences) | `UserProfile` class | In-memory only | **IMPLEMENTED (no persistence)** |

### Tier 1: Short-Term Memory (ConversationMemory)

```python
class ConversationMemory:
    def __init__(self, conversation_id: str):
        self.conversation_id = conversation_id
        self.messages: List[Message] = []  # Full conversation history
        self.started_at = datetime.now()
        self.metadata = {}

    def get_context_summary(self) -> str:
        # Returns: "Conversation started 5 minutes ago | 12 messages |
        #           Services discussed: api-service, postgres |
        #           Environments: qa, prod"

    def _extract_entities(self) -> Dict[str, List[str]]:
        # Extracts services and environments mentioned in conversation
```

### Tier 2: Long-Term Memory (IncidentMemory)

```python
@dataclass
class Incident:
    id: str
    service_name: str
    environment: str
    symptoms: str          # "CrashLoopBackOff + NullPointerException"
    root_cause: Optional[str]
    resolution: Optional[str]
    occurred_at: datetime
    resolved_at: Optional[datetime]
    tags: List[str]        # ['crashloop', 'nullpointer', 'memory']

class IncidentMemory:
    def find_similar_incidents(self, service: str, symptoms: str) -> List[Incident]:
        # Uses simple word overlap (30% threshold)
        # NOT vector embeddings / semantic search
```

### Tier 3: User Memory (UserProfile)

```python
@dataclass
class UserProfile:
    user_id: str
    frequent_services: List[str]   # Top 10 services user asks about
    communication_style: str       # 'concise', 'detailed', 'technical'
    learned_mistakes: List[Dict]   # Past mistakes to avoid (last 20)
    last_updated: datetime
```

### Vector DB / Semantic Search: NOT IMPLEMENTED

**Current State:**
```python
def _calculate_similarity(self, text1: str, text2: str) -> float:
    """Calculate text similarity (simple word overlap)"""
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    common = words1.intersection(words2)
    return len(common) / max(len(words1), len(words2))
```

**From code comments:**
```python
"""
For MVP: Uses in-memory storage
For Production: Switch to PostgreSQL backend
"""
```

**Roadmap:**
- PostgreSQL for incident persistence
- Vector embeddings for semantic similarity
- Redis for distributed session caching

---

## 8. Security & Guardrails

### JWT Authentication

**File:** `k8s-assistant/k8s_assistant/api/middleware/jwt_auth.py`

**Explicitly Allowed Algorithms (RSA only):**
```python
ALLOWED_JWT_ALGORITHMS = frozenset(["RS256", "RS384", "RS512"])

# Rejected algorithms (security)
REJECTED_ALGORITHMS = frozenset([
    "none",      # No signature (critical vulnerability)
    "HS256",     # Symmetric (key confusion attack)
    "HS384", "HS512",
    "ES256", "ES384", "ES512",  # ECDSA (not used by TR SSO)
])
```

**Validation Flow:**
1. **Pre-validate algorithm** before signature check (prevents algorithm confusion attacks)
2. **Fetch signing key** from JWKS endpoint (cached 1 hour)
3. **Verify signature** with public key
4. **Verify claims:** exp, iss, sub
5. **Extract user context:** email, name, employee_id, groups

**User Context Extracted:**
```python
{
    "user_email": "john.smith@thomsonreuters.com",
    "user_name": "Smith, John (TR Technology)",
    "username": "jsmith",
    "employee_id": "emp12345",
    "groups": ["engineering", "devops"],
    "auth_type": "jwt"
}
```

### Input Guardrails

**File:** `k8s-assistant/k8s_assistant/guardrails/guardrails_service.py`

**52+ Prompt Injection Patterns:**
```python
INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?(previous|prior)\s+instructions",
    r"forget\s+(your|all)\s+(rules|instructions)",
    r"you\s+are\s+now",
    r"pretend\s+(you\s+are|to\s+be)",
    r"disregard\s+(all|your)",
    r"system\s*:\s*",
    r"\[INST\]",
    r"<\|im_start\|>",
    # ... 44 more patterns
]
```

**Blocked Topics:**
```python
BLOCKED_TOPICS = {
    "politics", "election", "religion", "dating",
    "medical advice", "legal advice", "financial advice",
    "gambling", "weapons", "drugs"
}
```

### Output Guardrails

**Sensitive Data Masking:**
```python
SENSITIVE_PATTERNS = [
    (r"(password|passwd|pwd)\s*[:=]\s*(\S+)", r"\1: [REDACTED]"),
    (r"(api[_-]?key)\s*[:=]\s*(\S+)", r"\1: [REDACTED]"),
    (r"Bearer\s+[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_]+", r"Bearer [REDACTED]"),
    (r"\b\d{3}-\d{2}-\d{4}\b", r"[SSN_REDACTED]"),  # SSN
    (r"\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b", r"[CARD_REDACTED]"),  # Credit card
]
```

### Rate Limiting

```python
# 100 requests per minute per user (employee_id)
rate_limit = RateLimiter(max_requests=100, window_seconds=60)
```

---

## 9. TR API Standard Framework Usage

### Anthropic Client Integration

**File:** `k8s-assistant/k8s_assistant/clients/anthropic_client.py`

**TR AI Platform Common Token API Flow:**

```python
class AnthropicTRClient:
    def _fetch_token(self) -> Dict[str, Any]:
        """
        POST https://aiplatform.gcs.int.thomsonreuters.com/v1/anthropic/token

        Headers:
            Authorization: Bearer {ESSO_TOKEN}
            Content-Type: application/json

        Body:
            {"asset_id": "208321"}  # AIML Platform Training Workspace

        Response:
            {
                "anthropic_api_key": "sk-ant-...",
                "expires_in": 3600,
                "token_type": "Bearer"
            }
        """

    def _get_or_refresh_token(self) -> str:
        """
        Automatic token refresh logic:
        - Check if token exists and not expired
        - If expired → fetch new token
        - Subtract 60s buffer for safety
        """

    def create_message(self, **kwargs):
        """
        Interface-compatible with Anthropic SDK
        - Gets valid token (refreshes if needed)
        - Creates Anthropic client with token
        - Calls Claude API
        """
```

**Usage in BaseAgent:**
```python
class BaseAgent:
    def __init__(self, ...):
        self.client = get_anthropic_client()  # Gets TR Client

    def _call_llm(self):
        response = self.client.messages.create(
            model="claude-opus-4-5-20251101",
            messages=self.conversation_history,
            tools=self.tool_schemas
        )
```

---

## 10. Feature Implementation Status

| Feature | Status | Notes |
|---------|--------|-------|
| **JWT Auth (RS256/384/512)** | ✅ Implemented | RSA only, no symmetric |
| **Rate Limiting (100/min)** | ✅ Implemented | Per employee_id |
| **Input Guardrails (52+ patterns)** | ✅ Implemented | Prompt injection, PII, topics |
| **Output Guardrails (PII masking)** | ✅ Implemented | Passwords, tokens, SSN, cards |
| **Model Routing (context-based)** | ✅ Implemented | Sonnet at 150K+ tokens |
| **Model Routing (complexity-based)** | ⚠️ Designed, not active | Defaults to Opus |
| **Session Management (1hr TTL)** | ✅ Implemented | TTLCache, 1000 max |
| **API Response Caching** | ✅ Implemented | Type-specific TTLs |
| **Context Window Management** | ✅ Implemented | Auto-truncation at 80% |
| **Short-term Memory** | ✅ Implemented | In-memory per session |
| **Long-term Memory (Incidents)** | ⚠️ In-memory only | No persistence |
| **Vector DB / Semantic Search** | ❌ Not implemented | Roadmap item |
| **SSE Streaming** | ✅ Implemented | Real-time response chunks |
| **Health Checks** | ✅ Implemented | /health/live, /health/ready |

---

## 11. Anticipated Technical Questions

### Q: Why Opus-first instead of cost optimization with Haiku?

**A:** DevOps troubleshooting requires high accuracy. A misdiagnosis can be more costly than the LLM cost savings. Opus provides:
- Better tool selection reasoning
- More accurate error pattern recognition
- Higher quality correlation analysis

Cost difference: ~$15 vs $0.25 per million input tokens, but quality justifies it for enterprise use.

### Q: What's the plan for production memory persistence?

**A:** MVP uses in-memory storage. Production roadmap includes:
1. PostgreSQL for incident history
2. Redis for distributed session caching
3. Vector embeddings (OpenAI/Cohere) for semantic similarity
4. Estimated: Q2 2026

### Q: How does the agentic loop prevent infinite loops?

**A:** Multiple safeguards:
1. **Hard limit:** Max 10 iterations per request
2. **Stop reason check:** Loop exits on "end_turn"
3. **Context management:** Large tool results get truncated
4. **Timeout:** 60s API timeout, 30s LLM timeout
5. **Logging:** Every iteration logged for debugging

### Q: How do you handle token limit errors?

**A:** ContextManager automatically:
1. Estimates tokens before API call
2. Warns at 80% (160K tokens)
3. Truncates at 95% (190K tokens)
4. Keeps: system prompt + tools + last 6 messages
5. Truncates large tool results (keeps first/last 4000 chars)

### Q: What happens if Datadog/K8s APIs are down?

**A:** Graceful degradation:
1. Tools return error dict: `{"error": "Connection failed"}`
2. Claude sees the error and explains to user
3. Cached results used if available
4. Health endpoint reports degraded state

### Q: How is sensitive data protected?

**A:** Defense in depth:
1. **Input:** 52+ injection patterns blocked
2. **Processing:** No PII logging, structured logging only
3. **Output:** Automatic masking of passwords, tokens, SSN, cards
4. **Auth:** JWT with RSA signatures only (no HS256)
5. **Transport:** HTTPS only, CORS restricted

---

## 12. Demo Scenarios

For the live demo portion, use these scenarios from the demo script:

### Scenario 1: Pod Health Check (1 minute)
```
Show me unhealthy pods in QA
```
Demonstrates: K8s agent, pod status, immediate value

### Scenario 2: Error Log Analysis (1 minute)
```
Get error logs for pricing-be in the last hour
```
Demonstrates: Datadog agent, natural language to query, time handling

### Scenario 3: Full Investigation (2 minutes) - THE WOW MOMENT
```
Investigate errors in confirmation-service with full context
```
Demonstrates: Multi-tool coordination, correlation, root cause analysis

### Scenario 4: Cross-Agent Workflow (1 minute)
```
pricing-be pods are crashing - investigate why
```
Demonstrates: Orchestrator routing, K8s + Datadog coordination

---

## 13. Simplified Traffic Flow - One Example

**Query:** `"Show me error logs for pricing-service"`

```
┌──────────────────────────────────────────────────────────────────────┐
│ 1. API ENTRY                                                         │
│    chat.py → chat_endpoint()                                         │
│    Input: POST /v1/chat with JWT token                               │
└────────────────────────────┬─────────────────────────────────────────┘
                             ▼
┌──────────────────────────────────────────────────────────────────────┐
│ 2. CHAT SERVICE                                                      │
│    chat_service.py → process_message()                               │
│    • SessionManager.get_or_create_session()                          │
│    • guardrails.validate_input()                                     │
│    • ModelSelector.select_model() → Opus                             │
└────────────────────────────┬─────────────────────────────────────────┘
                             ▼
┌──────────────────────────────────────────────────────────────────────┐
│ 3. ORCHESTRATOR ROUTING                                              │
│    orchestrator.py → _route_to_agent()                               │
│                                                                      │
│    Keyword Scoring:                                                  │
│    • "error" matched → 5 chars × 1.5 = 7.5                           │
│    • "logs" matched  → 4 chars × 1.5 = 6.0                           │
│    • Total: 13.5 → WINNER: datadog-agent                             │
└────────────────────────────┬─────────────────────────────────────────┘
                             ▼
┌──────────────────────────────────────────────────────────────────────┐
│ 4. BASE AGENT - AGENTIC LOOP                                         │
│    base_agent.py → _execute_with_tools()                             │
│                                                                      │
│    ITERATION 1:                                                      │
│    ├─ prepare_context_for_api() → Estimate tokens, truncate if >80%  │
│    ├─ client.messages.create() → Call Claude API                     │
│    ├─ Claude returns: tool_use "get_error_logs"                      │
│    ├─ _execute_tool() → tool["func"](**input)                        │
│    │   └─ get_error_logs() [datadog_tools.py]                        │
│    │       └─ Datadog LogsApi.list_logs()                            │
│    └─ Append tool_result to messages → LOOP                          │
│                                                                      │
│    ITERATION 2:                                                      │
│    ├─ client.messages.create() → Claude sees tool results            │
│    ├─ Claude returns: end_turn "I found 23 errors..."                │
│    └─ RETURN final_response                                          │
└────────────────────────────┬─────────────────────────────────────────┘
                             ▼
┌──────────────────────────────────────────────────────────────────────┐
│ 5. RESPONSE                                                          │
│    • guardrails.validate_output() → Mask sensitive data              │
│    • Return: {response, session_id, model_used}                      │
└──────────────────────────────────────────────────────────────────────┘
```

### Files Touched (in order):
```
1. api/routes/v1/chat.py        → Entry point
2. api/services/chat_service.py → Session + orchestration
3. framework/orchestrator.py    → Keyword routing
4. framework/base_agent.py      → Agentic loop
5. tools/datadog_tools.py       → Tool execution
6. clients/anthropic_client.py  → Claude API call
```

### Key Code (Base Agent Loop):
```python
# base_agent.py - THE AGENTIC LOOP (simplified)
for iteration in range(10):  # Max 10 iterations
    response = claude.messages.create(messages, tools)

    if response.stop_reason == "end_turn":
        return response.text  # DONE

    if response.stop_reason == "tool_use":
        result = tool["func"](**input)  # Direct Python call
        messages.append(tool_result)    # Add result, loop again
```

---

## Appendix: File Locations Quick Reference

```
k8s-ops-assistant/
├── k8s-assistant/
│   └── k8s_assistant/
│       ├── agents/
│       │   ├── datadog_agent.py      # 19 tools
│       │   ├── k8s_agent.py          # 10 tools
│       │   └── cert_agent.py         # 1 tool
│       ├── framework/
│       │   ├── base_agent.py         # Agentic loop
│       │   ├── orchestrator.py       # Keyword routing
│       │   ├── model_selector.py     # Model switching
│       │   └── context_manager.py    # Token management
│       ├── api/
│       │   ├── main.py               # FastAPI + middleware
│       │   ├── middleware/jwt_auth.py
│       │   └── services/chat_service.py
│       ├── guardrails/
│       │   └── guardrails_service.py # Input/output validation
│       ├── memory/
│       │   └── memory_service.py     # 3-tier memory
│       ├── tools/
│       │   ├── k8s_tools.py
│       │   ├── datadog_tools.py
│       │   ├── datadog_trace_tools.py
│       │   ├── datadog_metrics_tools.py
│       │   └── datadog_correlation_tools.py
│       ├── cache.py                  # TTL caching
│       └── config.py                 # Pydantic settings
├── docs/
│   ├── architecture/
│   │   └── 07-unified-architecture.md
│   └── presentation/
│       ├── DEMO_SCRIPT_DATADOG_K8S.md
│       └── ARCHITECTURE_WALKTHROUGH.md  # This file
└── tests/
    ├── unit/
    ├── api/
    ├── integration/
    └── e2e/
```

---

**Document Version:** 1.0
**Last Updated:** February 2026
**Author:** DevOps Assistant Team
