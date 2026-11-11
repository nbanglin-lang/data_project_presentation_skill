# Translating metrics, uncertainty, and limits

Accuracy, precision, recall, and error measures mean something to the person who
built the model and little to the person who has to decide. A model's value to a
business is measured in business terms: money, time, risk, customers. Accuracy
and error metrics alone also fail to tell the whole story of a model, because
they hide its risks, strengths, and limitations, which leaves decision-makers
unable to feel confident using it. This file covers how to close that gap.

## Contents
- From metric to business language
- Pick the few metrics that matter
- Always give a baseline
- Showing uncertainty without jargon
- Limitations: the lexicon
- Presenting bad, modest, or inconclusive results
- A model-card slide

## From metric to business language

Start from the decision the model supports and ask what a mistake costs.

| Technical statement | Business statement |
|---|---|
| Recall of 0.71 for late orders | We catch 71 of every 100 orders that would have arrived late |
| Precision of 0.62 | When we raise a flag, about 6 in 10 are truly at risk; 4 in 10 are false alarms |
| RMSE of 1.8 days | Our delivery estimate is typically off by under two days |
| AUC of 0.84 | The model ranks a truly late order above an on-time one 84% of the time |
| 12% lift in conversion in test | About 1,300 more purchases a month at current traffic, assuming the test effect holds |

For each result, write the "so what chain": technical fact, what it means for the
process, what that means for the business metric, what action follows. If you
cannot complete the chain, the result is not ready for a decision-maker slide.

Show the impact calculation: assumption times volume gives impact. Give a range
when an assumption is soft. If the impact is only an estimate, label it as one.

## Pick the few metrics that matter

Choose the two or three metrics tied to the stated business objective and present
only those on main slides. Everything else goes to the appendix. Overwhelming the
audience with many technical metrics is a common way to lose them.

- Imbalanced outcomes: accuracy can look excellent while the model misses what matters. Use recall, precision, or cost-weighted outcomes, and say what a miss and a false alarm each cost.
- Rankings and targeting: use lift or "top 10% captures X%".
- Forecasts: use error in the units of the thing forecast, and compare with the naive forecast.

## Always give a baseline

A number without a comparison has no meaning. State what the model is compared
with: the current process, a simple rule, the previous period, the majority
class, last-value forecast. "Beats the current rule by 33 points" is a claim;
"71% recall" is a number.

## Showing uncertainty without jargon

- "Our best estimate is 1,200 orders a quarter, and the plausible range is 800 to 1,600."
- "The two models are statistically indistinguishable on this data, so we would pick the simpler one."
- Prefer ranges and intervals on charts to p-values on slides. Put the test details in the notes or appendix.
- When data is limited, say how many records the result rests on.

## Limitations: the lexicon

Rank limitations by how much each could change the conclusion. For each one: what
it is, why it matters, and what would address it. Plain-language framings:

| Limitation | Plain wording | Mitigation to mention |
|---|---|---|
| Small or unrepresentative sample | The result rests on 400 customers in one city and may not hold elsewhere | Test on another region or period |
| Data drift | Customer behavior changes; a model trained on last year's data will slowly get worse | Retrain quarterly; monitor three business metrics |
| Correlation not causation | Orders from these sellers are late, but we have not shown the sellers cause it | Run a pilot or controlled test |
| Leakage or look-ahead risk | Make sure no information from the future was used to predict the past | State how the split was done |
| Survivorship bias | We only see customers who stayed long enough to appear in the data | Include churned records |
| Proxy labels | We measure complaints, which understate actual dissatisfaction | Add a survey sample |
| Outlier sensitivity | A few very large orders move the average; results are shown with and without them | Report medians as well |

Structured format that works for model behavior: Situation (when), Behavior (what
the model does), Impact (what it means for the business).

## Presenting bad, modest, or inconclusive results

A negative result that changes a decision is valuable. Do not bury it, and do not
dress it up.

1. State plainly what was tested and that it did not meet the success criterion.
2. Say what you learned (what the data does and does not support).
3. Say what it means for the decision (stop, pivot, narrower pilot, collect different data).
4. Give the next step with its cost.

An honest title: "The model does not beat the current rule enough to justify rollout; a narrower pilot on high-risk sellers might."

## A model-card slide

For the appendix, or main deck if the audience will operate the model:

- Purpose and intended use; who should not use it for what
- Training data: source, period, size
- Evaluation: method, headline metrics against baseline
- Performance by segment, with the worst segment named
- Known failure modes and limitations
- Monitoring and retraining plan; owner
