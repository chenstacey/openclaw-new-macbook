#!/usr/bin/env python3
import sys, json
from mem0 import MemoryClient

config = json.load(open("/Users/openclaw/.openclaw/workspace/memory/mem0-config.json"))
client = MemoryClient(api_key=config["api_key"])
query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else sys.stdin.read()
results = client.search(query, user_id=config["user_id"], filters={"user_id": config["user_id"]})
memories = results.get("results", [])
if not memories:
    print("No relevant memories found.")
else:
    for m in memories:
        score = m.get("score", 0)
        print(f"[{score:.2f}] {m['memory']}")
