# AutoSRE
## Autonomous Ops Agent

## Overview

Autonomous Ops Agent is a GenAI-powered, policy-constrained operations system that **detects infrastructure anomalies, reasons about corrective actions, and executes safe self-healing workflows** with full observability and auditability.

---
## Live Demo: "https://autonomous-sre-agent.streamlit.app/"
---

## Problem Statement

Modern infrastructure failures (e.g., CPU saturation) are detected quickly but often require **manual triage and intervention**, increasing Mean Time To Recovery (MTTR).

This project demonstrates how **agentic AI** can:

* Reduce MTTR
* Enforce safety constraints
* Provide explainable, auditable decisions

---

## Architecture

Monitor → Diagnose → Decide (LLM + Safety) → Act → Verify → Report

* LangGraph for agent state transitions
* LLM Reasoning for decision justification
* Safety Layer to prevent unsafe actions
* Human-readable audit trail for every incident

---


## Safety & Guardrails

* Confidence thresholds for actions
* Failure memory to prevent infinite loops
* Escalation after repeated failures
* Deterministic overrides over LLM output

---

## Observability

* Prometheus for metrics
* Incident logs (JSONL)
* Streamlit Ops Dashboard

---

## Dashboard

The dashboard provides:

* Current system state
* Incident history
* Success rate
* Average CPU reduction
* Dark/light theme switching

---

## Tech Stack

* Python
* Docker & Docker Compose
* Prometheus
* LangGraph
* Gemini / LLM API
* Streamlit

---

## Key Design Decisions

* **LLM is advisory, not authoritative**
* **Rules override AI for safety**
* **Explainability over blind automation**

---

## Results

* Demonstrated automated CPU recovery
* Reduced simulated MTTR significantly
* Zero unsafe actions executed

---

## Future Work

* Multi-metric reasoning (memory, disk)
* Horizontal scaling actions
* PagerDuty / Slack escalation
* Kubernetes-native deployment

---

## How to Run

```bash
docker compose up
python -m core.runner
streamlit run frontend/dashboard.py
```
