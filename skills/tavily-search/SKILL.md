---
name: tavily-search
version: 1.0.0
description: Tavily-powered web search for AI agents. Use when Brave search is insufficient or when you need crawl/research features.
---

# Tavily Search 🔍

AI-optimized web search with content extraction, crawling, and research capabilities.

## When to Use (Auto-Routing)

**Use Tavily when search needs:**

1. **Multi-page crawl** — "crawl the docs", "download all pages"
2. **Site mapping** — "find all URLs", "map the site"
3. **Deep research** — "research report", "competitive analysis"
4. **Brave fails** — Brave search returns poor/incomplete results
5. **Extract from complex pages** — JavaScript-rendered content Brave can't handle

**Default to Brave when:**
- Simple factual queries
- News/current events
- General knowledge lookup
- Fast answers needed

## Auto-Routing Logic

```
Need: Multi-page content → Tavily crawl
Need: Site URLs → Tavily map
Need: Research report → Tavily research
Need: Deep dive → Tavily extract
Simple query → Brave search (default)
Fast answer → Brave search (default)
News → Brave + Tavily both
```

## Setup

API key stored in: `skills/tavily-config.md`

## Commands

### Search
```bash
TAVILY_API_KEY=tvly-xxx tvly search "query" --max-results 5 --json
```

### Extract (single URL → markdown)
```bash
TVLY_API_KEY=tvly-xxx tvly extract "https://example.com" --json
```

### Crawl (multi-page)
```bash
TVLY_API_KEY=tvly-xxx tvly crawl "https://docs.example.com" --output-dir ./docs/
```

### Research (AI report)
```bash
TVLY_API_KEY=tvly-xxx tvly research "topic" -o report.md
```

### Map (URL discovery)
```bash
TVLY_API_KEY=tvly-xxx tvly map "https://example.com" --json
```

## Free Tier Limits

- 1000 credits/month
- Search: ~1 credit per query
- Extract: ~3 credits per URL
- Research: ~50 credits per report

## Examples

```bash
# News search
tvly search "OpenClaw news" --topic news --time-range week

# Deep search
tvly search "quantum computing" --depth advanced --max-results 10

# Domain filter
tvly search "SEC filings" --include-domains sec.gov,reuters.com
```

## vs Brave Search

| Feature | Tavily | Brave |
|---------|-------|-------|
| Search | ✅ | ✅ |
| Extract | ✅ | ⚠️ (web_fetch) |
| Crawl | ✅ | ❌ |
| Research | ✅ | ❌ |
| Map | ✅ | ❌ |

---

*Installed 2026-03-27*