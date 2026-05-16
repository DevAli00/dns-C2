# dns-c2

An educational DNS-based research framework for studying encrypted message transport, task coordination, and detection in controlled lab environments.

> ⚠️ **Disclaimer:** This project is intended only for authorized research, defensive analysis, and private lab environments. Do not use it on systems, networks, or accounts you do not own or do not have explicit written permission to test.

## Purpose

This project is designed to help study:

- DNS message encoding and transport constraints
- Encrypted payload handling with authenticated encryption
- Lightweight task coordination across processes
- State persistence for distributed lab experiments
- Detection opportunities for DNS-based covert channels

## Architecture

```text
Operator / Controller
	↓
Task Engine
	↓
queue_store.py → session and task persistence
	↓
server.py → DNS listener and message router
	↕ DNS-based transport
agent.py → Lab client that exchanges encrypted messages
```

## Features

- DNS-based message transport for lab research
- AES-256-GCM encryption for payload protection
- ReAct-style reasoning loop for task selection and follow-up planning
- JSON-backed session state for simple persistence
- Protocol-aware handling of DNS length limits
- Pure Python implementation for local experimentation

## LLM Orchestration

The LLM component acts as the planning layer for the lab workflow. It reads the current session state, summarizes recent results, and proposes the next safe action based on the observed history.

In practice, that means it can:

- Rank candidate tasks from the current session history
- Turn raw observations into short summaries
- Decide when a session should stop, continue, or be reviewed manually
- Keep the workflow consistent across multiple runs without manual bookkeeping

This automation is useful for research because it reduces repetitive operator work while preserving a clear audit trail in `sessions.json`.

## Prerequisites

- Python 3.12+
- A local LLM runtime if you want to use the reasoning loop
- A controlled lab network
- Basic Python and networking knowledge

## Project Layout

```text
dns-c2/
├── server.py
├── agent.py
├── queue_store.py
├── react_engine.py
├── crypto.py
├── sessions.json
├── README.md
└── requirements.txt
```

## How It Works

1. A controller selects a task for a lab session.
2. The task engine records state in `sessions.json`.
3. The server exchanges encrypted DNS messages with the lab client.
4. The client processes the task in the authorized test environment.
5. Results are returned and stored for later analysis.
6. The reasoning loop updates the next task based on prior outcomes.

## Safety and Scope

This project must only be used:

- In isolated labs
- On systems you own or are explicitly authorized to test
- For defensive research, training, or detection engineering
- With clear written approval and scope limits

It must not be used for unauthorized access, persistence, stealth, malware deployment, credential theft, or evasion.

## Learning Goals

This repository is useful for understanding:

- DNS-based covert channel mechanics
- Encryption and message authentication
- Distributed task flow design
- State synchronization between processes
- Defensive monitoring and detection strategies

## Next Steps

Safe follow-up work for this project:

- Add stronger validation around session inputs and message sizes
- Expand tests for encryption, persistence, and task routing
- Improve logging so lab runs are easier to audit
- Document detection ideas for defenders and blue teams
- Refine the LLM prompts so task selection stays predictable and reviewable


