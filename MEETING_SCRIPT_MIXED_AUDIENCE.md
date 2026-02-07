# DevOps Assistant - Team Meeting Script

**Duration:** 1 hour
**Format:** Live Meeting (Teams/Zoom)
**Audience:** VPs, Architects, Dev Managers, QA Team
**Organized By:** QA Team

---

## Meeting Flow Overview

```
┌─────────────────────────────────────────────────────────────────┐
│  0-2 min   │  OPENING                                           │
│            │  Impact statement, acknowledge QA                   │
├────────────┼────────────────────────────────────────────────────┤
│  2-18 min  │  LIVE DEMO                                         │
│            │  4 scenarios, architecture woven in naturally       │
├────────────┼────────────────────────────────────────────────────┤
│ 18-30 min  │  QA TEAM USE CASES                                 │
│            │  QA drives with pre-coordinated queries             │
├────────────┼────────────────────────────────────────────────────┤
│ 30-50 min  │  OPEN DISCUSSION                                   │
│            │  Q&A for all audiences                              │
├────────────┼────────────────────────────────────────────────────┤
│ 50-60 min  │  NEXT STEPS & CLOSE                                │
│            │  Adoption path, contacts                            │
└─────────────────────────────────────────────────────────────────┘
```

---

## PRE-MEETING CHECKLIST (Critical - 30 min before)

### System Validation
```
[ ] Kubernetes cluster connected (test: kubectl get pods)
[ ] Datadog API responding (test: check Datadog UI)
[ ] Claude API working (TR AI Platform token valid)
[ ] Portal/Streamlit UI accessible
[ ] Clear conversation history
```

### Demo Query Validation
```
[ ] "Show me unhealthy pods in QA" - returns data
[ ] "Get error logs for pricing-be in the last hour" - returns data
[ ] "Investigate errors in confirmation-service with full context" - completes
[ ] "pricing-be pods are crashing - investigate why" - completes
```

### QA Coordination
```
[ ] Confirm 2-3 queries with QA lead
[ ] Test QA's queries work
[ ] QA lead knows when they'll be called on
```

### Technical Setup
```
[ ] Screen share tested
[ ] Backup queries noted on paper
[ ] Second browser tab with Portal ready
[ ] Mute notifications
```

---

## PART 1: OPENING (0-2 minutes)

**[Show: DevOps Assistant UI - clean chat interface]**

> "Thanks everyone for joining, and thanks to [QA Lead name] for organizing this.
>
> I'll keep this simple - I'm going to show you a tool that changes how we investigate issues.
>
> **The quick version:** A full incident investigation - checking logs, traces, metrics, pod health, correlating everything - used to take 30 to 45 minutes across multiple tools. Now it takes 90 seconds with one question.
>
> This is the DevOps Assistant. It understands natural language and queries real systems - Datadog and Kubernetes - in real time.
>
> Let me show you rather than tell you."

**[Immediately start first demo - no more talking]**

---

## PART 2: LIVE DEMO (2-18 minutes)

---

### Demo 1: Pod Health Check (3 min)

**[Type in the chat]**
```
Show me unhealthy pods in QA
```

**While waiting, say:**
> "This is what QA might check before running a test suite - is the environment healthy?
>
> Notice the streaming - it's calling real Kubernetes APIs right now."

**When response appears:**
> "Pod names, current status, what OOMKilled means, recommended next steps.
>
> Anyone on the team can now check environment health in seconds. No kubectl required."

**Architecture hook (casual):**
> "Behind the scenes, that used our Kubernetes agent - 10 specialized tools for cluster operations."

---

### Demo 2: Error Log Analysis (3 min)

**[Type in the chat]**
```
Get error logs for pricing-be in the last hour
```

**While waiting, say:**
> "Instead of writing Datadog query syntax, I just describe what I need.
>
> The agent knows our service naming conventions - maps 'pricing-be' to the correct Datadog tags automatically."

**When response appears:**
> "Error types, frequency, timestamps, context from each log entry.
>
> This would normally take several minutes navigating the Datadog UI."

**Architecture hook (casual):**
> "That's the Datadog agent - 19 tools for logs, traces, metrics, and correlation."

---

### Demo 3: Full Investigation - THE WOW MOMENT (5 min)

