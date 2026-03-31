# Market Briefing Skill

## Description
Daily 8am market briefing covering overnight US markets and key news impacting Asian markets (Hong Kong, China, Japan).

## Schedule
**8:00 AM daily (weekdays)** — Asian market open

## Content

### 🇺🇸 US Markets Overnight
- S&P 500 close, change, key movers
- NASDAQ close, change, tech focus
- US futures pre-Asia (implied open bias)

### 📰 Key News Impacting Asia
- Major headlines with impact analysis
- Corporate/policy news
- Regional factors (China policy, HK flows, Japan yen/BoJ)

### 📊 Asian Markets Today
- **Hang Seng** — Expected open, key levels, sectors
- **Shanghai Composite** — Expected open, key levels, themes
- **Nikkei 225** — Expected open, key levels, focus

### 🎯 Trading Focus
- Key events to watch per market
- Flow indicators
- Risk factors

### 💡 Key Levels
Support/resistance levels with overnight bias

## Usage

**Automatic:**
- Generates daily at 8am
- Saved to `Markets/YYYY-MM-DD.md`

**On-demand:**
- "Markets" — Get latest briefing
- "Market update" — Force refresh

## Data Sources
- Brave Search (market data, news)
- Yahoo Finance (price data)

## Cost Tracking
- ~10-15 queries per briefing
- Daily: ~15 queries (well under 50 limit)
- Monthly: ~300 queries (well under 1,000 cap)

## Output Location
`~/Documents/Obsidian Vault/Markets/YYYY-MM-DD.md`
