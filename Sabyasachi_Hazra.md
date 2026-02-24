Role: Agent Logic & Stability Scoring Architect

Responsible Files:

agent/scoring.py
agent/decision.py
agent/agent_loop.py
storage/database.py

Core Responsibilities:

Design weighted Concept Stability Index
Implement rule-based threshold logic
Control adaptive decision making
Integrate entire evaluation pipeline
Store results in SQLite

Must Understand:

Why scoring is heuristic
Why adaptation is rule-based
How deterministic logic controls the agent

How It Connects:

Central brain of system. Calls embedding → scoring → decision → possibly re-calls question_generator.

Issues faced during implementation: