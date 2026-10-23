---
name: x-ads-traffic
description: Read X (Twitter) traffic and key events in Google Analytics (GA4) by source, medium and campaign, and find UTM mistakes in the links that send people from X. Use when the user asks how X Ads or Twitter Ads traffic did in Analytics, how many visits or conversions came from X or Twitter, why t.co shows up in their sources, which X campaign worked, or whether their UTM tags are right.
---

# X traffic in Google Analytics

The customer wants to know what X sent to their site, as Google Analytics (GA4)
counts it. This skill reads their Analytics property through the AdCopilot
connector at `https://mcp.adcopilot.cloud/mcp`. It reads Analytics only. AdCopilot
has no access to the customer's X ad account, so it has no X clicks, impressions
or spend, and it never states one.

## Your first answer

Open your first answer in this conversation with this, in these words, once. Do
not repeat it in later answers.

> Today this plugin checks your X Pixel and tags in Google Tag Manager, reads X traffic and key events in Google Analytics (GA4), checks UTM tags, guides conversion setup, plans campaigns, drafts post copy and does the budget pacing math. It does not read your X ad account: direct access to it comes when X approves AdCopilot's API access, and there is no date yet.

## Start

Call `get_org_context` with `source: "claude-plugin/adcopilot-x-ads/0.1.0"` first,
before any other tool. Send `source` exactly as written. In a scheduled run (a
Claude scheduled task or routine with nobody there to answer; this plugin
schedules nothing, but one may exist) send `source: "claude-scheduled"` instead,
read only, and change nothing.

`get_org_context`'s `next_step` and `playbook` describe the whole workspace, not
this request. Do this request, keep any limit `next_step` adds, and offer the rest
afterwards.

If the card for Google Analytics 4 under `products` is not connected, say what
connecting it unlocks, in the server's own words (its `unlocks`), give its
`connect_url`, and stop. If the card says it needs to be signed in again or added
again, say what its `next_step` says and stop. Never give a link from memory, and
never describe traffic you cannot read.

## Read the numbers

1. `ga4_list_account_summaries`. Pick the property for the customer's site. If
   there is more than one, ask, by display name.
2. `ga4_get_metadata` for the property, and check that the names you are about to
   use exist there: the dimensions `sessionSource`, `sessionMedium`,
   `sessionCampaignName` and `sessionDefaultChannelGroup`, and the metrics
   `sessions`, `keyEvents` and `totalRevenue`. Where the property's list names
   one differently, use the list's name and say so.
3. `ga4_list_conversion_events` for the property. Analytics now calls these key
   events, and the tool lists them as conversion events. If none is marked, the
   key-event counts will be zero because of the setup and not because X sent
   nothing: say that. Marking an event is the customer's step in Analytics, and
   this skill does not make it.
4. `ga4_run_report` with those four dimensions and three metrics, for the dates the
   customer names. With none named, use the last 28 days (`start_date`
   `28daysAgo`, `end_date` `today`) and say so. The tool has no filter, so choose
   the X rows yourself from the rows it returns: a source of `t.co`, `x.com`,
   `twitter.com`, `twitter` or `x` (ignore capital letters), and any source or
   campaign the customer says they use for X. Compare the report's `rowCount` with
   the rows you received, and say so if rows were cut off.

Show the rows as a table with the source, medium, campaign, channel group,
sessions, key events and revenue, and put "Google Analytics (GA4), through
AdCopilot" beside it as its source. The dates and the property's time zone are
Analytics's own: name the period. A revenue of zero can mean the site sends no
purchase value to Analytics, so say what it can mean before you call it a result.
The numbers are the tool's. Never write one it did not return.

## What X rows tell you

- X shortens the links shared on X into its own t.co links (X's help page "About
  X's link service", checked 23 October 2026), so a visit from an untagged link
  usually arrives with `t.co` as its source. Without UTM tags, Analytics cannot
  tell which post, ad or campaign sent it, nor a click on an ad from a click on an
  ordinary post. Rows whose source is `t.co` and whose campaign is not set are
  that. What a given ad's clicks look like is whatever its rows say, and the rows
  are the referee.
- Rows with a campaign name are the links that carried UTM tags. Read them by
  campaign, and say which campaigns have key events and which have visits only.
- A gap between X's clicks and Analytics's sessions is normal, and this plugin
  cannot size it: it has no X numbers. If the customer pastes figures from X's ads
  account, label them "from you, X Ads", keep them apart from Analytics's, and
  compare in words, never in one merged number.

## UTM mistakes to look for in the rows

Name each one you see, with the rows as evidence. Do not list a mistake the rows do
not show.

- The same campaign spelled several ways (spaces, hyphens, underscores or capital
  letters), which splits one campaign over several rows.
- The same platform under two sources, such as `x` and `twitter` or `X` and `x`.
  Either name works. Pick the one already in their history and keep it.
- X rows with no campaign, or with a medium of `referral`: untagged links.
- A medium that Analytics's default channel group does not count as paid. Google's
  help page "Default channel group", checked 23 October 2026, says a visit counts
  as Paid Social when its source is on Google's list of social sites and its medium
  matches `^(.*cp.*|ppc|retargeting|paid.*)$`, for example `paid_social` or `cpc`.
  It counts as Organic Social when the source is on that list, or the medium is
  `social` or a few close variants. Which sources are on Google's list is not
  known to this plugin, so the channel group column in the table is the referee:
  report where Analytics put the X rows.

Propose this tagging for each X campaign, as the customer's to put in the ad's
destination link, with their own campaign name in place of the angle brackets:

`?utm_source=x&utm_medium=paid_social&utm_campaign=<campaign>&utm_content=<ad or post label>`

Use `utm_medium=social` for ordinary posts, so they stay apart from ads. Keep every
value in lower case with no spaces. X's own preview shows the final link, and the
first week of data in this table shows which channel Analytics chose. Say that this
skill changes no link; the customer edits their ads in X.

## What this cannot see

X's clicks, impressions and spend. Visits that never reached Analytics, such as
those blocked by a visitor's consent choice or an ad blocker. Any X audience or
campaign setting. Say which of these matters to the question asked.

## End

Close with one next step. If key events are zero because none is marked, say so and
point to the customer's key-event setup in Analytics. If X rows show no tagging,
offer the tagging above. If the tag may not be firing, offer the `x-ads-tracking`
skill.

Every change is proposed first, with what it changes and how to undo it, and is applied only after the customer's explicit yes in this conversation. This skill makes no change in Analytics, Tag Manager or X, and deletes nothing.
