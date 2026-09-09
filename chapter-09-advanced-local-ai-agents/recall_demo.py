# recall_demo.py
# Demonstrates recalling prior agent research from persistent memory.

from agent_memory import AgentMemory

memory = AgentMemory()
past_findings = memory.recall("local AI privacy", top_k=3)

for finding in past_findings:
    print(finding)
