"""
Run once to push your prompts into Langfuse.
After this, edit prompts in the Langfuse UI without touching code.

Usage: python push_prompts.py
"""
from dotenv import load_dotenv
load_dotenv()

from langfuse import Langfuse
from src.prompt import llm_call_1, llm_call_2, llm_call_3

langfuse = Langfuse()

prompts = [
    ("generate-api-docs",          llm_call_1),
    ("generate-architecture-docs", llm_call_2),
    ("generate-ui-docs",           llm_call_3),
]

for name, template in prompts:
    langfuse.create_prompt(
        name=name,
        prompt=template,
        labels=["production"],
        config={"model": "gemini-1.5-flash", "temperature": 0}
    )
    print(f"✓ pushed: {name}")

langfuse.flush()
print("\nDone. Edit them at https://us.cloud.langfuse.com → Prompts")
