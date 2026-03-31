---
name: mirofish-research
description: "End-to-end scenario simulation using MiroFish. Use when asked to simulate, model, or war-game a geopolitical/economic scenario (e.g. 'simulate Iran war impact on China', 'model what happens if...'). Automatically runs deep research, builds seed data with multi-agent roles, calls MiroFish API to launch simulation, monitors progress, and delivers a structured report. Requires MiroFish running at localhost:5001."
---

# MiroFish Research Skill

Automate the full pipeline: research → seed → simulate → report.

## Prerequisites

MiroFish must be running. Check first:
```bash
curl -s http://localhost:5001/health
```
If not running: `cd ~/clawd-projects/MiroFish && npm run dev`

## Full Pipeline

### Step 1: Research Phase
Use `brave-search` + `web-content-fetcher` to gather key facts, data, expert analysis.
- 3-5 sources minimum, focus on quantitative data
- Save findings to `/tmp/mirofish-seed.txt`

### Step 2: Build Seed File

Write to `/tmp/mirofish-seed.txt`:
```
【现实背景】
<key facts, data, current situation>

【参与角色】（5-8 具名角色，不同立场/行业）
1. <Name> - <Role/Title>, <interests/pressures>
2. ...

【核心事件】
<What triggered the scenario, what changes>
```

Role design: each role needs conflicting interests. Mix policy makers, industry players, financiers, intermediaries.

### Step 3: Run Automation Script

```bash
python3 ~/.openclaw/workspace/skills/mirofish-research/scripts/run_simulation.py \
  --seed /tmp/mirofish-seed.txt \
  --prompt "模拟[N]个参与者在[事件]背景下的决策互动。重点观察：策略、传导链、受益/受损、政策空间、最终均衡" \
  --name "scenario-name" \
  --rounds 10
```

### Step 4: Deliver Report

The script outputs findings. Format as structured analysis and send to user.
If report is truncated (tool call limit hit), reduce `--rounds` to 6-8.

## Common Issues

| Issue | Fix |
|-------|-----|
| Only 1 agent generated | Seed lacks role diversity → rewrite with explicit named characters |
| Network Error on load | Backend crashed → restart MiroFish |
| Tool call limit / truncated report | Reduce `--rounds` to 6-8 |
| Zep 401 | Check ZEP_API_KEY in ~/clawd-projects/MiroFish/.env |

## Config Reference

- `.env`: `~/clawd-projects/MiroFish/.env`
- LLM: MiniMax-M2.1 via `api.minimax.io`
- Memory: Zep Cloud (graph memory)
- Default max rounds: 10 (set via OASIS_DEFAULT_MAX_ROUNDS)
