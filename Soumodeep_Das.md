Role: LLM & Prompt Engineering Lead

Responsible Files:

llm/question_generator.py
llm/reference_generator.py
app.py

Core Responsibilities:

Design structured prompt templates
Implement dynamic prompt builder
Integrate Gemini API calls
Handle fallback question logic
Ensure proper reframing (definition, analogy, application)

Must Understand:

How dynamic prompting works
Why structured templates prevent hallucination
How mode (normal/deeper_probe/advanced) modifies question generation

How It Connects:

app.py calls question_generator → returns question → passed to user → then evaluation continues.

Issues faced during implementation:
