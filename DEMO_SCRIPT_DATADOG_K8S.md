# DevOps Assistant - Demo Script

**Duration:** 10-12 minutes
**Format:** Recorded Video for Organization-wide Distribution
**Audience:** Developers, DevOps, ITOps, QA Engineers, Architects
**Focus:** Datadog Agent (Observability) + K8s Agent (Kubernetes Operations)

---

## Pre-Recording Checklist

- [ ] Streamlit UI running (or Portal URL ready)
- [ ] Kubernetes cluster connected
- [ ] Datadog credentials configured
- [ ] Conversation history cleared
- [ ] Screen recording software ready
- [ ] Microphone tested
- [ ] Test each demo query works

---

## DEMO SCRIPT

---

### 1. WHAT IS DEVOPS ASSISTANT (2-3 minutes)

**[Show: DevOps Assistant UI - clean chat interface]**

> "This is the DevOps Assistant - an AI-powered operations assistant built for the Audit DevOps Portal.
>
> Before I show you what it does, let me explain the problem it solves."

**[Pause for emphasis]**

> "Today, when an issue occurs in production or QA - whether it's a service throwing errors, pods crashing, or latency spikes - our teams need to investigate across multiple tools.
>
> They open Datadog to search logs, switch to APM for traces, check metrics dashboards, then jump to kubectl or Lens for Kubernetes status. Each tool has its own query syntax, its own interface, its own learning curve.
>
> A typical investigation involves:
> - Writing Datadog log queries with the correct syntax
> - Navigating between Logs, APM, and Metrics views
> - Running kubectl commands to check pod status and events
> - Manually correlating timestamps across all these sources
>
> By combining all these capabilities into one interface, the DevOps Assistant eliminates context-switching and lets teams focus on solving problems rather than navigating tools.
>
> Let me show you how."

**[Gesture to the UI]**

> "Instead of learning multiple tools, you ask questions in plain English.
>
> 'Show me errors in pricing-service'
> 'Why are pods crashing in QA?'
> 'Investigate latency issues in the checkout flow'
>
> The assistant understands your intent, queries the right systems, and returns actionable answers - all in one conversation.
>
> This means:
> - **Developers** can troubleshoot without waiting for DevOps
> - **QA Engineers** can verify environment health before running tests
> - **ITOps** can quickly assess incident impact
> - **DevOps** can focus on complex problems instead of answering routine questions
>
> It democratizes access to operational data across the entire team."

**[Brief pause]**

> "Under the hood, we have two specialized AI agents:
>
> The **Datadog Agent** - with 19 purpose-built tools for querying logs, analyzing traces, checking metrics, and correlating data across all three.
>
> The **Kubernetes Agent** - with 10 tools for checking pod health, reading events, inspecting deployments, and understanding cluster state.
>
> These aren't generic AI responses. Each agent has deep knowledge of our infrastructure, our service naming conventions, and our environments. They know how to translate a simple question into the right API calls and return meaningful results."

---

### 2. HOW IT WORKS (1.5-2 minutes)

**[Show: DevOps Assistant chat interface]**

> "Let me explain the architecture briefly, because this isn't just a chatbot wrapper around APIs.
>
> When you ask a question, an orchestrator analyzes your intent and routes it to the appropriate agent - or multiple agents if needed.
>
> If you ask about pods, deployments, or scaling - it uses the Kubernetes agent.
> If you ask about logs, errors, traces, or metrics - it uses the Datadog agent.
> For complex questions that span both infrastructure and observability, it coordinates both agents together."

**[Point to the chat interface]**