**[Type in the chat]**
```
Investigate errors in confirmation-service with full context
```

**While waiting, say:**
> "Watch what happens. It's going to:
> - Query error logs
> - Search for related traces in APM
> - Check service health metrics
> - Correlate everything and identify patterns
>
> This is exactly what a senior engineer does during incident investigation - but automated."

**Point to streaming updates:**
> "You can see the tool calls - query_logs, query_traces, get_service_health_metrics.
>
> It's running the same troubleshooting workflow we would run manually."

**When response appears:**
> "Look at this:
> - **Log Analysis**: Error patterns identified
> - **Trace Analysis**: Slow spans, latency breakdown
> - **Metrics**: Error rate compared to baseline
> - **Root Cause**: Clear hypothesis with supporting evidence
>
> In 90 seconds, with one question, we completed an investigation that would typically take 30 to 45 minutes.
>
> That's not incremental improvement. That's a fundamental change in how we diagnose issues."

**Architecture hook (casual):**
> "What you just saw is the agentic loop - Claude decides which tools to call, executes them, reasons over results, and chains them together until it has a complete answer."

---

### Demo 4: Cross-Agent Workflow (3 min)

**[Type in the chat]**
```
pricing-be pods are crashing - investigate why
```

**While waiting, say:**
> "I didn't specify which tool to use. It figures that out automatically.
>
> This will use both agents - Kubernetes to check pod status and events, Datadog to find related errors and patterns."

**When response appears:**
> "Combined data from both sources:
> - Kubernetes shows pods restarting with OOMKilled status
> - Datadog shows memory usage increasing before each crash
> - Root cause: likely a memory leak
>
> Two agents, one conversation, complete picture."

**Architecture hook (casual):**
> "The orchestrator routed this to both agents based on keywords - 'pods' triggered Kubernetes, 'crashing' triggered Datadog investigation."

---

## PART 3: QA TEAM USE CASES (18-30 minutes)

**[Transition]**

> "Those are the core capabilities. But [QA Lead], your team has been using this - what scenarios would be most relevant to show everyone?"

**Let QA lead drive. They might ask:**
- Environment health checks before test runs
- Investigating test failures
- Checking service status after deployments

**If QA's query works:** Run it, let results speak

**If QA's query needs tweaking:** "Let me adjust the phrasing slightly..." then run

**If unsure about query:** "That's a great use case - let me show a similar one first, then we can explore that specific scenario."

**Encourage discussion:**
> "What other scenarios would help your daily work?"

---

## PART 4: OPEN DISCUSSION (30-50 minutes)

**Transition:**
> "Let's open it up for questions. Happy to go deeper on any aspect - technical architecture, security, how to get started."

### Expected Questions & Answers

#### From VPs

| Question | Answer |
|----------|--------|
| "What's the cost?" | "Uses TR AI Platform tokens. Roughly $X per query, but saves 30+ minutes of engineer time per investigation. The ROI is significant for incident response." |
| "Is this production ready?" | "Yes - live now in the Portal. QA team has been using it. We're iterating based on feedback." |
| "Security concerns?" | "Three layers: JWT authentication for access control, input guardrails that block prompt injection attempts, output guardrails that mask sensitive data like passwords and tokens." |
| "Can it take actions?" | "Currently read-only - investigation and diagnosis focused. That's intentional for safety. Action capabilities would require additional approval workflows." |

#### From Architects

| Question | Answer |
|----------|--------|
| "What model are you using?" | "Claude Opus 4.5 via TR AI Platform - best reasoning capability for complex multi-step investigations." |
| "How do you prevent hallucination?" | "All responses are grounded in real API calls. You saw the tool calls executing - no guessing. If data doesn't exist, it says so." |
| "How does the routing work?" | "Keyword scoring with weights. Certificate queries get highest priority (weight 2.0), then Datadog (1.5), then Kubernetes (1.0). You can also use @datadog or @k8s for explicit routing." |
| "What about context limits?" | "Auto-truncation at 80% of 200K token limit. Keeps system prompt and last 6 messages. Context manager handles this transparently." |
| "How many tools total?" | "30 tools across 3 agents: 19 for Datadog (logs, traces, metrics, correlation), 10 for Kubernetes, 1 for certificate monitoring." |
| "Can we add custom tools?" | "Yes - tool registration is modular. Define schema, implement function, register with agent." |

