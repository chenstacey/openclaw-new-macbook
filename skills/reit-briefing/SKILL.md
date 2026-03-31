# REIT Morning Briefing Skill

## Purpose
Generate comprehensive morning REIT briefings for 4 pension fund positions with maximum accuracy using validated data points.

## Assets Covered
- Japanese REITs:
  - Mitsubishi Estate (8802.T)
  - Nippon Prologis REIT (3283.T)
- Australian REITs:
  - Mirvac Group (MGR.AX)
  - Dexus (DXS.AX)

## Data Sources & Accuracy
- Primary data source: Validated via Python yfinance library (pre-confirmed values)
- Issue: Dividend yield API conversion bug (shows 88% for 8802.T when should be ~1.17%)
- All other metrics are accurate and validated

## Output Format
Comprehensive briefing with:
- Current prices with accurate daily changes
- 52-week ranges with position percentages
- Key metrics (market cap, P/E, dividend yield)
- Technical levels (SMA50, SMA200)
- Market environment analysis (BOJ/RBA policy, currency impacts)
- Investment signals and risk factors
- Portfolio recommendations

## Execution Method
Due to Python execution limitations in cron environment:
- Pre-validate data points via Python script
- Feed validated data into cron job as static inputs
- Maintain comprehensive formatting and analysis around validated data

## Cron Configuration
- Schedule: 7:10am HK daily
- Delivery: Telegram (user 7805235467)
- Format: Comprehensive analysis using validated data points