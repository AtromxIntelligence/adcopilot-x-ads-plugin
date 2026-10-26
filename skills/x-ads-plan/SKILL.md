---
name: x-ads-plan
description: Plan an X Ads (Twitter Ads) campaign and draft promoted-post copy, covering the objective, the audience by keywords, follower look-alikes and interests, the conversion to count, post text within 280 characters and website-card headline variants. Claude writes it from what the customer says, and AdCopilot reads no X data for it. Use when the user asks to plan, write, brainstorm or draft X ads, Twitter ads, promoted posts, post copy, headlines or an X campaign.
---

# X Ads campaign plan and post drafts

The customer wants a plan for an X Ads campaign, or copy for its posts. The plan
and the copy are Claude's own work, written from what the customer tells you.
AdCopilot reads no X data for this: it has no access to the customer's X ad
account, and nothing here says how any X campaign performed.

## Your first answer

Open your first answer in this conversation with this, in these words, once. Do
not repeat it in later answers.

> Today this plugin checks your X Pixel and tags in Google Tag Manager, reads X traffic and key events in Google Analytics (GA4), checks UTM tags, guides conversion setup, plans campaigns, drafts post copy and does the budget pacing math. It does not read your X ad account.

## Start

Call `get_org_context` with `source: "claude-plugin/adcopilot-x-ads/0.1.1"` first,
before any other tool, and read only what its saved `profile` says about the
customer's business: what they sell, where, and to whom. Send `source` exactly as
written. In a scheduled run (a Claude scheduled task or routine with nobody there
to answer; this plugin schedules nothing, but one may exist) send
`source: "claude-scheduled"` instead, read only, and change nothing.

`get_org_context`'s `next_step` and `playbook` describe the whole workspace, not
this request. Do this request, keep any limit `next_step` adds, and offer the rest
afterwards. This plan needs no Google product: if nothing is connected, carry on.
If the profile is empty, ask.

## Ask, one question at a time

What they want to promote, who it is for and where, the goal (visits to a page,
leads or sales), the page the ad sends people to, the budget they choose, in their
own currency, and the dates. Never propose a figure they did not name. Use only
facts they gave you or the profile holds.

## Build the plan

1. **Objective and the conversion to count.** Say which action on the site counts
   as the result. It can be counted only if the X Pixel records it, so if you do not
   know that the pixel is installed, offer the `x-ads-tracking` skill before launch.
2. **Audience.** From X's help pages on targeting, checked 23 October 2026:
   - Keywords. X recommends a mix of at least 25 relevant keywords. A hashtag
     version is included automatically, punctuation is not supported, and a
     keyword matches posts with the words in any order, including related terms,
     synonyms, misspellings and slang. Keywords can be included or excluded, and X
     warns that excluding too many narrows the audience. X prohibits keywords that
     involve sensitive categories. Draft a keyword list from the customer's own
     words: broad and specific terms, and a short exclude list.
   - Follower look-alikes. People similar to the followers of the accounts the
     customer names. X's tips: around 30 accounts per campaign, accounts closely
     tied to the business, and a separate campaign for accounts and for interests.
     Ask the customer which accounts they follow or compete with. You cannot look an
     account up, so suggest kinds of account to look for, never a name you cannot
     verify.
   - Interests. X offers a list of interest categories (82 when checked). Choose the
     ones that line up with the posts. X's audience estimate and its own targeting
     screen are the referee.
3. **Copy.** Write three post variants and three headline variants, each with its
   character count.
   - Post text is at most 280 characters. X's creative specs page, checked 23
     October 2026, says each link counts as 23 characters, which leaves 257 for the
     words when there is one link.
   - A website card headline is at most 70 characters. X says up to two lines
     show, and that about 50 characters usually avoids truncation.
   - For an image with a website card, X recommends 800 x 418 pixels at 1.91:1 or
     800 x 800 at 1:1, and its page lists 4:5, 2:3, 16:9 and 9:16 as supported
     ratios too. X notes that not every format is open to self-serve advertisers.
   Count with care. If you cannot count a line exactly, say "about". X's preview is
   the referee for how a post looks.
4. **Rules for the words.** Claim only what the customer told you. Never invent a
   price, an offer, a statistic, a review or a result, and never promise one. X
   reviews ads against its own ad policies, which you cannot check: tell the customer
   to read them before they launch.
5. **Tracking links.** The destination link carries UTM tags so the visits can be
   told apart in Analytics. Offer the tagging in the `x-ads-traffic` skill.
6. **Budget.** The customer's figure, said back in their currency. Offer the
   `x-ads-budget` skill for pacing.

Give the plan as a short document: objective, conversion to count, audience (keywords,
accounts, interests), the post and headline variants with counts, the link with its
UTM tags, the budget as the customer gave it, and what to look at in X's preview.

## What this does not do

It creates nothing in X: AdCopilot cannot reach the customer's X ad account, so
the customer builds the campaign in X's ads account from this plan, and X's own
screens are the referee for every setting. Say that plainly once the plan is given.

Every change is proposed first, with what it changes and how to undo it, and is applied only after the customer's explicit yes in this conversation. This skill makes no change anywhere, and deletes nothing.
