# ADR-001: Bounded LangGraph orchestration

Status: Proposed
Version: 1.0
Last Updated: 2026-10-14
Applicability: M03 graph
Acceptance Readiness: Blocked by OQ-009 and graph/state coordination review.

- ID: ADR-001
- Date: 2026-10-07
- Related requirements: FR-OBS-002, FR-AI-001, FR-AI-003
- Supersedes: None
- Superseded by: None
- Decision owner: Product owner; acceptance pending.

## Context
The complete analysis requires conditional stages, recoverable model failures and durable human review. The first deterministic slice does not require an orchestration framework.

## Decision
Propose LangGraph for M03 onward, with explicit typed state and bounded node transitions specified in graph-spec.md. Keep business rules in Domain/Application. No generic planner, supervisor or multi-agent graph.

## Alternatives
Ordinary application functions are simpler and selected for M02. A custom persistent state machine avoids framework coupling but adds recovery machinery. Autonomous agents increase nondeterminism without a demonstrated need.

## Consequences
Checkpoint schema compatibility and replay become explicit responsibilities. Validate crash/restart and interrupt behavior before accepting the adapter implementation. Package versions and checkpointer integration remain deferred to the approved slice. Graph state is not the audit record.
