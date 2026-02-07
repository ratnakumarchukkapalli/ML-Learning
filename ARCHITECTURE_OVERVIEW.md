# DevOps Assistant - Architecture Overview

## Executive Summary

The DevOps Assistant is an AI-powered operations platform that transforms how teams interact with infrastructure and observability data. By leveraging Claude as an intelligent reasoning engine, the platform enables natural language queries against Kubernetes clusters and Datadog observability systems, dramatically reducing the time and expertise required for incident investigation and operational tasks.

**Key Value Proposition:** Investigations that traditionally require 30-45 minutes of navigating multiple tools and writing complex queries can now be completed in under 90 seconds through conversational interaction.

---

## Architectural Philosophy

### Software 3.0 Paradigm

The DevOps Assistant represents a fundamental shift from traditional software development approaches:

| Paradigm | Approach | Example |
|----------|----------|---------|
| **Software 1.0** | Explicit rules and conditionals | `if status == "error": alert()` |
| **Software 2.0** | Learned patterns from data | ML model trained on log patterns |
| **Software 3.0** | Natural language reasoning | "Investigate why pricing-service has errors" |

In the Software 3.0 paradigm, we do not prescribe specific workflows or decision trees. Instead, we provide the AI with:
- A set of well-defined tools (capabilities)
- Domain context (system prompts describing our infrastructure)
- Access to real-time data sources

The AI then reasons about user intent and autonomously determines which tools to invoke, in what sequence, and how to synthesize the results into actionable insights.

---

## System Architecture

### High-Level Component Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           CLIENT LAYER                                       │
│                    (Audit DevOps Portal / Streamlit UI)                      │
└─────────────────────────────────────┬───────────────────────────────────────┘
                                      │ HTTPS + JWT Bearer Token
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          MIDDLEWARE LAYER                                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ CORS Policy  │→ │ Rate Limiter │→ │ JWT Auth     │→ │ Guardrails   │     │
│  │              │  │ (100/min)    │  │ (RS256/384)  │  │ (12 patterns)│     │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────┬───────────────────────────────────────┘
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                       SESSION MANAGEMENT LAYER                               │
│           TTLCache: 1-hour session TTL | 1,000 concurrent sessions           │
└─────────────────────────────────────┬───────────────────────────────────────┘
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         ORCHESTRATION LAYER                                  │
│                                                                              │
│    ┌────────────────────────────────────────────────────────────────────┐   │
│    │                    ORCHESTRATOR AGENT                               │   │
│    │  Intelligent Routing: @mentions → Keyword Scoring → Default Fallback│   │
│    └────────────┬─────────────────────┬─────────────────────┬───────────┘   │
│                 ▼                     ▼                     ▼               │
│    ┌────────────────────┐ ┌────────────────────┐ ┌────────────────────┐    │
│    │   DATADOG AGENT    │ │     K8S AGENT      │ │    CERT AGENT      │    │
│    │    (19 Tools)      │ │    (10 Tools)      │ │     (1 Tool)       │    │
│    │                    │ │                    │ │                    │    │
│    │ • Log Analysis     │ │ • Pod Management   │ │ • TLS Certificate  │    │
│    │ • Trace Correlation│ │ • Event Inspection │ │   Monitoring       │    │
│    │ • Metrics Query    │ │ • Resource Metrics │ │                    │    │
│    │ • Multi-pillar     │ │ • Deployment Status│ │                    │    │
│    │   Investigation    │ │ • Namespace Search │ │                    │    │
│    └────────────────────┘ └────────────────────┘ └────────────────────┘    │
└─────────────────────────────────────┬───────────────────────────────────────┘
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         EXECUTION LAYER                                      │
│                                                                              │
│    ┌────────────────────────────────────────────────────────────────────┐   │
│    │                       BASE AGENT                                    │   │
│    │              Agentic Loop (Maximum 10 Iterations)                   │   │
│    │                                                                     │   │
│    │  ┌─────────────────────────────────────────────────────────────┐   │   │
│    │  │ 1. Prepare context → 2. Call Claude → 3. Execute tools →    │   │   │
│    │  │ 4. Append results → 5. Loop until "end_turn"                │   │   │
│    │  └─────────────────────────────────────────────────────────────┘   │   │
│    └────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────┬───────────────────────────────────────┘
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        INTEGRATION LAYER                                     │
│                                                                              │
│    ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐        │
│    │  TR AI Platform  │  │  Kubernetes API  │  │   Datadog API    │        │
│    │  (Claude Opus)   │  │  (EKS Clusters)  │  │  (Logs/APM/      │        │
│    │                  │  │                  │  │   Metrics)       │        │
│    └──────────────────┘  └──────────────────┘  └──────────────────┘        │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Core Components

### 1. Orchestrator Agent

The Orchestrator serves as the intelligent routing layer, directing user queries to the most appropriate specialized agent. Unlike traditional rule engines, routing decisions are made through a weighted keyword scoring algorithm combined with explicit mention support.

