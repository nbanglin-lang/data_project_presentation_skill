# Storylines by audience

Pick the storyline that matches who is in the room. The same project becomes
four different decks. All of them share one spine, then differ in how much method
they show and where the result sits.

## Contents
- The shared spine (SCQA)
- A. Decision-maker readout
- B. Technical peer review
- C. Portfolio or interview walkthrough
- D. Course or capstone final presentation
- Building the ghost deck
- Timing

## The shared spine (SCQA)

Frame the opening as Situation, Complication, Question, Answer:

- **Situation**: the stable context the audience already agrees with.
- **Complication**: what changed or what is going wrong (the business problem).
- **Question**: what the audience therefore needs to decide or understand.
- **Answer**: your conclusion, stated up front.

Putting the answer first (the "inverted pyramid") matters because the audience's
attention is highest at the start, and because a reader who sees the conclusion
first can judge the evidence against it instead of waiting to find out where the
talk is going. The detail then follows as supporting groups of evidence, each
group becoming a section of the deck.

## A. Decision-maker readout (sponsor, executive, client)

Goal: get a decision or approval. About 10 minutes, 8-10 main slides. Audience
cares about outcome, impact, risk, and cost, not model internals. Keep time on
data and method to roughly 30 seconds.

| # | Slide | Job |
|---|---|---|
| 1 | Title | Name plus a one-line answer as the subtitle |
| 2 | Executive summary | Problem, finding, recommendation, expected impact in four short lines |
| 3 | The problem and what it costs | Business problem in business metrics; why now |
| 4 | Approach in one picture | Data to pipeline to output; no jargon |
| 5-7 | Findings (one per slide) | Each: finding as title, one chart, a so-what line |
| 8 | Recommendation | Action, owner, timeline, expected impact, cost |
| 9 | Risks and limits | What could make this wrong; confidence level; what to monitor |
| 10 | Decision or ask | Exactly what you need from them, by when |
| A | Appendix | Method detail, extra charts, data dictionary, model card |

## B. Technical peer review (data team, supervisor, reviewers)

Goal: have the work scrutinized and the method trusted. 15-20 minutes. The
result still comes early (slide 2 or 3), because reviewers read the method
differently once they know the claim.

| # | Slide | Job |
|---|---|---|
| 1 | Title | |
| 2 | Problem and headline result | Task definition, success criterion, the main number against a baseline |
| 3 | Data | Source and provenance, size, time range, labels, how it was split |
| 4 | Data quality decisions | What was dropped or imputed and how much it changed things |
| 5 | EDA findings that shaped the approach | Two or three, each as an action title |
| 6 | Pipeline and features | Diagram of the pipeline; key features and why |
| 7 | Evaluation protocol | Metric choice, split, cross-validation, leakage controls |
| 8 | Results vs baselines | Comparison with uncertainty (intervals or repeated runs) |
| 9 | Error analysis | Where it fails and for whom; segment performance |
| 10 | Ablation or sensitivity | What actually drives the result |
| 11 | Limitations and threats to validity | Honest list, ranked |
| 12 | Next steps | What would most improve confidence |
| A | Appendix | Hyperparameters, extra plots, reproducibility details |

## C. Portfolio or interview walkthrough

Goal: show how you think, not only what you built. About 10 minutes, and the
person listening is judging judgment, communication, and honesty. Keep your own
role explicit. Use "I" for decisions you made and say plainly when a result is
modest.

| # | Slide | Job |
|---|---|---|
| 1 | Title and hook | The project plus its headline result in one line |
| 2 | Context and my role | What the problem was, who it was for, what I owned |
| 3 | The business question | Framed as a decision someone had to make |
| 4 | Data | Source, size, quirks; what made it hard |
| 5 | Pipeline | One diagram: ingest, clean, model or analyse, output; tools named |
| 6-8 | Key findings | One per slide, each with a chart and an action title |
| 9 | Decisions I made and why | Two or three judgment calls and the alternatives rejected |
| 10 | What went wrong and what I changed | A real mistake or dead end, handled well |
| 11 | Limitations and what I would do next | |
| 12 | Skills and tools, with link | Repository, notebook or dashboard link; contact |

Why include slides 9 and 10: interviewers learn more from a considered trade-off
and an honest dead end than from another chart. If the project came from a
course or a public dataset, say so directly and point out what you added beyond
the brief.

## D. Course or capstone final presentation

These are usually assessed against a rubric. Check the rubric first and mirror
its headings in the slide titles so the assessor can find each criterion. A
common set of components, which you should adapt to the actual rubric:

1. Project overview: business problem and objectives
2. Data collection: sources, how access was obtained
3. Cleaning and preprocessing: decisions and their effect
4. Exploratory analysis and feature engineering
5. Modeling or analysis approach
6. Results, insights, and recommendations
7. Limitations and next steps

Still use action titles inside those sections, so the deck reads as an argument
and not as a form being filled in.

## Building the ghost deck

1. Write the single sentence you want the audience to leave with (the governing thought).
2. List the 2-4 reasons or findings that support it. These become sections.
3. Under each, list the evidence slides. Write each title as a sentence.
4. Add the opening (context, problem) and closing (recommendation, ask).
5. Mark each slide with its exhibit: "bar chart, region vs delay days", "pipeline diagram", "table, 3 models".
6. Run the titles test, then cut or merge anything that does not move the argument.

Example ghost-deck fragment for a delivery-delay project:

1. Late deliveries are costing an estimated 6% of repeat orders (exhibit: before/after bar, headline number)
2. Delays concentrate in three regions, not across the network (exhibit: ranked bars, top three highlighted)
3. Seller handling time, not carrier transit, explains most of the gap (exhibit: stacked time breakdown)
4. A simple model flags 7 in 10 late orders a day before they ship (exhibit: model vs baseline)
5. We recommend piloting early warnings with the 40 slowest sellers (exhibit: action table)

## Timing

About one main slide per minute. Beyond roughly 1.5 slides per minute, either
the slides are too dense or the talk will rush. The appendix does not count
toward the time; it exists to answer questions without cluttering the story.
