---
name: data-project-deck
description: Builds presentation decks for data analysis and data science projects - the business problem, the data and pipeline, key findings with charts, limitations, and recommendations - using a consulting-style storyline (action titles, one message per slide, answer first) and verified numbers. Use whenever the user wants slides, a deck, a readout, a stakeholder presentation, a capstone or final-project presentation, a portfolio or interview walkthrough, or a pitch based on a notebook, dataset, model results, dashboard, or analysis write-up, even if they never say "storyline" or "data science". Also use to restructure, tighten, or critique an existing data-project deck.
---

# Data Project Deck

Turn an analysis into a deck that a busy audience can follow in one pass. Most
data-project decks fail the same way: they replay the analyst's *process* (data,
cleaning, models, metrics) and bury the *answer* on slide 14. This skill reverses
that: lead with the answer, then give just enough evidence for the audience to
trust it.

## What good looks like

- The titles alone, read top to bottom, tell the whole story (the "titles test").
- Every slide carries one message, stated as a sentence in its title, and the
  visual on the slide proves that sentence.
- The business problem is stated in the audience's language before any method.
- Every number on a slide traces to a source and has been recomputed or checked.
- Limitations are shown on purpose, not discovered by an audience member.
- The deck ends with a decision or next step, with an owner and a date where possible.

## Workflow

Work through these in order. Steps 3 and 7 are where decks most often go wrong,
so do not skip them under time pressure.

### 1. Intake - infer first, ask only what is missing

Settle four things. Infer from the conversation and attached files; ask one short
question only if the answer would change the deck's structure.

| Question | Why it matters | Default if unknown |
|---|---|---|
| Who is the audience? (decision-maker, technical peers, recruiter/interviewer, course assessor) | Picks the storyline and how much method to show | Mixed: non-technical decision-makers plus one technical reviewer |
| How long is the slot? | Roughly one main slide per minute | 10 minutes, so 8-12 main slides plus appendix |
| What source material exists? (notebook, CSVs, results tables, write-up, dashboard) | You can only claim what the material supports | Ask for it; do not invent results |
| What output format? | Decides the build route in step 6 | The deck type this session offers (see step 6) |

### 2. Write the ghost deck before any slide

A ghost deck is the whole presentation as a numbered list of action titles, one
per slide, with a one-line note of the exhibit each will use. The thinking
happens here; the slides are then mostly assembly. It is cheap to fix a story
at this stage and expensive after charts are built.

1. Pick the storyline for the audience: read `references/storylines.md`.
2. Draft titles as full-sentence conclusions with a number where possible.
3. Run the titles test: read only the titles. Does the argument hold? Is any
   slide a topic label ("Model results")? Does any slide carry two messages
   (split it)? Does any slide not serve the story (cut it or move it to the appendix)?
4. If the user is present and the project facts are thin or ambiguous, show the
   ghost deck and get a quick confirmation. If the facts are clear, or nobody is
   watching, proceed and note the structure you chose.

Titles you cannot yet write because the number is missing are a to-do for step 3,
not a reason to write a vague title.

### 3. Gather and verify the evidence

Read the full source material first. Then build a **numbers ledger** (a small
table you keep for yourself, and deliver on request): one row for every figure
that will appear on a slide.

| Slide | Claim | Value | Source (file/cell/table) | Check |
|---|---|---|---|---|
| 4 | Late deliveries rose after the policy change | 12.1% -> 17.4% | orders.csv, col delay_flag | recomputed |

- When the data is available, recompute the figure in code instead of copying it.
  Where only a reported number exists, mark it "as reported" and say so in notes.
- Check arithmetic, units, denominators, date ranges, and that percentages and
  absolute numbers agree across slides.
- For models: confirm the evaluation was on held-out data, name the baseline
  being beaten, and give the sample size. An accuracy figure with no baseline
  and no n is not evidence. If the project involves backtests or time series,
  also check for look-ahead leakage and whether results are net of costs.
- Never fill a gap with a plausible number. Use a visible `[TBD: ...]` placeholder
  and list it in your hand-off.
- Translate technical metrics into the audience's terms: read
  `references/metrics-translation.md`.

### 4. Design each slide from its pattern

For each slide type (executive summary, problem, pipeline, finding, model
comparison, limitations, recommendation, appendix), `references/slide-patterns.md`
gives the anatomy and good/bad title examples. The rules that apply everywhere:

1. **Action title**: a complete sentence stating the takeaway, specific, ideally
   with a number, at most two lines. "Orders from the north region arrive 3.1
   days later than average", not "Delivery analysis".
2. **One message per slide.** If the title needs "and", split the slide.
3. **The visual proves the title.** One main exhibit. Text supports it; it does
   not repeat it.
4. **Source line** on every slide that shows data: where the numbers come from
   and the date range or sample.
5. **Text discipline**: aim for under about 60 words of body text; body text 14pt
   or larger; nothing under 12pt. If it will not fit, the slide has too many
   messages, so split it instead of shrinking the font.
