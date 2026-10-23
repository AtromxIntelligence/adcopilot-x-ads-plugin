---
name: x-ads-budget
description: Work out budget pacing for an X Ads (Twitter Ads) campaign from the customer's own figures, giving the projected spend, the daily amount that lands on budget and whether spend is over or under pace. Claude does the math itself and AdCopilot reads no X data for it. Use when the user asks about X ads budget, pacing, whether they are overspending or underspending on X, how much to spend per day, or what a month of X ads will cost.
---

# X Ads budget pacing

The customer wants to know whether an X Ads campaign is on pace for its budget. The
math is Claude's own, done on the figures the customer gives you. AdCopilot reads no
X data for this: it has no access to the customer's X ad account, and this skill calls
no AdCopilot tool at all.

## Your first answer

Open your first answer in this conversation with this, in these words, once. Do
not repeat it in later answers.

> Today this plugin checks your X Pixel and tags in Google Tag Manager, reads X traffic and key events in Google Analytics (GA4), checks UTM tags, guides conversion setup, plans campaigns, drafts post copy and does the budget pacing math. It does not read your X ad account: direct access to it comes when X approves AdCopilot's API access, and there is no date yet.

## Ask for the figures

One question at a time, and only the ones you still lack:

1. The budget for the period, in the customer's currency. It can be a total, or a
   daily amount and the number of days.
2. The dates of the period: its first day, its last day, and what today's date is.
3. The spend so far, read from X's ads account for those dates, and whether it
   includes today.

Name the currency and say it back. Never convert one currency into another. Never
state a spend figure you were not given, and label every figure "from you". X's
ads account has its own time zone, which sets where a day ends, so use the day
boundaries as the customer reads them there.

## The math

Let B be the budget for the period, D the days in the period, d the days elapsed
and S the spend so far. Count a day only when its spend is in S, and say how you
counted today.

- Even-pace spend to date: B x d / D.
- Pace: S divided by the even-pace spend to date. Above 100 percent is ahead of
  pace, below is behind.
- Projected spend at the current run-rate: S / d x D.
- Projected gap: the projection minus B. Positive is over budget, negative is under.
- Daily amount that lands on budget from here: (B - S) / (D - d), when days remain.
- Compare that daily amount with the run-rate so far, S / d, and with the daily
  budget the customer has set, if they told you one.

Edge cases, said plainly:

- No days elapsed (d is 0): there is no run-rate. Say so, and give only the daily
  amount that spreads the budget over the period, B / D.
- S is at or above B: nothing is left. Say the budget is spent, or by how much it is
  over, and give no daily amount.
- No days remain (D equals d): the period is over. Give the final gap.
- A budget changed part-way, or days with the campaign paused: ask for the dates
  and work each stretch on its own, or say that the projection ignores it.

Round to the unit the customer uses for the currency. Show the working in a short
table, inputs first and each result beside its formula, then give the verdict in one
sentence.

## What the projection is not

A run-rate is a straight line. Real spend is rarely flat: it moves with the day of
the week, with how long a campaign has run and with its end date. Say so beside the
projection. X's own reporting is the referee for what was spent. The daily amount
that lands on budget is the customer's to set in X's ads account, and this plugin
cannot set it.

## End

Offer one next step. If the pace is off, offer to rework the plan with the
`x-ads-plan` skill, or the tracking check in the `x-ads-tracking` skill if they
doubt the results the spend is buying.

Every change is proposed first, with what it changes and how to undo it, and is applied only after the customer's explicit yes in this conversation. This skill makes no change anywhere, and deletes nothing.
