#!/usr/bin/env python3
import sys, json
from mem0 import MemoryClient

config = json.load(open("/Users/openclaw/.openclaw/workspace/memory/mem0-config.json"))
client = MemoryClient(api_key=config["api_key"])
content = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else sys.stdin.read()
result = client.add(content, user_id=config["user_id"])
print(f"✅ Saved to Mem0: {result['results'][0]['status'] if result.get('results') else result}")
