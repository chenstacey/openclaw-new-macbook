---
name: autoresearch
description: "Autonomously optimize any Claude Code skill or prompt by running it repeatedly, scoring outputs against binary evals, mutating the prompt, and keeping improvements. Based on Karpathy's autoresearch methodology. Use when: optimize this skill, improve this skill, run autoresearch on, make this skill better, self-improve skill, benchmark skill, eval my skill, run evals on. Outputs: an improved SKILL.md, a results log, and a changelog of every mutation tried."
---

# Autoresearch for Skills

Most skills work about 70% of the time. The other 30% you get garbage. The fix isn't to rewrite the skill from scratch. It's to let an agent run it dozens of times, score every output, and tighten the prompt until that 30% disappears.

This skill adapts Andrej Karpathy's autoresearch methodology (autonomous experimentation loops) to Claude Code skills and any prompt-based system. Instead of optimizing ML training code, we optimize skill prompts.

**Core loop:**
```
modify → run → measure → keep if better / discard if worse → repeat
```

---

## Before Starting: Gather Context

**STOP. Do not run any experiments until all fields below are confirmed. Ask for any missing fields.**

1. **Target** — Which skill or prompt to optimize? (exact path to SKILL.md or prompt file)
2. **Test inputs** — 3–5 different prompts/scenarios (variety matters — cover different use cases)
3. **Eval criteria** — 3–6 binary yes/no checks that define a good output
4. **Runs per experiment** — Default: 5 (more = reliable, slower)
5. **Budget cap** — Optional. Max cycles before stopping. Default: no cap.

---

## Step 1: Read the Target

Read the full SKILL.md (or prompt file) completely before touching anything. Read any linked `references/` files. Understand the core job, steps, and output format.

**Do not skip this.**

---

## Step 2: Build the Eval Suite

Convert criteria into structured binary tests. Every check must be pass/fail — no scales.

**Format each eval:**
```
EVAL [N]: [Short name]
Question: [Yes/no question about the output]
Pass condition: [What "yes" looks like — specific]
Fail condition: [What triggers a "no"]
```

**Rules for good evals:**
- Binary only — yes or no, never "rate 1–7"
- Specific enough to be consistent ("Are all words spelled correctly?" not "Is text readable?")
- Not so narrow the skill games the eval ("fewer than 200 words" → skill optimizes brevity only)
- 3–6 evals is the sweet spot

**Max score:** `[number of evals] × [runs per experiment]`
Example: 4 evals × 5 runs = max 20 points.

---

## Step 3: Generate Live Dashboard

Before running experiments, create a live dashboard at `autoresearch-[skill-name]/dashboard.html`.

Dashboard must:
- Auto-refresh every 10 seconds (reads from results.json)
- Score progression line chart (experiment # on X, pass rate % on Y)
- Colored bar per experiment: green = keep, red = discard, blue = baseline
- Table: experiment #, score, pass rate, status, description
- Per-eval breakdown: which evals pass most/least
- Current status: "Running experiment [N]..." or "Idle"
- Clean styling (white background, pastel accents, sans-serif)

Generate as single self-contained HTML (inline CSS/JS, Chart.js from CDN). Open immediately: `open dashboard.html`

**results.json format:**
```json
{
  "skill_name": "[name]",
  "status": "running",
  "current_experiment": 3,
  "baseline_score": 70.0,
  "best_score": 90.0,
  "experiments": [
    {"id": 0, "score": 14, "max_score": 20, "pass_rate": 70.0, "status": "baseline", "description": "original skill — no changes"}
  ],
  "eval_breakdown": [
    {"name": "Text legibility", "pass_count": 8, "total": 10}
  ]
}
```

---

## Step 4: Establish Baseline

Run the skill/prompt AS-IS. This is experiment #0.

1. Create `autoresearch-[skill-name]/` directory
2. Back up original as `SKILL.md.baseline`
3. Create `results.tsv`, `results.json`, `changelog.md`
4. Open dashboard in browser
5. Run [N] times with test inputs, score every output
6. Record baseline score in both files

**results.tsv format:**
```
experiment	score	max_score	pass_rate	status	description
0	14	20	70.0%	baseline	original skill — no changes
```

**Confirm baseline with user before proceeding.** If already 90%+, ask if they want to continue.

---

## Step 5: Run the Experiment Loop

**Run autonomously until stopped. Never pause to ask if you should continue.**

Each cycle:

1. **Analyze failures** — which evals fail most? Read actual failing outputs. Find the pattern.

2. **Form hypothesis** — pick ONE thing to change. Never change multiple things at once.

   **Good mutations:**
   - Add specific instruction addressing the most common failure
   - Reword ambiguous instruction to be explicit
   - Add anti-pattern ("Do NOT do X") for recurring mistake
   - Move buried instruction higher (priority = position)
   - Add example showing correct behavior
   - Remove instruction causing over-optimization

   **Bad mutations:**
   - Rewriting entire skill from scratch
   - Adding 10 new rules at once
   - Vague instructions like "be more creative"

3. **Make the change** — edit SKILL.md with ONE targeted mutation

4. **Run [N] times** with test inputs

5. **Score** every output against every eval

6. **Keep or discard:**
   - Score improved → **KEEP** (new baseline)
   - Same or worse → **DISCARD** (revert SKILL.md)

7. **Log** in results.tsv and results.json

8. **Repeat** from step 1

**Stop only when:**
- User stops manually
- Budget cap hit
- 95%+ pass rate for 3 consecutive experiments

**If out of ideas:** re-read failing outputs, try combining near-miss mutations, try removing instead of adding.

---

## Step 6: Write the Changelog

After every experiment, append to `changelog.md`:

```markdown
## Experiment [N] — [keep/discard]

**Score:** [X]/[max] ([percent]%)
**Change:** [One sentence — what was changed]
**Reasoning:** [Why expected to help]
**Result:** [What actually happened — which evals improved/declined]
**Failing outputs:** [What still fails, if anything]
```

This changelog is the most valuable artifact. A future agent can pick it up and continue.

---

## Step 7: Deliver Results

When user returns or loop stops, present:

1. **Score summary:** Baseline → Final (% improvement)
2. **Total experiments run**
3. **Keep rate** (kept vs discarded)
4. **Top 3 changes that helped most**
5. **Remaining failure patterns**
6. **Improved SKILL.md** (already saved)
7. **File locations** for results.tsv and changelog.md

---

## Output Files

```
autoresearch-[skill-name]/
├── dashboard.html       ← live browser dashboard (auto-refreshes)
├── results.json         ← data file powering the dashboard
├── results.tsv          ← score log for every experiment
├── changelog.md         ← detailed mutation log
└── SKILL.md.baseline    ← original skill before optimization
```

Plus the improved SKILL.md saved back to its original location.

---

## Usage Examples

- "Run autoresearch on the allianz-care-claim skill"
- "Optimize my morning-briefing prompt using autoresearch"
- "What can autoresearch improve in this skill?"
- "Self-improve this SKILL.md"

---

## Notes

- Adapted from Andrej Karpathy's autoresearch (github.com/karpathy/autoresearch), released March 2026
- Original applied to ML training code; this version applies the same loop to prompt/skill optimization
- The key insight: **any system with an objective metric + automated measurement + something to change can be autoresearched**
