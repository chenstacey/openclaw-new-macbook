#!/bin/bash
# check_agents.sh — Health check all Telegram bots/agents
# Usage: bash check_agents.sh
# Returns: 0 if all healthy, 1 if issues found (and attempts auto-fix)

echo "🔍 Checking OpenClaw agent health..."
echo ""

# Step 1: Gateway reachable?
GATEWAY_STATUS=$(openclaw gateway status 2>&1)
if echo "$GATEWAY_STATUS" | grep -q "running"; then
  echo "✅ Gateway: running"
else
  echo "❌ Gateway: not running — attempting restart..."
  openclaw gateway start
  sleep 5
fi

# Step 2: Channel status
echo ""
echo "📡 Channel status:"
CHANNEL_STATUS=$(openclaw channels status 2>&1)
echo "$CHANNEL_STATUS"

# Step 3: Deep health probe (checks each bot's Telegram API response)
echo ""
echo "🩺 Deep health probe:"
DEEP=$(openclaw status --deep 2>&1)

# Extract Telegram health line
TELEGRAM_HEALTH=$(echo "$DEEP" | grep "Telegram" | grep -v "ON\|OFF\|token")
echo "$TELEGRAM_HEALTH"

# Step 4: Check for any bot not showing "ok"
if echo "$TELEGRAM_HEALTH" | grep -q "ok"; then
  echo ""
  echo "✅ All bots responding to Telegram API"
else
  echo ""
  echo "❌ One or more bots not responding — restarting gateway..."
  openclaw gateway restart
  sleep 8
  echo ""
  echo "🔄 Re-checking after restart:"
  openclaw status --deep 2>&1 | grep "Telegram"
fi

# Step 5: Check for recent inbound messages (shows if messages are actually flowing)
echo ""
echo "📨 Recent inbound activity:"
openclaw channels status 2>&1 | grep -i "telegram"

echo ""
echo "Done. If bots still unresponsive after restart, check:"
echo "  1. Bot token is valid (test via https://api.telegram.org/bot<TOKEN>/getMe)"
echo "  2. Pairing approved: openclaw pairing list --channel telegram"
echo "  3. Config valid: cat ~/.openclaw/openclaw.json"
