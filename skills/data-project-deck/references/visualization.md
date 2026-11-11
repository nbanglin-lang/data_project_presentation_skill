# Visualization for slides

A chart on a slide has one job: make the title's claim obvious faster than a
table could. If a chart does not prove its slide's title, change the chart or the title.

## Contents
- Choose the chart from the question
- Declutter, then highlight
- Color
- Labels, titles, and sources
- Uncertainty
- Charts for data-science results
- Slide-size specs
- Checklist

## Choose the chart from the question

Start from what the audience should see, not from what the software offers.

| Question | Use | Avoid |
|---|---|---|
| How do categories compare? | Bar chart, sorted; horizontal when labels are long or there are many categories | Pie chart, 3D |
| How does it change over time? | Line chart; columns if few periods | Stacked areas with many series |
| What is the composition? | Stacked bar of 2-4 parts; single stacked bar for share | Pie with many slices |
| How do two numeric variables relate? | Scatter, with a fitted line if the claim is about trend | Dual axes |
| What is the distribution? | Histogram or box/violin; add a reference line for the mean or threshold | Bar of means with no spread |
| How did we get from A to B? | Waterfall (bridge) | A table of deltas |
| How do models compare, with uncertainty? | Dot plot with intervals | Bar chart without error bars |
| Few exact numbers matter | Table or big-number callout | A chart for two data points |

Never use two y-axes on one chart: it lets the author imply a relationship the
data does not show. Two measures on different scales become two charts, small
multiples, or an indexed series.

## Declutter, then highlight

Default chart settings add things that do not carry meaning. Remove gridlines (or
make them hairline), borders, legend boxes where direct labels work, redundant
axis labels, and decimals that imply false precision. Then add back only what
earns its place: a title that states the takeaway, direct labels on key points,
and a light reference line if it helps.

Highlight with contrast: make everything grey except the one thing the title is
about, and give that the accent color. The audience's eye goes to the color, so
color should mean "look here".

Bar charts start at zero, because bar length encodes value. Line charts may use
a non-zero baseline when the claim is about change, but say so on the axis.

## Color

- Grey for context, one accent for the point of the slide, a second contrasting color only when the slide compares two things (for example, current vs proposed).
- Do not use rainbow palettes, or use color to mean something different on different slides.
- Keep color meaning consistent across the deck: if blue is "our model" on slide 7, it is not "region North" on slide 8.
- Check that the colors are distinguishable for color-blind viewers and legible in grayscale (print or projector washout). The default palette in `scripts/chart_helpers.py` is chosen for this: a blue accent, an orange contrast, and neutral greys. If the session has a `dataviz` skill, use its palette and validator when you need more than two or three categories.
- Never rely on color alone for identity: pair it with a direct label.
- Red/green as the only distinction is a failure for many viewers. Use blue/orange and a label.

## Labels, titles, and sources

- **Title**: the takeaway sentence, in the slide title. The chart itself can carry a short descriptor (what and unit) in small text.
- **Direct labels**: label lines at their right end and bars at their end. Remove the legend if every series is directly labeled.
- **Units and period** on the axis or in a subtitle: "Late-delivery rate, % of orders, monthly".
- **Source line** below every data chart: dataset, filter, date range, n.
- **Annotation**: one callout at most that explains an important point (a policy change, an outlier). Do not annotate every point.

## Uncertainty

When the claim depends on a difference being real, show the spread. Error bars,
confidence bands, or an interval dot plot say "this is how sure we are" without
words. Gaps in the data should show as gaps. If the intervals overlap heavily,
the title must not claim a clear winner.

For forecasts and backtests, show out-of-sample results separately from in-sample,
and show results net of costs if money is involved.

## Charts for data-science results

Translate each technical chart for the audience instead of pasting the default plot.

| Technical output | For a non-technical audience | For technical reviewers |
|---|---|---|
| Confusion matrix | Counts or dollars of each outcome: "caught 71 of 100 late orders, 12 false alarms per 100 flagged" | Matrix with normalized rates and class balance noted |
| ROC or PR curve | A single operating point: "at this threshold we flag 20% of orders and catch 71% of late ones" | Curve with the chosen threshold marked, baseline line, AUC with interval |
| Feature importance | Top 5 drivers in plain words, direction marked ("longer handling time increases delay") | Importance with method named (permutation, SHAP) and caveats on correlated features |
| Model metric table | Chosen model vs current process in a business unit | Table with baselines, intervals, and the split described |
| Calibration | "When we say 70% risk, about 7 in 10 are late" | Reliability curve |
| Lift or gain | "Targeting the top 10% of scores reaches 3x more at-risk orders" | Cumulative gains vs random |
| Residuals or errors | Where the model is typically off and by how much, in units | Residuals vs fitted, by segment |
| Clusters | Named segments with one distinguishing fact each | Projection plus validation of cluster stability |

## Slide-size specs

- 16:9. Export raster charts at about 200 dpi at the size they will appear.
- Chart text no smaller than 12pt at final size; axis and data labels 12-14pt, title text larger.
- One main chart per slide. Two small charts side by side only when comparing the same measure across two groups with identical scales.
- Leave breathing room; the chart should fill most of the body area, not sit in a corner.
- Add alt text: one sentence saying what the chart shows ("Bar chart: the north region's delay is 3.1 days above average, the largest of nine regions").
- Do not paste screenshots of notebook output or dashboards with tiny text. Recreate the chart cleanly.

## Checklist

- [ ] The title states the takeaway and the chart shows exactly that
- [ ] Right chart type for the question; no dual axis, no 3D, no pie with many slices
- [ ] Bars start at zero; axes have units; period stated
- [ ] One accent color on the point, context in grey; meaning consistent across the deck
- [ ] Direct labels; no legend if avoidable; no clutter
- [ ] Uncertainty shown where the claim needs it
- [ ] Source line with n and date range
- [ ] Text 12pt or larger at slide size; alt text added