6. **Method is context, not the star.** The pipeline gets one slide. Details go
   to the appendix. Technical audiences get more, but still after the result.
7. **Consistent layout**: title, exhibit, takeaway, and source in the same
   positions on every slide; one font family; a restrained palette.

### 5. Charts

Read `references/visualization.md` before making any chart. The short version:
match the chart to the question, remove everything that is not the point, grey
everything except what the title is about (accent color on the one thing that
matters), label directly, start bar charts at zero, show uncertainty when the
claim depends on it, and put the takeaway in the chart's title.

If this session has a `dataviz` skill, read it before writing chart code and use
its color rules. `scripts/chart_helpers.py` gives matplotlib helpers that already
follow these rules (highlighted bar, line with end labels, waterfall bridge,
confidence-interval dot plot, pipeline diagram). Import them rather than
restyling every chart by hand:

```python
import sys; sys.path.insert(0, "<skill dir>/scripts")
from chart_helpers import bar_highlight, line_end_labels, waterfall, ci_dots, pipeline_diagram
```

### 6. Build the deck

Use whichever deck route this session offers, in this order:

1. A dedicated slide-deck artifact type (e.g. a Slides type listed by the
   Artifact tool), unless the user asked for a PowerPoint file. It gives the user
   an editor and an export to .pptx or PDF.
2. If the user asked for a .pptx (or no deck type is listed), read and follow the
   `pptx` skill, using this skill's content decisions.
3. If neither exists, build with python-pptx directly at 16:9.

Whatever the route, apply these:

- Put speaker notes on every main slide: a two- to four-sentence talk track and,
  where useful, the question the slide is likely to provoke with a short answer.
- Give pictures and charts alt text (one sentence stating what the chart shows).
- Put methods, extra charts, the data dictionary, and detailed model settings in
  an appendix after the closing slide, each with an action title too.
- Native, editable charts are better than pasted images when the tool supports
  them. Otherwise export images at 200 dpi, sized for the slide.
- Put the source line in the slide as text rather than baking it into the chart
  image (call the chart helpers with `source=None`). It stays editable, and the
  linter can see it. Never show it twice.

### 7. QA before handing over

1. **Lint** (for .pptx output): `python <skill dir>/scripts/lint_deck.py deck.pptx --minutes 10`.
   It flags topic-label titles, crowded slides, tiny fonts, missing sources,
   missing alt text, missing notes, duplicate titles, and prints the titles in
   order so you can run the titles test on the real file. Add
   `--ledger ledger.csv` to list any number on a slide that is not in your ledger.
   Fix errors; judge warnings.
2. **Look at it.** Render slides to images (LibreOffice to PDF, then pdftoppm) and
   inspect them for overflow, overlapping labels, unreadable charts, and
   inconsistent layout. The linter cannot see layout.
3. **Re-verify the numbers** on the final slides against the ledger. A number
   edited late is the most common source of an error in a finished deck.
4. **Read it as the audience's skeptic.** What is the first question they will
   ask? Is it answered in the deck or the notes?

For a deck that is a Slides artifact rather than a file, do the same checks by
reading the content back and looking at the rendered result.

### 8. Hand over

Report in a few lines: what the deck argues, where it is, the main assumptions
you made, any `[TBD]` placeholders, and one natural next step (for example, a
rehearsal pass or a shorter executive version). Do not recap the steps you took.

## Optional features - add when they fit the request

- **Executive version**: a 3-slide cut (answer, evidence, ask) for forwarding.
- **Standalone summary slide** that makes sense without the presenter, for decks
  that will be read rather than presented.
- **Model card slide** in the appendix: intended use, data, performance by
  segment, known failure modes, monitoring plan.
- **Reproducibility footer** in the appendix: data source and date pulled, code
  repo link, environment, random seed. Technical reviewers and interviewers look
  for this.
- **Portfolio mode** (interviews, applications): add your role and the decisions
  you made and why, tools used, one thing that went wrong and what you changed,
  and what you would do next. Keep a link to the code. See the portfolio
  storyline in `references/storylines.md`.
- **Negative or inconclusive results**: still a valid deck. Lead with what was
  learned and what it means for the decision; see `references/metrics-translation.md`.

## Reference files

| File | Read it when |
|---|---|
| `references/storylines.md` | Choosing the structure for the audience (step 2) |
| `references/slide-patterns.md` | Designing any individual slide (step 4) |
| `references/visualization.md` | Before making any chart (step 5) |
| `references/metrics-translation.md` | Presenting model metrics, uncertainty, limits, or bad news (step 3) |
| `scripts/chart_helpers.py` | Making charts and the pipeline diagram (step 5) |
| `scripts/lint_deck.py` | Checking a finished .pptx (step 7) |
| `tests/acceptance-prompts.md` | Checking the skill still behaves after you edit it |
