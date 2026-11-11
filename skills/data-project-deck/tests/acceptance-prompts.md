# Acceptance prompts

Run these after editing the skill to check it still behaves. For each, the
"should" list is what a good result contains. Use realistic source material
(a notebook, a results table, or a short written summary of a project).

## 1. Stakeholder readout from a notebook

Prompt: "I finished my delivery-delay analysis (notebook attached). Make a 10-minute
deck for the operations director. She cares about cost, not models."

Should:
- Start from an executive-summary slide that states the answer, not an agenda
- Use decision-maker storyline (problem, approach in one picture, findings, recommendation, risks, ask)
- Titles are full sentences with numbers; titles alone tell the story
- Metrics translated into business terms; a baseline appears next to every model number
- Limitations slide in the main deck; recommendations with owner and timing
- Numbers match the notebook (ledger kept); anything missing is marked `[TBD: ...]`
- Lint run on the .pptx with no errors; slides rendered and inspected

## 2. Portfolio walkthrough for an interview

Prompt: "Turn my data warehouse project (built on a public e-commerce dataset) into a deck for a data analyst interview.
I built the pipeline with SQL and Python."

Should:
- Portfolio storyline: hook, context and my role, problem, data, pipeline diagram, findings, decisions and why, what went wrong, next steps, links
- States which parts were a course or public-dataset exercise
- Pipeline slide is one diagram with tools named
- Does not invent business results that were not in the source material

## 3. Negative result

Prompt: "My model barely beat the baseline (0.61 vs 0.58 AUC) and the intervals overlap.
Make slides for my supervisor."

Should:
- Title does not claim a clear winner
- Shows intervals; says the difference is not distinguishable
- States what was learned, what it means for the decision, and a next step with cost

## 4. Critique an existing deck

Prompt: "Here is my deck (pptx attached). Make it better but keep the content."

Should:
- Run lint, report the title sequence, rewrite topic titles as takeaway sentences
- Split overloaded slides, move method detail to appendix, add source lines and alt text
- Edit the attached file's format (.pptx stays .pptx), working on a copy

## 5. Should not trigger

- "Explain what a confusion matrix is" (a question, not a deck)
- "Make a dashboard of my sales data" (dashboard, not a presentation)
- "Write a README for my project" (document)
