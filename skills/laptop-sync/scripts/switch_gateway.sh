#!/bin/bash
# switch_gateway.sh - 在两台 Mac 之间切换 OpenClaw Telegram Bot 主控权
# 用法: ./switch_gateway.sh [new|old]

set -e

NEW_MAC="stacey@192.168.68.63"
CURRENT_HOST=$(hostname)

switch_to_new() {
    echo "=== 切换到新 MacBook (192.168.68.63) ==="
    if [[ "$CURRENT_HOST" == *"Air"* ]]; then
        echo "停止本地 gateway..."
        openclaw gateway stop 2>/dev/null || true
    fi
    echo "在新 MacBook 上启动 gateway..."
    ssh "$NEW_MAC" 'openclaw gateway start'
    echo "✅ 切换完成 - Bot 现在运行在新 MacBook"
}

switch_to_old() {
    echo "=== 切换到旧 MacBook (本地) ==="
    echo "停止新 MacBook 上的 gateway..."
    ssh "$NEW_MAC" 'openclaw gateway stop' 2>/dev/null || true
    echo "启动本地 gateway..."
    openclaw gateway start
    echo "✅ 切换完成 - Bot 现在运行在旧 MacBook"
}

STATUS_NEW=$(ssh "$NEW_MAC" 'openclaw gateway status' 2>/dev/null | grep -c "running\|started\|active" || echo "0")

show_status() {
    echo "=== 当前 Bot 状态 ==="
    if [[ "$CURRENT_HOST" == *"Air"* ]]; then
        LOCAL=$(openclaw gateway status 2>/dev/null | grep -c "running\|started\|active" || echo "0")
        if [[ "$LOCAL" -gt 0 ]]; then
            echo "🟢 Bot 运行在: 本地 (旧 MacBook)"
        else
            echo "⚪ Bot 未运行 (本地)"
        fi
    fi
    if [[ "$STATUS_NEW" -gt 0 ]]; then
        echo "🟢 Bot 运行在: 新 MacBook (192.168.68.63)"
    else
        echo "⚪ Bot 未运行 (新 MacBook)"
    fi
}

case "$1" in
    new) switch_to_new ;;
    old) switch_to_old ;;
    status) show_status ;;
    *)
        echo "用法: $0 [new|old|status]"
        echo "  new   - 切换到新 MacBook"
        echo "  old   - 切换到旧 MacBook"
        echo "  status - 查看当前状态"
        ;;
esac
