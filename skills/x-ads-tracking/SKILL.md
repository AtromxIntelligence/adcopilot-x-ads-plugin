---
name: x-ads-tracking
description: Check whether the X Pixel, the tag behind X Ads (Twitter Ads) conversion tracking, is set up in Google Tag Manager, name the proof that it fires, and stage the tag when the customer pastes X's code. Use when the user asks about the X Pixel, the Twitter pixel, X Ads or Twitter Ads conversion tracking, Events Manager, uwt.js, twq, X base code or event code, or whether their X tag fires.
---

# X Pixel check in Tag Manager

The customer wants to know whether their X Ads tracking is in place on their site.
This skill reads their Google Tag Manager through the AdCopilot connector at
`https://mcp.adcopilot.cloud/mcp` and, on their yes, stages tags there. AdCopilot
has no access to the customer's X ad account and reads no X figure; the pixel is
checked from the tags in Tag Manager, and what only X's own screens can show is
named below.

## Your first answer

Open your first answer in this conversation with this, in these words, once. Do
not repeat it in later answers.

> Today this plugin checks your X Pixel and tags in Google Tag Manager, reads X traffic and key events in Google Analytics (GA4), checks UTM tags, guides conversion setup, plans campaigns, drafts post copy and does the budget pacing math. It does not read your X ad account.

## Start

Call `get_org_context` with `source: "claude-plugin/adcopilot-x-ads/0.1.1"` first,
before any other tool. Send `source` exactly as written. In a scheduled run (a
Claude scheduled task or routine with nobody there to answer; this plugin
schedules nothing, but one may exist) send `source: "claude-scheduled"` instead,
read only, and change nothing.

`get_org_context`'s `next_step` and `playbook` describe the whole workspace, not
this request. Do this request, keep any limit `next_step` adds, and offer the rest
afterwards.

If the card for Google Tag Manager under `products` is not connected, say what
connecting it unlocks, in the server's own words (its `unlocks`), give its
`connect_url`, and stop. If the card says it needs to be signed in again or added
again, say what its `next_step` says and stop. Never give a link from memory, and
never describe a container you cannot read.

## What the X Pixel is

From X's help page "Conversion tracking for websites", checked 23 October 2026:

- The pixel has two parts. The base code goes on every page of the site. The
  event code records one action, such as a purchase or a lead, and needs the base
  code on the page.
- The base code loads `https://static.ads-twitter.com/uwt.js`, defines a function
  called `twq`, and calls `twq('config', '<pixel id>')`. The older address
  `platform.twitter.com/uwt.js` redirects to the same file (checked 23 October
  2026), so a tag that loads either is X's base code.
- Event code looks like `twq('event', 'tw-<pixel id>-<event id>', { ... })`, with
  optional parameters such as value and currency.
- An event can also be defined in X's Events Manager by URL rules, with no event
  code at all. A site with no event tags may still have events, and this check
  cannot see them.
- X offers a second route, the Conversion API, which sends events from a server
  and needs no tag on the page. If the customer uses only that, nothing here will
  show it.

## Read the container

1. `gtm_list_accounts`, then `gtm_list_containers` for the account. Pick the
   container that is on the customer's site. If there is more than one, ask, by
   display name. You cannot see their website, so say that the container is the
   one they named, not one you confirmed on the page.
2. `gtm_list_workspaces` for the container. Read the Default Workspace, any
   workspace the customer names, and the workspace named AdCopilot if there is
   one: it holds what AdCopilot staged earlier.
3. `gtm_list_tags` and `gtm_list_triggers` for each workspace you read.
4. `gtm_list_version_headers` for the container.

Find the X Pixel among the tags: a Custom HTML tag (type `html`) whose code holds
`static.ads-twitter.com/uwt.js` or a `twq(` call. X's own Tag Manager guide
describes Custom HTML tags. A tag built from a gallery template is possible too;
read its parameters the same way. When you cannot tell what a tag sends, say so
and send the customer to X's screens below.

Report each finding with its evidence (tag name, workspace, trigger name, as the
server returned them), and never a number or a name you did not read:

- **Base code.** Which tag carries it, in which workspace, and which pixel id its
  `config` call holds (quote the id only). If no tag carries it, say that no tag
  in the workspaces you read does. The code can also sit directly in the site's
  own pages, which Tag Manager cannot show, so do not say the pixel is missing.
- **More than one base tag for the same pixel id.** Ask which is meant. X's own
  instructions show the base code once per page.
- **Its trigger.** X says the base code belongs on every page. A tag that fires
  on Tag Manager's built-in All Pages trigger (id 2147479553) or Initialization -
  All Pages (id 2147479573) does. For a trigger of the customer's own, read its
  type and its filter and say what it does. A tag with no firing trigger does not
  fire on its own, and a tag marked paused does not fire either, if the tag shows it.
- **Event tags.** For each Custom HTML tag with `twq('event', 'tw-...` code: the
  event id, the pixel id, and the trigger. An event tag whose pixel id differs
  from the base tag's is a mismatch. An event tag with no base tag in the
  container is a gap: X's event code needs the base code on the page.
