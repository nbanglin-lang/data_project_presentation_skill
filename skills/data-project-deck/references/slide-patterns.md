# Slide patterns

Anatomy, purpose, and title examples for each slide type in a data-project deck.

## Contents
- Action titles: the rules
- Title slide
- Executive summary
- Problem and impact
- Data and scope
- Pipeline
- Data quality decisions
- Finding (EDA or analysis)
- Model comparison
- Result and business impact
- Error analysis and failure modes
- Limitations and assumptions
- Recommendations and next steps
- Appendix

## Action titles: the rules

An action title states what the audience should conclude, not what the slide is
about. It is the single biggest difference between a deck that persuades and a
deck that merely displays.

- Write a full sentence with a verb and, where you have it, a number.
- Be specific: "Churn is concentrated in customers in their first 60 days" beats "Churn is a problem".
- Keep it to two lines at slide size (roughly 15 to 20 words at most).
- One message. If you need "and" to join two findings, make two slides.
- Test: cover the chart and read only the title. Does it tell you what to think?
  Then read all titles in order. Does the argument hold?

| Topic label (avoid) | Action title |
|---|---|
| Model results | The gradient-boosted model flags 71% of late orders, against 38% for the current rule |
| Customer segments | Three of five segments account for 82% of churn |
| Data overview | 96,000 orders over two years give enough history to model delivery delay |
| Next steps | Piloting early warnings with 40 sellers would test the effect within one quarter |

Exempt from the action-title rule: the title slide, section dividers, agenda,
Q&A or thank-you slide, and appendix divider.

## Title slide

- Project name, a one-line answer or promise as subtitle, presenter, date.
- Subtitle states the result: "Predicting late deliveries a day early" is better than "Data science project".

## Executive summary

Purpose: someone who reads only this slide should know the answer.

- Four short lines: the problem, what we found, what we recommend, expected impact.
- Numbers in every line that can have one.
- No chart. It is a text slide by design, and the only one that should be.
- Place it as slide 2 for decision-makers, where it replaces the agenda.

## Problem and impact

- Title states the problem and its size: "Late deliveries put an estimated 6% of repeat orders at risk".
- State the problem in the stakeholder's language and metric (revenue, cost, time, risk), not in model terms.
- One exhibit that shows the size or trend of the problem. Say why now.
- If the cost is an estimate, show the assumption behind it in the source line.

## Data and scope

- Title states what the data supports: "96,000 orders from 2016-2018 cover nine regions".
- Show source, time range, size, unit of analysis, and the one or two caveats that matter.
- A small table or a few big numbers works better than a paragraph.
- Keep detail (column list, schema) in the appendix.

## Pipeline

Purpose: show how the work was done in one glance, so the audience trusts it
without needing the details. One slide, about 30 seconds for non-technical audiences.

- Left-to-right flow of 4-6 stages: sources, ingest and clean, transform or feature build, analysis or model, output (dashboard, report, API).
- Under each stage: one short phrase and, for technical audiences, the tool (SQL, Python, dbt, Airflow).
- Mark where the key decisions or quality checks happen.
- Title states the outcome of the pipeline, not its name: "Daily refreshed pipeline turns raw orders into a delay score by 7am".
- Use `pipeline_diagram` in `scripts/chart_helpers.py`, or native shapes in the deck tool.

## Data quality decisions

- Title states the effect: "Dropping 3% of orders with missing dates does not change the delay estimate".
- Show what was dropped or imputed, how much, and a check that the choice did not drive the result.
- Usually appendix material unless the cleaning materially changes the story.

## Finding (EDA or analysis)

The workhorse slide. Typical deck has three to five.

- Title is the finding with its number.
- One chart that shows exactly that finding, with the relevant bar or line in the accent color and everything else grey.
- A one-line so-what below or beside the chart: what this implies for the decision.
- Source line: data, filter, date range, n.

## Model comparison

- Title states which approach wins and by how much, against a baseline the audience understands.
- Always include a simple baseline (current process, last-value, majority class) so the number has meaning.
- For technical audiences show intervals or repeated-run spread. For others, translate the metric (see `metrics-translation.md`).
- Keep the table to 3-5 rows. Highlight the chosen model's row; do not highlight everything.

## Result and business impact

- Translate the result into money, time, risk, or customers: "Early warnings could save about 1,200 repeat orders a quarter".
- Show the calculation chain in a source line or notes: assumption x volume = impact. State the main assumption and a range, not a single point, when the estimate is soft.
- A waterfall or before/after bar works well for impact bridges (`waterfall` helper).

## Error analysis and failure modes

- Title names where it fails: "Accuracy drops to 52% for orders shipped from small sellers".
- Show performance by segment, or the most costly error types.
- Include what you would do about it. This slide builds trust more than any accuracy figure.

## Limitations and assumptions

- Title is honest and specific: "Results hold for 2017-2018 data; we have not tested during peak season".
- Three to five items, ranked by how much each could change the conclusion. Each: the limitation, why it matters, what would address it.
- Put this in the main deck, not only the appendix. Stating limits first makes the findings more credible.

## Recommendations and next steps

- Title is the recommendation as a sentence.
- A small table: action, owner, timing, expected impact, cost or effort.
- Order by impact and ease. End on a single clear ask.
- Separate "do now" from "investigate".

## Appendix

- Divider slide, then methodology, data dictionary, extra charts, hyperparameters, model card, reproducibility details (data source and date, code link, environment, seed).
- Appendix slides still get action titles and source lines, because they get screenshotted and forwarded.
