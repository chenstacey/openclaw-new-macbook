---
name: laptop-sync
description: 在两台 Mac 之间无缝切换 OpenClaw Telegram Bot 主控权。当需要从新 MacBook (192.168.68.63) 切换到旧 MacBook 或反之时使用。触发场景：用户说"切换电脑"、"接管 Bot"、"备用电脑上线"、"停止主电脑"。
---

# Laptop Sync

两台 MacBook 共用同一个 Telegram Bot，通过 SSH 远程控制 gateway 的启停来实现无缝切换。

## 机器信息

| 机器 | IP / 主机名 | 角色 |
|------|------------|------|
| 新 MacBook | `192.168.68.63` | 主控 (默认运行 Bot) |
| 旧 MacBook | `本地运行` | 备用 (需要时接管) |

## 工作原理

```
Telegram → 路由到运行 gateway 的那台机器
```

同一时刻只有一台机器运行 gateway，避免重复回复。

## 核心脚本

### 1. 停止远程 gateway (在旧 MacBook 上执行)
```bash
ssh stacey@192.168.68.63 'openclaw gateway stop'
```

### 2. 在旧 MacBook 上启动 gateway
```bash
openclaw gateway start
```

### 3. 查看当前哪台机器在运行 gateway
```bash
ssh stacey@192.168.68.63 'openclaw gateway status' 2>/dev/null && echo "新 MacBook 运行中" || echo "新 MacBook 未运行"
```

## Bot Token 迁移

Bot Token 存储在 `~/.openclaw/gateway.json` 或 `~/.openclaw/env` 中。

**在旧 Mac 接管前，需要确保新 Mac 的 token 配置可以迁移：**

1. 登录新 Mac 的 OpenClaw Dashboard (或查看配置)
2. 获取 Bot Token
3. 在旧 Mac 的 `~/.openclaw/` 中写入相同配置

## 快速切换命令

### 切换到旧 MacBook（备用电脑接管）:
```bash
ssh stacey@192.168.68.63 'openclaw gateway stop' && openclaw gateway start
```

### 切换回新 MacBook:
```bash
openclaw gateway stop && ssh stacey@192.168.68.63 'openclaw gateway start'
```

## 同步工作区文件 (GitHub)

每次切换后，建议同步最新文件：

```bash
# 拉取最新配置
git pull origin main

# 工作完成后提交更改
git add -A && git commit -m "sync" && git push
```

## 安全说明

- SSH 需要在两台机器上启用 (系统设置 → 通用 → 共享 → 远程登录)
- `.openclaw/` 目录不提交到 GitHub（包含 Bot Token）
- 建议定期确保两台机器的 OpenClaw 版本一致
