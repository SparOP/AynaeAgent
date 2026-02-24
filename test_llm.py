# test_llm.py

from llm.reference_generator import build_reference
from llm.question_generator import generate_question

topic = "Recursion"

print("\n=== REFERENCE ===")
print(build_reference(topic))

print("\n=== NORMAL ===")
print(generate_question(topic, "normal"))

print("\n=== REFRAMED ===")
print(generate_question(topic, "reframed"))

print("\n=== FUNDAMENTAL ===")
print(generate_question(topic, "fundamental_probe"))

print("\n=== ADVANCED ===")
print(generate_question(topic, "advanced"))