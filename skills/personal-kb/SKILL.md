---
name: personal-kb
description: Personal knowledge base with RAG (Retrieval-Augmented Generation). Ingest URLs from Telegram topics including articles, YouTube videos (with Whisper transcription), X/Twitter threads (full threads), and PDFs. Extract entities (people, companies, concepts). Store in Obsidian. Support natural language queries with semantic search, time-aware ranking, and source-weighted ranking. Use browser automation for paywalled content. Triggers on URLs dropped in Telegram, queries about knowledge base, or commands like "search my notes", "what do I know about X".
---

# Personal Knowledge Base with RAG

Build and query a personal knowledge base from ingested content.

## Core Workflow

### 1. Ingest Content (Triggered by URL in Telegram Topic)

**Detect URL type and process:**

| URL Type | Processing |
|----------|------------|
| **Web Article** | Fetch content, extract text, entities |
| **YouTube** | Download audio → Whisper transcribe → Save transcript |
| **X/Twitter** | Get tweet + full thread (not just first tweet) |
| **PDF** | Download, extract text |
| **Tweet + Article** | Ingest both tweet thread AND linked article |

**YouTube Processing Pipeline:**
1. Extract metadata (title, channel, duration)
2. Download audio with `yt-dlp`
3. Transcribe with local Whisper
4. Extract entities from transcript
5. Save to Obsidian with full text

**Entity Extraction:**
- People (names)
- Companies/Organizations
- Concepts/Technologies
- Locations
- Dates/Events

**Storage:** Save to Obsidian vault at `~/Documents/Obsidian Vault/Knowledge Base/`

### 2. Query Knowledge Base

**Natural language queries:**
- "What do I know about AI regulation?"
- "Summarize what I've read about Tesla"
- "Find articles about climate change from last month"
- "What did I save about that startup?"

**Ranking factors:**
- Semantic relevance (vector similarity)
- Recency (newer sources rank higher)
- Source authority (user can weight sources)

## Data Structure

**Obsidian Storage:**
```
Knowledge Base/
├── Sources/
│   ├── 2026-02-25-article-title.md
│   ├── 2026-02-24-youtube-video-title.md
│   └── 2026-02-23-twitter-thread-topic.md
├── Entities/
│   ├── People/
│   │   └── Elon Musk.md
│   ├── Companies/
│   │   └── Tesla.md
│   └── Concepts/
│       └── Artificial Intelligence.md
└── Index/
    └── source-index.json
```

**Source Frontmatter:**
```yaml
---
title: Article Title
url: https://...
ingested: 2026-02-25T10:30:00Z
source_type: article|youtube|twitter|pdf
entities:
  - Elon Musk
  - Tesla
  - EVs
tags: [tech, automotive]
---
```

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/ingest.py` | Process content, create Obsidian notes |
| `scripts/query.py` | Semantic search with ranking |
| `scripts/extract_entities.py` | Extract people, companies, concepts |
| `scripts/process_youtube.sh` | Download + Whisper transcribe YouTube videos |

## Commands

- Drop URL in Telegram topic → Auto-ingest
- "Search my notes for [query]" → Semantic search
- "What do I know about [topic]?" → Summarize relevant sources
- "Show recent saves" → List by date
- "Find sources about [entity]" → Entity-based search

## YouTube with Whisper

For YouTube videos, use the full pipeline:
```bash
scripts/process_youtube.sh <youtube-url>
```

**Prerequisites:**
```bash
brew install yt-dlp ffmpeg
pip install openai-whisper
```

This downloads the audio and transcribes it locally with Whisper.

## Paywalled Content

For sites requiring login:
1. Use browser tool with `profile="chrome"` to access user's logged-in session
2. Navigate to URL
3. Extract content from rendered page
4. Save to Obsidian

## Response Style

- Confirm ingestion with summary
- For queries: synthesize across sources, cite sources
- Show entity extractions
- Link to Obsidian notes