# Healthcare Appeals Decisioning
A governed agentic AI application for evaluating healthcare insurance appeals using multimodal evidence, deterministic governance rules, and Human-in-the-Loop escalation.

# Responsibilities
- Ingest structured appeal cases (documents and images)
- Evaluate medical necessity using LLM reasoning
- Detect evidence inconsistencies (e.g. patient identity mismatch)
- Enforce deterministic governance rules
- Escalate high-risk cases for human review
- Produce auditable, replayable outputs

# Why LangGraph
LangGraph is used to orchestrate agent execution as an explicit decision graph.
LangGraph Enables
- Deterministic execution order
- Stateful agent coordination
- Conditional branching (approve vs escalate)
- Human-in-the-Loop interruption points
- Replayable decision paths

This is critical for regulated decisioning systems where control flow must be explicit and auditable.

# Architecture
Case Input
  └─► Intake Agent
        └─► Reasoning Agent (LLM)
              └─► Decision Agent (Hard Rules)
                    └─► Governance Agent
                          ├─► Human Review Queue (if ESCALATE)
                          └─► Final Decision

# Case Definitions

Each JSON file represents a single healthcare appeal case.

**Case Responsibilities**

1. Reference documents and images
2. Define appeal context
3. Provide control inputs (urgency, procedure)

**Important Notes**

1. Case files do not contain raw document text
2. All referenced paths are relative to the data folder
3. Cases are deterministic and replayable

**Governance Rules**

1. If evidence inconsistency is detected → decision must be ESCALATE
2. Auto-approval is allowed only when evidence is consistent
3. Escalated cases require human review before final disposition

**Human-in-the-Loop (HITL)**

1. Escalated cases are placed in a review queue: `outputs/hitl_queue/<case_id>.json`

Human reviewers can:

1. Approve
2. Deny
3. Request additional information

All actions are audit-logged.

# Outputs

outputs/
├── runs/
├── hitl_queue/
└── audit/

**Outputs are deterministic, timestamped, and auditable.**

# Use Cases

- Healthcare insurance appeals
- Prior authorization reviews
- Medical necessity determination
- Policy-driven decision governance

# Design Principles

- Separate reasoning from governance
- Deterministic control over probabilistic models
- Human oversight for high-risk decisions
- Auditability by default

# Key Takeaway

This application demonstrates how agentic AI can be safely deployed in regulated environments by combining LLM reasoning with explicit governance and human oversight.