> "The agents are built using a multi-tool architecture. Each agent has access to specialized tools - think of them as skills.
>
> For example, the Datadog agent can:
> - Query logs with automatic time range and filter handling
> - Search traces in APM and identify slow spans
> - Fetch metrics and compare against baselines
> - Correlate errors across logs, traces, and metrics simultaneously
>
> The Kubernetes agent can:
> - List pods and their health status across namespaces
> - Read events to understand why pods are failing
> - Describe deployments, services, and configurations
> - Check resource utilization and scaling status
>
> The AI decides which tools to use based on your question. For a simple query, it might use one tool. For a full investigation, it chains multiple tools together and synthesizes the results."

**[Emphasize this point]**

> "Importantly, all responses are grounded in real data. The assistant doesn't guess or hallucinate - it queries actual systems and shows you what it found. You can see the tool calls executing in real-time, so you know exactly where the data comes from.
>
> You can also use explicit routing with @k8s or @datadog if you want to target a specific agent directly.
>
> Let me show you this in action."

---

### 3. LIVE DEMO (5 minutes)

---

#### Scenario 1: Pod Health Check (1 minute)

**[Type in the chat]**

```
Show me unhealthy pods in QA
```

**[While waiting for response]**

> "Let's start simple. I want to know if my environment is healthy.
>
> This is something a QA engineer might ask before running tests, or a developer after deploying.
>
> Behind the scenes, the Kubernetes agent is now connecting to the cluster and running health checks across all pods in the QA namespace.
>
> Normally, you'd need to run kubectl commands, filter by status, and interpret the output. Here, you just ask.
>
> Notice the streaming - you can see the agent working in real-time, showing which tools it's calling."

**[When response appears]**

> "The assistant found the unhealthy pods and shows:
> - The pod name and current status
> - What the status means - for example, OOMKilled indicates the container ran out of memory
> - Recommended next steps
>
> Anyone on the team can now check environment health in seconds."

---

#### Scenario 2: Error Log Analysis (1 minute)

**[Type in the chat]**

```
Get error logs for pricing-be in the last hour
```

**[While waiting]**

> "Now I need to find error logs. Instead of writing Datadog query syntax, I just describe what I need.
>
> The Datadog agent understands service names, time ranges, and log levels automatically. It builds the right query for you.
>
> If you've used Datadog before, you know the query syntax can be complex - especially when filtering by service, environment, and status.
>
> Here, the agent handles all of that. It knows our service naming conventions and maps 'pricing-be' to the correct Datadog service tags.
>
> Notice the streaming feedback - you can see each tool call as it executes."

**[When response appears]**

> "The assistant queried Datadog and found the errors.
>
> It shows:
> - Error types and their frequency
> - Timestamps for correlation
> - Relevant context from each log entry
>
> This would normally take several minutes navigating the Datadog UI. Now it's done in seconds."

---

#### Scenario 3: Full Investigation (2 minutes)

**[THE WOW MOMENT]**

**[Type in the chat]**

```
Investigate errors in confirmation-service with full context
```