- **Draft or published.** The tags a workspace lists can include changes nobody
  has published. AdCopilot can list the container's versions (their names and
  ids, as the server returns them) but cannot open one to see its tags, and it
  has no tool that says which version is live. So it can say what a workspace
  holds and when the latest version was made, and it cannot prove a tag is live.
- **Consent.** If a tag shows a consent setting, say what it shows. AdCopilot
  cannot see the site's cookie banner or any visitor's choice.

## The proof that it fires

What you read is a list of tags. You did not watch a page load, so name the
proof, from X's help page, checked 23 October 2026, and at the time of writing:

- X's Events Manager, in the ads account at ads.x.com under Tools, shows each
  event's status: Active (activity in the last 24 hours), Inactive, or No recent
  activity. The base code's own events, "Site Visit" and "Landing Page View", are
  created for it. The status moves only after someone visits a tagged page. X
  says a missing Tools tab usually means no credit card has been added to the
  ads account.
- In Events Manager, an event's menu has View Activity, a Recent Activity Log
  with a sample of the data X received, the parameters sent and the host name of
  the site that sent them.
- X also lists the X Pixel Helper, a Google Chrome extension that shows the
  pixel's tracking status and error codes.
- Tag Manager's own Preview mode shows which tags fired on a page (at the time of
  writing).

AdCopilot cannot see any of these. Say so, and say which one to open first.

## When the customer pastes X's code

Staging a tag is a change, so it follows the rule at the end of this skill.

- Use only what the customer pastes from their own Events Manager. Never type,
  complete or correct a base code or an event code from memory or from this
  skill, and never supply a pixel id you were not given.
- Read the paste before you propose anything. It should load X's script host and
  call `twq`. If it holds anything else, such as another script host or other
  inline code, say what and do not stage it: send the customer back to Events
  Manager for the code.
- Propose, in plain words. For the base code: one Custom HTML tag named "X Pixel
  base code" with the pixel id, firing on All Pages. For an event: one DOM Ready
  trigger (type `domReady`) on the thank-you page, with the page path the
  customer names, and one Custom HTML tag with the event code on that trigger.
  DOM Ready comes after Page View in Tag Manager, so the base code on All Pages
  has defined `twq` before the event code runs; a Page View trigger would race
  it. If the base tag fires later than Page View, say so and ask before you
  propose the trigger. Say that both are staged
  in a workspace named AdCopilot, that nothing fires until the customer reviews
  and publishes it in Tag Manager (Submit, then Publish, at the time of writing),
  and that to undo it they leave it unpublished or delete it in that workspace.
- The trigger's filter reads Tag Manager's built-in Page Path variable, which
  must be enabled in the workspace for the filter to work. Read
  `gtm_list_built_in_variables` first, for the workspace named AdCopilot if
  there is one, or else the Default Workspace. If Page Path is not enabled,
  include `gtm_enable_built_in_variable` for it in the same proposal.
- On their yes, make the trigger first with `gtm_create_trigger`, then the tag
  with `gtm_create_tag`: type `html`, the pasted code in the parameter `html`, the
  trigger's id as its firing trigger. If the container already has a Custom HTML
  tag, `gtm_list_tags` shows the parameter keys it uses; copy them.
- Read the result back with `gtm_list_tags` and `gtm_list_triggers` for the
  AdCopilot workspace (`gtm_list_workspaces` finds it) and report what you read.
  Do not say it works: the proof is Preview and X's Events Manager.
- X's page says a conversion type, such as Purchase, should be used once on a
  site, because several events of one type split the signal. Before staging a
  second event of a type already on the site, say so.
- Tell the customer the tag fires wherever its trigger does. If the site asks
  visitors for consent before advertising tags, their consent setup decides, and
  AdCopilot does not read it.
- Never publish, and never delete: there is no tool for either.

## Conversion event setup, in X's steps

From X's help page, checked 23 October 2026, and at the time of writing: in the
ads account, Tools, then Events Manager, then Add event source, and agree to X's
terms. X creates the base pixel. Then Add events: give the event a name, choose its
type (X lists Page view, Add to cart, Lead, Added payment info, Purchase and
Custom) and an attribution window. X recommends defining an event with code, and
says its parameters (value, currency, contents and others) work only for events
defined with code. Ticking a parameter box only makes a template, so the code must
pass the real values. If the customer uses both the pixel and the Conversion API,
X recommends the `conversion_id` parameter on both so X can match them.

Whether to pass an email address or a phone number in event code is the
customer's privacy decision; X's page describes it, and you propose none. Where X's
screen differs from this, X's screen is the referee.

## End

Close with one next step: when the base code is in place, offer the
`x-ads-traffic` skill to see whether visits and key events from X arrive in
Analytics.

Every change is proposed first, with what it changes and how to undo it, and is applied only after the customer's explicit yes in this conversation. A change to Tag Manager is staged in the AdCopilot workspace and never published. This skill deletes nothing.