#### From Dev Managers

| Question | Answer |
|----------|--------|
| "Training needed?" | "None. Just type questions in English. The demo you just saw is the interface." |
| "Can my team break it?" | "Guardrails block prompt injection and off-topic queries. It only does DevOps tasks. We just added protection against prompt leakage attacks too." |
| "Support?" | "Reach out to Audit DevOps team. We're actively iterating based on feedback." |
| "How do we onboard?" | "Access through the Portal. No special setup needed - just start asking questions." |

#### From QA

| Question | Answer |
|----------|--------|
| "Can it check all environments?" | "Yes - works across namespaces: CI, QA, Demo, Prod." |
| "Pre-test health checks?" | "Perfect use case. 'Show unhealthy pods in QA' before test runs." |
| "Can it help debug test failures?" | "Yes - 'Investigate errors in [service] in the last hour' after a failed test run." |

---

## PART 5: NEXT STEPS & CLOSE (50-60 minutes)

**Summarize:**
> "Let me quickly recap what we covered:
>
> **The DevOps Assistant** - AI-powered operations tool that brings together Kubernetes and Datadog in one natural language interface.
>
> **Key benefits:**
> 1. **Faster troubleshooting** - 30-45 min investigations in 90 seconds
> 2. **Democratized access** - No kubectl or Datadog query syntax needed
> 3. **Reduced context switching** - Everything in one conversation
> 4. **Consistent quality** - Same thorough investigation every time

**Call to action:**
> "It's available now through the Audit DevOps Portal.
>
> If you'd like a hands-on session for your team, or have specific use cases you'd like to explore, reach out to the Audit DevOps team.
>
> Thanks for your time today."

---

## APPENDIX

### Backup Queries (If Primary Fails)

```
List all pods in confirmation-qa
```

```
What namespaces are available?
```

```
@datadog check health of api-adapter-be
```

```
Describe the api-adapter pod in QA
```

### Recovery Phrases

| Situation | What to Say |
|-----------|-------------|
| Query takes too long | "Real-time data from production systems - sometimes takes a moment to gather everything." |
| Unexpected error | "Let me try a different phrasing..." (use backup query) |
| No data found | "Good news - no errors in that service right now. Let me show another example." |
| API timeout | "The connection timed out - this happens occasionally with live systems. Let me retry." |
| Query fails completely | "That's actually a great edge case to note. Let me show a similar query that demonstrates the capability." |

### Architecture Quick Reference (If Asked)

```
                         ┌─────────────────┐
                         │   Portal/UI     │
                         └────────┬────────┘
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│ MIDDLEWARE: JWT Auth → Rate Limit → Guardrails                   │
└─────────────────────────────────┬───────────────────────────────┘
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│ ORCHESTRATOR: Keyword Routing (Cert=2.0, Datadog=1.5, K8s=1.0)  │
└────────────┬─────────────────────┬──────────────────┬───────────┘
             ▼                     ▼                  ▼
      ┌───────────┐         ┌───────────┐      ┌───────────┐
      │ DATADOG   │         │ K8S       │      │ CERT      │
      │ 19 tools  │         │ 10 tools  │      │ 1 tool    │
      └─────┬─────┘         └─────┬─────┘      └─────┬─────┘
            └─────────────────────┴──────────────────┘
                                  ▼
                    ┌─────────────────────────┐
                    │ BASE AGENT: Agentic Loop │
                    │ (max 10 iterations)      │
                    └─────────────────────────┘
```

### Key Numbers to Remember

| Metric | Value |
|--------|-------|
| Total tools | 30 |
| Datadog agent tools | 19 |
| K8s agent tools | 10 |
| Cert agent tools | 1 |
| Guardrail patterns | 12 |
| Max agentic iterations | 10 |
| Context limit | 200K tokens (auto-truncate at 80%) |
| Session TTL | 1 hour |
| Rate limit | 100 req/min per user |

---

## Post-Meeting

- [ ] Send follow-up email with Portal access info
- [ ] Note any feature requests or feedback
- [ ] Schedule hands-on sessions if requested
- [ ] Share this script with team for future demos
