---
name: mem0-memory
description: Mem0 智能记忆层。在每次对话中自动保存重要记忆，并在回答前语义搜索相关记忆。解决 Episodic Memory（事件记忆）和 External Memory（语义检索）两个痛点。
---

# Mem0 Memory Skill

## 配置

- **API Key:** 存储在 `~/.openclaw/workspace/memory/mem0-config.json`
- **User ID:** `sisi`
- **SDK:** `mem0ai` (pip3 install mem0ai)

## 何时使用

### 1. 保存记忆（会话中学到新东西时）
```python
python3 ~/.openclaw/workspace/skills/mem0-memory/scripts/mem0_add.py "<内容>"
```

### 2. 搜索记忆（回答问题前查询相关背景）
```python
python3 ~/.openclaw/workspace/skills/mem0-memory/scripts/mem0_search.py "<查询>"
```

### 3. 自动会话摘要（会话结束时）
```python
python3 ~/.openclaw/workspace/skills/mem0-memory/scripts/mem0_session_save.py "<摘要>"
```

## 使用频率控制（月 1000 次上限）

**预算分配：**
- 每天 save: 最多 3 次（~90次/月）
- 每天 search: 最多 5 次（~150次/月）
- 月均使用约 240 次，远低于 1000 次上限

**保存（save）— 只在以下情况触发：**
- 用户明确说"记住这个"
- 重大决定或配置变更（新安装、新设置）
- 用户纠正了我（学习教训）
- 每日会话总结（每天最多1次，在 nightly-memory-update cron 里）

**❌ 不保存：**
- 普通问答、日常闲聊
- 已在 MEMORY.md 有记录的内容（避免重复）
- 临时任务结果

**搜索（search）— 只在以下情况触发：**
- 用户问"你还记得..."或引用历史
- 新会话开始时，主题涉及过去讨论过的项目
- 需要判断某件事是否已做过

**❌ 不搜索：**
- 每条消息都查（最浪费）
- MEMORY.md 已能覆盖的基础信息
- 简单、明显的问题

## 与现有记忆系统的关系

| 系统 | 用途 | Mem0 补充 |
|------|------|-----------|
| MEMORY.md | 长期策划记忆 | Mem0 = 自动、细粒度 |
| memory/YYYY-MM-DD.md | 日志 | Mem0 = 可语义搜索 |
| knowledge/ | 原则/技能 | 不替代 |

## 免费额度

Mem0 free tier: 1000次操作/月，足够日常使用
