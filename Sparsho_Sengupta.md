Role: Embedding & Semantic Consistency Engineer

Responsible Files:

llm/embeddings.py

Core Responsibilities:

Implement embedding API calls
Convert responses to vector representations
Compute cosine similarity using NumPy
Return semantic similarity score

Must Understand:

What embeddings represent
Why cosine similarity measures semantic closeness
How low similarity implies conceptual instability

How It Connects:

agent_loop.py passes user answers → embeddings.py returns similarity score → scoring.py consumes it.