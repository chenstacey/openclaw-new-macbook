# openclaw-sync Skill

用 GitHub 同步 OpenClaw 配置到新 MacBook。

## 触发词
"同步配置", "sync config", "push config", "保存配置"

## 同步什么

| 路径 | 内容 |
|------|------|
| `~/.openclaw/agents/*/agent/` | AGENTS.md, SOUL.md, models.json |
| `~/.openclaw/workspace/skills/` | 所有 skill 的 SKILL.md + scripts |
| `~/clawd-projects/` | 脚本和项目（MiroFish 等） |
| `~/.openclaw/cron/jobs.json` | Cron 任务配置 |

## 不同步（secrets）
- `auth-profiles.json` / `openclaw.json`（含 API keys）
- `sessions/` / `sessions.json`
- `media/` / `inbound/` / `cache/`
- `.env` 文件

## 执行

```bash
SYNC=~/openclaw-sync
OC=~/.openclaw
PROJ=~/clawd-projects

# Sync agents
for agent_dir in $OC/agents/*/agent; do
    agent_name=$(basename $(dirname $agent_dir))
    dest="$SYNC/agents/$agent_name"
    mkdir -p "$dest"
    for f in AGENTS.md SOUL.md models.json agent.json; do
        [ -f "$agent_dir/$f" ] && cp "$agent_dir/$f" "$dest/$f"
    done
done

# Sync skills (SKILL.md + scripts/ + data/)
for skill_dir in $OC/workspace/skills/*/; do
    skill_name=$(basename $skill_dir)
    dest="$SYNC/skills/$skill_name"
    mkdir -p "$dest"
    cp "$skill_dir/SKILL.md" "$dest/" 2>/dev/null
    [ -d "$skill_dir/scripts" ] && cp -r "$skill_dir/scripts" "$dest/"
    [ -d "$skill_dir/data" ] && cp -r "$skill_dir/data" "$dest/"
done

# Sync clawd-projects
rsync -av --exclude='node_modules/' --exclude='backend/uploads/simulations/' \
    --exclude='*.env' --exclude='.DS_Store' --exclude='package-lock.json' \
    $PROJ/ "$SYNC/clawd-projects/" 2>/dev/null | tail -1

# Sync cron
[ -f $OC/cron/jobs.json ] && cp $OC/cron/jobs.json "$SYNC/cron/jobs.json"

# Git commit & push
cd "$SYNC"
git add .
git commit -m "sync $(date +%Y-%m-%d\ %H:%M)" 2>/dev/null || echo "No changes to commit"
TOKEN=$(gh auth token)
git remote set-url origin "https://x-access-token:${TOKEN}@github.com/chenstacey/openclaw-config.git"
git push 2>/dev/null || echo "Push failed"
```

## 输出
成功：✅ 已同步到 GitHub
无变化：⏭️ 无需同步
失败：❌ + 错误原因

## 规则
每次 OpenClaw 配置变更后 **立即执行**，不要等。