**Routing Priority:**

| Priority | Method | Description |
|----------|--------|-------------|
| 1 | Explicit Mention | User specifies `@datadog`, `@k8s`, or `@cert` |
| 2 | Weighted Scoring | Keywords matched against agent domains |
| 3 | Default Fallback | Datadog agent (most common use case) |

**Keyword Weighting Strategy:**

| Agent | Weight | Rationale |
|-------|--------|-----------|
| Certificate | 2.0 | Highest specificity - unambiguous intent |
| Datadog | 1.5 | Primary observability workload |
| Kubernetes | 1.0 | Infrastructure queries |

This weighting ensures that specialized queries (certificate expiry checks) are not inadvertently routed to general-purpose agents.

### 2. Specialized Agents

Each agent encapsulates domain-specific expertise and tooling:

**Datadog Agent (19 Tools)**
- Log querying and analysis
- APM trace correlation
- Metrics aggregation and comparison
- Multi-pillar investigation (logs + traces + metrics)

**Kubernetes Agent (10 Tools)**
- Pod health and status monitoring
- Event stream analysis
- Resource utilization metrics
- Deployment and rollout status
- Cross-namespace search capabilities

**Certificate Agent (1 Tool)**
- TLS certificate expiry monitoring
- Multi-domain scanning

### 3. Base Agent - The Agentic Loop

The Base Agent implements the core reasoning loop that enables autonomous investigation:

```
┌─────────────────────────────────────────────────────────────────┐
│                    AGENTIC LOOP                                  │
│                                                                  │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐    │
│  │   Prepare    │ ──► │  Call Claude │ ──► │   Evaluate   │    │
│  │   Context    │     │     API      │     │   Response   │    │
│  └──────────────┘     └──────────────┘     └──────┬───────┘    │
│                                                    │            │
│                              ┌─────────────────────┴──────┐     │
│                              ▼                            ▼     │
│                    ┌──────────────┐            ┌──────────────┐ │
│                    │  Tool Use?   │            │  End Turn?   │ │
│                    └──────┬───────┘            └──────┬───────┘ │
│                           │                          │         │
│                           ▼                          ▼         │
│                    ┌──────────────┐            ┌──────────────┐ │
│                    │   Execute    │            │    Return    │ │
│                    │    Tool      │            │   Response   │ │
│                    └──────┬───────┘            └──────────────┘ │
│                           │                                     │
│                           ▼                                     │
│                    ┌──────────────┐                             │
│                    │   Append     │ ────► Continue Loop         │
│                    │   Results    │       (max 10 iterations)   │
│                    └──────────────┘                             │
└─────────────────────────────────────────────────────────────────┘
```

**Key Characteristics:**
- **Autonomous Reasoning:** Claude determines which tools to invoke based on user intent
- **Iterative Refinement:** Multiple tool calls can be chained to build comprehensive answers
- **Bounded Execution:** Maximum 10 iterations prevents runaway queries
- **Context Preservation:** Conversation history enables follow-up questions

---

## Security Architecture

### Authentication & Authorization

| Layer | Implementation | Details |
|-------|----------------|---------|
| Authentication | JWT (RS256/RS384/RS512) | RSA-based signing only; symmetric algorithms rejected |
| Token Validation | JWKS with 1-hour cache | Keys fetched from SSO endpoint |
| User Context | Claims extraction | Email, employee ID, group memberships |
| Rate Limiting | Per-user throttling | 100 requests per minute per employee ID |

### Input Guardrails

The system implements comprehensive input validation to prevent prompt injection and misuse:

**Protected Against:**
- Instruction override attempts ("ignore previous instructions")
- Role manipulation ("you are now a different assistant")
- System prompt extraction ("show me your instructions")
- Token boundary attacks (`[INST]`, `<|im_start|>`)

**Current Pattern Coverage:** 12 distinct attack vectors

### Output Guardrails

All responses are sanitized before delivery:

| Data Type | Action |
|-----------|--------|
| Passwords | Redacted |
| API Keys | Redacted |
| Bearer Tokens | Redacted |
| Social Security Numbers | Redacted |
| Credit Card Numbers | Redacted |

---

## Context Management

### Token Limit Handling

The system implements intelligent context management to handle long conversations:

| Threshold | Tokens | Action |
|-----------|--------|--------|
| Normal | < 160K | Full context preserved |
| Soft Limit | 160K-190K | Warning logged, Sonnet model considered |
| Hard Limit | > 190K | Automatic truncation of oldest messages |

**Truncation Strategy:**
- System prompt always preserved
- Tool definitions always preserved
- Most recent 6 messages retained
- Oldest messages truncated first

---

## Model Selection Strategy

### Current Implementation: Opus-First

The platform utilizes Claude Opus 4.5 as the primary reasoning engine, selected for its superior performance on complex multi-step investigations.

