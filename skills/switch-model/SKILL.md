---
name: switch-model
description: "Switch the active AI model. Use when: user says 'switch to kimi', 'use gemini', 'switch model', 'change model', 'switch to gemini flash', 'use kimi code', or any natural language request to change the AI model."
metadata: { "openclaw": { "emoji": "🔄" } }
---

# Switch Model Skill

Switch the active AI model using natural language.

## Available Models

| Name | Model ID |
|------|----------|
| Kimi / Kimi Code | `kimi-coding/k2p5` |
| Gemini / Gemini Flash | `google-gemini/gemini-2.0-flash` |

## How to Switch

Use the `exec` tool to run the switch command, then restart the gateway:

### Switch to Kimi
```bash
openclaw models set kimi-coding/k2p5
```

### Switch to Gemini Flash
```bash
openclaw models set google-gemini/gemini-2.0-flash
```

After switching, run:
```bash
openclaw gateway restart
```

## Examples

- "switch to kimi" → set `kimi-coding/k2p5`
- "switch to gemini" → set `google-gemini/gemini-2.0-flash`
- "use gemini flash" → set `google-gemini/gemini-2.0-flash`
- "switch model kimi" → set `kimi-coding/k2p5`
- "what model am i using?" → run `openclaw models status` and report back

## After Switching

Always confirm to the user which model is now active.
