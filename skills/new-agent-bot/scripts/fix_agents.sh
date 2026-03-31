#!/bin/bash
# fix_agents.sh — Attempt full auto-fix of unresponsive Telegram bots
# Usage: bash fix_agents.sh
# Tries progressively harder fixes until bots respond

echo "🔧 Running full agent auto-fix..."
echo ""

FIXED=false

# Fix 1: Restart gateway
echo "▶ Fix 1: Restarting gateway..."
openclaw gateway restart
sleep 8

HEALTH=$(openclaw status --deep 2>&1 | grep "Telegram" | grep -v "ON\|OFF\|token")
echo "$HEALTH"
if echo "$HEALTH" | grep -q "ok"; then
  echo "✅ Fix 1 worked — bots responding after gateway restart"
  FIXED=true
fi

# Fix 2: Stop + start (harder reset)
if [ "$FIXED" = false ]; then
  echo ""
  echo "▶ Fix 2: Stop/start cycle..."
  openclaw gateway stop
  sleep 5
  openclaw gateway start
  sleep 10

  HEALTH=$(openclaw status --deep 2>&1 | grep "Telegram" | grep -v "ON\|OFF\|token")
  echo "$HEALTH"
  if echo "$HEALTH" | grep -q "ok"; then
    echo "✅ Fix 2 worked — bots responding after stop/start"
    FIXED=true
  fi
fi

# Fix 3: Validate config
if [ "$FIXED" = false ]; then
  echo ""
  echo "▶ Fix 3: Validating openclaw.json..."
  python3 -c "
import json, sys
try:
    with open('$HOME/.openclaw/openclaw.json') as f:
        cfg = json.load(f)
    accounts = cfg.get('channels', {}).get('telegram', {}).get('accounts', {})
    bindings = cfg.get('bindings', [])
    print(f'  Telegram accounts: {list(accounts.keys())}')
    print(f'  Bindings: {[b[\"agentId\"] for b in bindings if b.get(\"match\",{}).get(\"channel\")==\"telegram\"]}')
    # Check each account has a botToken
    for name, acct in accounts.items():
        if not acct.get('botToken'):
            print(f'  ❌ Account \"{name}\" missing botToken!')
            sys.exit(1)
    print('  ✅ Config looks valid')
except json.JSONDecodeError as e:
    print(f'  ❌ JSON parse error: {e}')
    sys.exit(1)
"
fi

# Fix 4: Validate each bot token via Telegram API
if [ "$FIXED" = false ]; then
  echo ""
  echo "▶ Fix 4: Testing bot tokens via Telegram API..."
  python3 -c "
import json, urllib.request, urllib.error

with open('$HOME/.openclaw/openclaw.json') as f:
    cfg = json.load(f)

accounts = cfg.get('channels', {}).get('telegram', {}).get('accounts', {})
for name, acct in accounts.items():
    token = acct.get('botToken', '')
    try:
        url = f'https://api.telegram.org/bot{token}/getMe'
        with urllib.request.urlopen(url, timeout=10) as r:
            data = json.loads(r.read())
            if data.get('ok'):
                bot = data['result']
                print(f'  ✅ {name}: @{bot[\"username\"]} — token valid')
            else:
                print(f'  ❌ {name}: Telegram returned not-ok')
    except urllib.error.HTTPError as e:
        print(f'  ❌ {name}: HTTP {e.code} — token may be invalid')
    except Exception as e:
        print(f'  ❌ {name}: {e}')
"
fi

# Final status
echo ""
echo "📋 Final status:"
openclaw channels status 2>&1 | grep -i telegram

if [ "$FIXED" = false ]; then
  echo ""
  echo "⚠️  Auto-fix could not fully resolve the issue."
  echo "Manual steps to try:"
  echo "  1. Verify bot token: https://api.telegram.org/bot<TOKEN>/getMe"
  echo "  2. Check pairing: openclaw pairing list --channel telegram"
  echo "  3. Re-approve pairing: openclaw pairing approve telegram <CODE>"
  echo "  4. Check logs: openclaw logs | grep -i telegram"
fi
