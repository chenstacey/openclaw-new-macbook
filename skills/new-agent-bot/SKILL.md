---
name: new-agent-bot
description: Create a new OpenClaw sub-agent with a dedicated Telegram bot. Use when the user wants to add a new specialized bot (e.g., "create a new bot for X", "set up a new agent for Y", "add another bot"). Handles full setup: agent creation, workspace files, openclaw.json config update, bindings, and gateway restart.
---

# New Agent Bot

Creates a fully configured OpenClaw sub-agent with a dedicated Telegram bot account.

## Prerequisites

User must provide:
1. **Bot token** — from Telegram BotFather (`/newbot`)
2. **Agent purpose** — what the bot specializes in (e.g., "real estate", "fitness", "travel")

## Process

### Step 1: Choose IDs

- `agentId` — hyphen-case, e.g. `hk-apartment-analyst`
- `accountId` — snake_case, e.g. `real_estate`
- `workspacePath` — `~/.openclaw/workspace-<agentId>`

### Step 2: Create Agent via CLI

```bash
openclaw agents add <agentId>
# When prompted for workspace, enter the workspacePath above
# When prompted for identity name/emoji, set appropriately
```

### Step 3: Set Identity

```bash
openclaw agents set-identity <agentId> --name "<Display Name>" --emoji <emoji>
```

### Step 4: Create Workspace Files

Create these files in `~/.openclaw/workspace-<agentId>/`:

- `IDENTITY.md` — name, creature, vibe, emoji
- `SOUL.md` — personality, tone, domain focus
- `USER.md` — who Sisi is, her timezone, context
- `AGENTS.md` — specialization, behavior, memory guidelines
- `MEMORY.md` — long-term memory seed for the domain
- `memory/` — directory for daily notes

See `references/workspace-templates.md` for file templates.

### Step 5: Update openclaw.json

File: `~/.openclaw/openclaw.json`

Add new account under `channels.telegram.accounts`:
```json
"<accountId>": {
  "botToken": "<BOT_TOKEN>",
  "dmPolicy": "pairing"
}
```

Add new binding under `bindings` array:
```json
{
  "agentId": "<agentId>",
  "match": {
    "channel": "telegram",
    "accountId": "<accountId>"
  }
}
```

### Step 6: Restart Gateway

```bash
openclaw gateway restart
```

### Step 7: Verify

```bash
openclaw status --deep
```

Confirm the new bot appears under Health > Telegram with `ok` status.

### Step 8: Pairing

The new bot uses `dmPolicy: pairing`. User must send a message to the new bot, then:
```bash
openclaw pairing list --channel telegram
openclaw pairing approve telegram <CODE>
```

## Health Check & Auto-Fix

Use when: bots are not responding, messages not getting through, or after config changes.

Triggers: "check if my bots are working", "why isn't the bot responding", "fix my bots", "agents not responding".

### Quick Check
Run `scripts/check_agents.sh` — checks gateway, channel status, and Telegram API response for each bot.

```bash
bash ~/.openclaw/workspace/skills/new-agent-bot/scripts/check_agents.sh
```

### Auto-Fix
Run `scripts/fix_agents.sh` — tries progressive fixes:
1. Gateway restart
2. Stop/start cycle
3. Validate `openclaw.json` config
4. Test each bot token via Telegram API

```bash
bash ~/.openclaw/workspace/skills/new-agent-bot/scripts/fix_agents.sh
```

### Manual Diagnosis Steps (if scripts don't fix it)

1. **Check gateway:** `openclaw gateway status`
2. **Deep probe:** `openclaw status --deep` — look for each bot under Health > Telegram
3. **Check pairing:** `openclaw pairing list --channel telegram` — unpaired users get no response
4. **Approve pairing:** `openclaw pairing approve telegram <CODE>`
5. **Validate token:** `https://api.telegram.org/bot<TOKEN>/getMe`
6. **Check logs:** `openclaw logs | grep -i telegram`

### Common Issues & Fixes

| Symptom | Likely Cause | Fix |
|---|---|---|
| Bot shows `ok` in status but no response | Pairing not approved | `openclaw pairing approve telegram <CODE>` |
| Bot not showing in `status --deep` | Gateway not loaded with new config | `openclaw gateway restart` |
| Bot token invalid | Wrong token in config | Re-check `openclaw.json` accounts |
| Main bot stopped after adding new bot | Config conflict | Ensure no duplicate `botToken` at top level |
| All bots down | Gateway crashed | `openclaw gateway stop && openclaw gateway start` |

## Notes

- Each agent has fully isolated workspace, memory, and session history
- Bindings route inbound messages by `accountId` (which bot received the message)
- The `main` agent always keeps its existing binding — never remove it
- After restart, both old and new bots should show as `ok` in `openclaw status --deep`
- Read `references/workspace-templates.md` for the file content templates
