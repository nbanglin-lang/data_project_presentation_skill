# Data Analysis Presentation Skill

An agent skill that builds presentation decks for data analysis and data science
projects: the business problem, the data and pipeline, key findings with charts,
limitations, and recommendations.

Most data-project decks replay the analyst's process and bury the answer near the
end. This skill reverses that. It leads with the answer, writes every slide title
as a takeaway sentence, keeps one message per slide, and checks every number
against its source before the deck is handed over.

## What it does

- Picks a storyline for the audience: decision-maker readout, technical peer
  review, portfolio or interview walkthrough, or course capstone
- Drafts a "ghost deck" (titles only) first and runs the titles test: read only
  the titles, and the argument should hold
- Keeps a numbers ledger so every figure on a slide traces to a source
- Translates model metrics into business terms, always next to a baseline
- Designs charts that grey out context and highlight the one thing the title is about
- Builds the pipeline slide as a single diagram, puts limitations in the main deck,
  and adds speaker notes and alt text
- Lints the finished .pptx and checks rendered slides before hand-over

## Layout

```
skills/data-project-deck/
├── SKILL.md                      # workflow and rules (loaded when the skill triggers)
├── references/
│   ├── storylines.md             # structures by audience, ghost-deck procedure
│   ├── slide-patterns.md         # anatomy and action-title examples per slide type
│   ├── visualization.md          # chart choice, decluttering, color, uncertainty
│   └── metrics-translation.md    # metrics to business language, limitations, bad news
├── scripts/
│   ├── chart_helpers.py          # matplotlib helpers: bar, line, waterfall, CI dots, pipeline
│   └── lint_deck.py              # deck checker for .pptx files
└── tests/
    └── acceptance-prompts.md     # prompts to re-check behavior after edits
```

## Install

The skill is a folder containing a `SKILL.md`, following the Agent Skills format.
For Claude Code, copy the skill folder into your skills directory:

```bash
git clone https://github.com/<your-username>/data-project-deck-skill.git
cp -r data-project-deck-skill/skills/data-project-deck ~/.claude/skills/
```

For other tools that read skill folders, place it wherever that tool looks for skills.

The scripts need Python 3.9+ and two packages:

```bash
pip install -r requirements.txt
```

## Use

Describe the deck you want and attach or point to your analysis. For example:

- "Make a 10-minute readout deck from this notebook for the operations director."
- "Turn my churn model project into a portfolio presentation for a data analyst interview."
- "Here is my capstone deck. Tighten the titles and cut it to 12 slides."

To check a finished PowerPoint file yourself:

```bash
python skills/data-project-deck/scripts/lint_deck.py deck.pptx --minutes 10
python skills/data-project-deck/scripts/lint_deck.py deck.pptx --ledger numbers.csv --json
```

It prints the slide titles in order and flags topic-label titles, crowded slides,
fonts under 12pt, data slides with no source line, pictures without alt text,
missing notes, and duplicate titles. It exits with status 1 if any error is found.
The linter reads text and shape properties only, so also render the slides and
look at them.

To make charts in your own scripts:

```python
import sys; sys.path.insert(0, "skills/data-project-deck/scripts")
from chart_helpers import bar_highlight, ci_dots, waterfall, line_end_labels, pipeline_diagram

bar_highlight(["North", "South", "East"], [8.2, 5.1, 4.4], highlight=["North"],
              path="delay.png", fmt="{:.1f} days")
```

## Safety

The scripts read the files you give them and write only the output files you name.
They make no network calls and delete nothing. As with any skill, read the code
before installing it.

## Testing

`tests/acceptance-prompts.md` lists five prompts and what a good result contains.
Run them after editing the skill to see whether the behavior still holds.

## Credits and sources

The method draws on widely taught practice for consulting-style slides (action
titles, one message per slide, answer first) and for communicating data science
results to non-technical audiences. The reference files are written in my own
words. Chart colors come from the Okabe-Ito color-blind-safe palette.

## License

MIT. See [LICENSE](LICENSE).
