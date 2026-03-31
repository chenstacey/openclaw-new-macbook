---
name: allianz-care-claim
description: Allianz Care insurance claim formatter with benefits optimization and policy Q&A. Formats medical receipts into claim categories, answers coverage questions, and auto-submits claims via Chrome Relay Extension.
---

# Allianz Care Claim & Benefits Assistant (OPTIMIZED VERSION)

> ⚠️ **Speed optimization**: This skill is optimized for Sisi's typical claims (HK, HKD). Most fields are pre-filled — only ask for provider, treatment type, patient, amount.

## Speed Optimization: Default Values

**For Sisi's typical claims (HK, HKD), these are ALWAYS correct — skip asking:**
- Country: Hong Kong SAR, China (always)
- Currency: HKD (always)
- Payee: Insured member (always)
- Accident: No (always)
- Other insurance: No (always)
- Hospitalization: No (always)

**Only ask user for:**
- Provider name (from receipt header — clinic name, NOT practitioner name)
- Treatment type (Physiotherapy / Doctor Visit / etc.)
- Patient (Sisi / Chao Cheng / William)
- Amount + Date

---

## Core Functions

### 🚀 Auto-Submit Claims

**Trigger:** User sends receipt photos or says "submit this claim"

**Uses:** `profile=user` — your real Chrome with Relay Extension

---

#### ⚠️ Pre-flight Checklist
1. Chrome open with OpenClaw extension attached
2. If disconnected → click extension icon → "continue, browser is attached"
3. Use `profile=user` (NOT profile=chrome or default)

---

#### ⚠️ Receipt Analysis Protocol

**From receipt, extract ONLY:**
1. **Provider** → Clinic/business name in header (e.g., "Joint Dynamics", NOT "Ms. Mandy Hilary Shum")
2. **Treatment type:**
   - Physiotherapist → Doctor Visit → Physiotherapy
   - Doctor → Doctor Visit → GP or Specialist
   - Osteopath → Alternative treatment → Osteopathy
3. **Patient** → Who (Sisi/Chao/William)
4. **Amount + Date**

---

## Submit Flow (Optimized — Minimal Snapshots)

### Phase 1: Pre-browser
- Copy receipt to /tmp/openclaw/uploads/
- Extract 4 details from receipt (provider, type, patient, amount)

### Phase 2: Navigate (1 snapshot)
```bash
browser action=navigate profile=user targetUrl=https://my.allianzcare.com
```
- 1 snapshot to verify page loaded

### Phase 3: Submit Claim (no snapshot)
```bash
browser action=act profile=user request='click text="Submit a claim"'
browser action=act profile=user request='click text="Continue"'
```

### Phase 4: Fill Invoice Form (no snapshots)
User uploads file → wait for "✓ PDF"

Then fill fields in order:
1. Patient → Sisi Chen (1991)
2. Country → Hong Kong SAR, China
3. Provider → [from receipt header]
4. Currency → HKD
5. Invoice date → DD/MM/YYYY
6. Treatment date → DD/MM/YYYY
7. Treatment type → Doctor Visit → Physiotherapy (or appropriate)
8. Hospitalization Q1 → No
9. Hospitalization Q2 → No
10. Amount → [from receipt]

Click Save Invoice → 1 snapshot to verify

### Phase 5: Submit (1 snapshot)
```bash
browser action=act profile=user request='click text="Submit Claim"'
browser action=act profile=user request='click text="Agree and Proceed"'
```
1 snapshot to confirm claim number

---

## Timeout Handling
- If timeout → wait 3 seconds, retry once
- If still fails → ask user to complete manually

---

## Known Form Values (Sisi's Policy)

| Field | Default | When to Change |
|-------|---------|----------------|
| Patient | Sisi Chen (1991) | If Chao Cheng or William |
| Country | Hong Kong SAR, China | Never |
| Currency | HKD | Never |
| Payee | Insured member | Never |
| Accident | No | Never |
| Other insurance | No | Never |
| Hospitalization | No | Never |

---

## Treatment Type Guide

| Receipt Says | Select |
|--------------|--------|
| Physiotherapist/Physiotherapy | Doctor Visit → Physiotherapy |
| Doctor/General Practitioner | Doctor Visit → GP/General Doctor |
| Specialist | Doctor Visit → Specialist Visit |
| Osteopath | Alternative treatment → Osteopathy |
| Chiropractor | Alternative treatment → Chiropractor |

---

## Provider Name Rule

- **Header/Clinic name** = CORRECT (e.g., "Joint Dynamics")
- **Practitioner name** = WRONG (e.g., "Ms. Mandy Hilary Shum")

---

## All Commands

| Command | What I Do |
|---------|-----------|
| Send receipt | Extract details → auto-submit → report claim number |
| "Submit claim" | Start browser workflow |
| "What's covered for [treatment]?" | Check coverage |
| "Explain my benefits" | Policy summary |

---

## Policy Info

**Policy:** APG Investments Asia Ltd (P003799926)
**Plan:** Hong Kong Summit 5000 (Standard Network)
**Coverage:** Out-patient 90%, In-patient 80%

---

*Updated: Mar 27, 2026*