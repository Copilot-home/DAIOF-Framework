# Agent Broker (local enforcement)

Purpose
-------
This broker enforces that local AI agents running on the machine are registered and verified in the Meta‑Pool registry before they are allowed to execute. It is a lightweight, enforceable gate for local execution.

Usage
-----
Create a metadata JSON for your agent (example `agent_meta.json`) with fields `machine_ack`, `header.meta.attribution`, etc.

Run:

```bash
python3 agent_broker.py --metadata agent_meta.json -- python3 my_agent.py
```

Environment
-----------
- `OSLF_ALLOW_UNREGISTERED=1` to bypass registry checks in development (not recommended for production).

Notes
-----
- Broker expects a `MetaPoolManager` import to be available for production registry checks. If not available and bypass is not set, the broker will refuse to run agents.
