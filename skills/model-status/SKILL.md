---
name: model-status
description: "Check AI model status, cooldowns, and switch the active model. Use when: user says 'model status', 'check models', 'which model', 'model health', 'clear cooldowns', 'clear model cooldown', 'switch to kimi', 'switch to minimax', 'switch to claude', 'switch to aliyun', 'switch to gemini', 'use kimi', 'use claude', 'models not working'."
metadata: { "openclaw": { "emoji": "🔀" } }
---

# Model Status Skill

Check the current model chain, rate limit cooldowns, and switch models — all from Telegram.

## Commands

### Check status
```bash
python3 ~/clawd-projects/model-status.py
```

### Clear all cooldowns
```bash
python3 ~/clawd-projects/model-status.py clear
```

### Switch primary model
```bash
python3 ~/clawd-projects/model-status.py switch kimi
python3 ~/clawd-projects/model-status.py switch minimax
python3 ~/clawd-projects/model-status.py switch claude
python3 ~/clawd-projects/model-status.py switch aliyun
python3 ~/clawd-projects/model-status.py switch gemini
```

## Trigger phrases → action

| User says | Action |
|-----------|--------|
| "model status" / "check models" / "which model" | Run status check |
| "clear cooldowns" / "models not working" | Run clear |
| "switch to kimi" / "use kimi" | Run switch kimi |
| "switch to minimax" / "use minimax" | Run switch minimax |
| "switch to claude" / "use claude" | Run switch claude |
| "switch to aliyun" | Run switch aliyun |
| "switch to gemini" | Run switch gemini |

## Output format

Status uses emoji indicators:
- ✅ = model ready
- ⏳ Xm Ys = in rate limit cooldown, X minutes Y seconds remaining

Always run the script and return its output directly to the user. Do not add extra commentary.