**Context-Based Routing:**

| Context Size | Model Selection | Rationale |
|--------------|-----------------|-----------|
| < 150K tokens | Claude Opus 4.5 | Maximum reasoning capability |
| 150K-180K tokens | Claude Sonnet 4 | Cost optimization for large contexts |
| > 180K tokens | Claude Opus 4.5 + Truncation | Maintain quality with managed context |

---

## Integration Points

### TR AI Platform

- **Protocol:** HTTPS REST API
- **Authentication:** ESSO token-based
- **Model:** Claude Opus 4.5 (claude-opus-4-5-20251101)
- **Workspace:** Asset ID managed via configuration

### Kubernetes (EKS)

- **Protocol:** Kubernetes API via boto3/kubernetes client
- **Authentication:** AWS IAM with profile-based credentials
- **Scope:** Read-only operations across all namespaces

### Datadog

- **Protocol:** Datadog API v2
- **Capabilities:** Logs API, APM API, Metrics API
- **Scope:** Read-only queries with configurable time ranges

---

## Operational Characteristics

### Performance Metrics

| Metric | Target |
|--------|--------|
| Simple query response | < 5 seconds |
| Full investigation | < 90 seconds |
| Session capacity | 1,000 concurrent users |
| Request rate limit | 100/min per user |

### Caching Strategy

| Resource Type | Cache TTL | Rationale |
|---------------|-----------|-----------|
| Pod status | 30 seconds | Balance freshness with API load |
| Metrics data | 15 seconds | Near real-time accuracy required |
| Namespace list | 5 minutes | Infrequently changing |
| Certificate data | 5 minutes | Expiry data is stable |

---

## Tooling Summary

### Complete Tool Inventory

**Datadog Agent - 19 Tools**

| Category | Tools | Purpose |
|----------|-------|---------|
| Logs | 4 | `query_logs`, `get_error_logs`, `get_service_logs`, `get_recent_errors_summary` |
| Traces | 5 | `query_traces`, `get_trace_details`, `get_slow_traces`, `correlate_trace_with_logs`, `get_service_dependencies` |
| Metrics | 6 | `query_apm_metrics`, `get_service_health_metrics`, `get_metric_timeseries`, `compare_metrics_across_services`, `get_slo_status`, `discover_service_operation` |
| Correlation | 4 | `investigate_error_full_context`, `analyze_service_health_unified`, `trace_error_to_root_cause`, `detect_anomalies` |

**Kubernetes Agent - 10 Tools**

| Tool | Purpose |
|------|---------|
| `get_pods` | List pods with filtering |
| `describe_pod` | Detailed pod information |
| `get_pod_events` | Pod failure diagnostics |
| `get_namespaces` | List available namespaces |
| `resolve_namespace` | Fuzzy namespace matching |
| `get_hpa_status` | Horizontal Pod Autoscaler status |
| `get_rollout_status` | Argo Rollout deployment status |
| `get_pvcs` | PersistentVolumeClaim information |
| `get_resource_metrics` | CPU/Memory utilization |
| `search_resources` | Cross-namespace resource search |

**Certificate Agent - 1 Tool**

| Tool | Purpose |
|------|---------|
| `check_certificate_expiry` | TLS certificate monitoring with expiry alerting |

---

## Design Principles

### 1. Grounded Responses
All assistant responses are derived from actual API calls to production systems. The platform does not generate speculative or fabricated data.

### 2. Transparent Execution
Tool invocations are streamed to users in real-time, providing visibility into the assistant's reasoning process and data sources.

### 3. Bounded Autonomy
The agentic loop is constrained to 10 iterations maximum, preventing unbounded execution while allowing sufficient depth for complex investigations.

### 4. Defense in Depth
Security is implemented across multiple layers: authentication, authorization, input validation, output sanitization, and rate limiting.

### 5. Graceful Degradation
The system maintains functionality even when optional components (NeMo Guardrails) are unavailable, falling back to basic protection mechanisms.

---

## Future Considerations

### Planned Enhancements

| Capability | Status | Description |
|------------|--------|-------------|
| Vector Database | Roadmap | Semantic search for similar incidents |
| Complexity-Based Routing | Designed | Route simple queries to faster/cheaper models |
| Action Capabilities | Under Review | Safe write operations with approval workflows |
| Expanded Agents | Roadmap | Additional domain agents (AWS, GitHub, etc.) |

---

## Conclusion

The DevOps Assistant represents a significant advancement in operational tooling, applying modern AI capabilities to the challenge of infrastructure observability. By combining intelligent routing, specialized domain agents, and a robust security framework, the platform enables teams to investigate and resolve issues with unprecedented speed and consistency.

The architecture is designed for extensibility, allowing new agents and tools to be integrated as operational needs evolve, while maintaining the security and reliability characteristics required for production deployment.

---

*Document Version: 1.0*
*Last Updated: February 2026*