**[While waiting - explain what's happening]**

> "This is the powerful capability.
>
> Watch what happens. The assistant will:
> - Query error logs from Datadog
> - Search for related traces in APM
> - Check service health metrics
> - Correlate everything and identify the root cause
>
> This is exactly what a senior engineer does during incident investigation - but automated."

**[Point to streaming updates as they appear]**

> "You can see the tool calls as they execute - query_logs, query_traces, get_service_health_metrics.
>
> It's running the same troubleshooting workflow we would run manually.
>
> What's important here is the correlation. The agent doesn't just fetch data - it connects the dots between logs, traces, and metrics to find patterns.
>
> For example, if errors spike at the same time latency increases, it will identify that correlation and suggest a root cause.
>
> This kind of analysis typically requires switching between multiple Datadog dashboards - Logs, APM, Metrics - and manually correlating timestamps.
>
> The agent does this automatically, in one conversation."

**[If still waiting - additional context]**

> "Each tool you see executing is a specialized capability. The Datadog agent has 19 different tools - from simple log queries to complex trace analysis and metric aggregation.
>
> It chooses which tools to use based on your question. For a full investigation like this, it uses multiple tools and synthesizes the results."

**[When response appears]**

> "Look at this response:
>
> - **Log Analysis**: Error patterns identified and categorized
> - **Trace Analysis**: Slow spans and latency breakdown
> - **Metrics**: Error rate compared to baseline
> - **Root Cause**: A clear hypothesis with supporting evidence
>
> In 90 seconds, with one question, we completed an investigation that would typically take 30 to 45 minutes.
>
> That's not incremental improvement. That's a fundamental change in how we diagnose issues."

---

#### Scenario 4: Cross-Agent Workflow (1 minute)

**[Type in the chat]**

```
pricing-be pods are crashing - investigate why
```

**[While waiting]**

> "For this query, I didn't specify which tool to use. The assistant determines that automatically.
>
> It will use both agents: Kubernetes to check pod status and events, and Datadog to find related errors and patterns."

**[When response appears]**

> "The investigation combined data from both sources:
>
> - Kubernetes shows the pods have been restarting with OOMKilled status
> - Datadog shows a memory usage pattern increasing before each crash
> - The root cause: likely a memory leak that needs code-level investigation
>
> Two agents, one conversation, complete picture."

---

### 4. CLOSING (1-1.5 minutes)

**[Show: DevOps Assistant UI]**

> "Let me summarize what we've seen today.
>
> The DevOps Assistant is an AI-powered operations tool that brings together Kubernetes and Datadog in one natural language interface."

**[Count on fingers or use visual emphasis]**

> "The key benefits:
>
> **First - Faster Troubleshooting.** Investigations that typically take 30 to 45 minutes can now be completed in under 2 minutes. We saw this in the full investigation scenario - one question, complete root cause analysis.
>
> **Second - Democratized Access.** Every team member - developers, QA, ITOps - can now query operational data without learning specialized tools. No kubectl expertise required. No Datadog query syntax to memorize.
>
> **Third - Reduced Context Switching.** Instead of jumping between Datadog Logs, APM, Metrics dashboards, and terminal windows - everything happens in one conversation. The assistant handles the tool coordination.
>
> **Fourth - Consistent Investigation Quality.** The assistant follows the same thorough investigation pattern every time - checking logs, traces, metrics, and correlating them. This ensures nothing gets missed, regardless of who's investigating."

**[Pause for emphasis]**

> "This isn't about replacing engineers. It's about amplifying their capabilities and removing friction from day-to-day operations.
>
> Senior engineers can focus on complex architectural problems instead of answering routine questions.
> Junior engineers can investigate issues independently and learn faster.
> And during incidents, everyone can contribute to diagnosis without bottlenecks."

**[Final call to action]**

> "The DevOps Assistant is available now through the Audit DevOps Portal. If you'd like a walkthrough for your team or have specific use cases you'd like to explore, reach out to the Audit DevOps team.
>
> Thank you for watching."

---

## Backup Scenarios

If any primary scenario fails, use these alternatives:

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

---

## Recording Tips

1. **Speak at a measured pace** - recordings can be sped up but not slowed down cleanly
2. **Pause after each response** - let the output fully render before continuing
3. **Highlight the streaming** - it demonstrates responsiveness
4. **Use real service names** - adds authenticity
5. **Record in segments** - easier to edit if needed
6. **Add captions in post** - improves accessibility

---

## Key Messages to Reinforce

| Audience | Primary Message |
|----------|-----------------|
| Developers | "No kubectl needed - just ask in plain English" |
| DevOps | "Full investigation in 90 seconds instead of 45 minutes" |
| ITOps | "Self-service monitoring reduces escalations" |
| QA Engineers | "Check environment health before tests in seconds" |
| Architects | "Real-time service insights from actual data" |

---

## Post-Recording

- [ ] Review recording for clarity
- [ ] Add captions/subtitles
- [ ] Share via internal channels
- [ ] Collect feedback
- [ ] Track engagement metrics
