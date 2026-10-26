---
name: setup
description: Check the AdCopilot connector is signed in, say which Google products are connected for X Ads work (Tag Manager and Analytics), and say what this plugin does today.
---

Open your first answer with this, in these words, once:

> Today this plugin checks your X Pixel and tags in Google Tag Manager, reads X traffic and key events in Google Analytics (GA4), checks UTM tags, guides conversion setup, plans campaigns, drafts post copy and does the budget pacing math. It does not read your X ad account.

Then call `get_org_context` with `source: "claude-plugin/adcopilot-x-ads/0.1.1"`, before
any other tool. Send `source` exactly as written. In a scheduled run send
`source: "claude-scheduled"` instead, read only, and change nothing.

`get_org_context`'s `next_step` and `playbook` describe the whole workspace, not this
request. Do this request, keep any limit `next_step` adds, and offer the rest
afterwards.

Report, from what the server returns and nothing from memory:

- **Google Tag Manager** and **Google Analytics 4**, the two products this plugin
  works from: connected or not. For one that is not, say what connecting it unlocks
  in the server's own words (its `unlocks`) and give its `connect_url`. For one that
  needs to be signed in again or added again, say what its `next_step` says.
- That the Google products are connected inside AdCopilot at
  `https://app.adcopilot.cloud`, not in this AI client. A sign-in that reports
  nothing connected is the server working, not a fault.

If the connector does not answer, it is a sign-in. In Claude Code, run `/mcp` and sign
in to `adcopilot`. In Claude on the web, in Cowork or in the desktop app, open this
plugin, then its Connectors tab, and connect `adcopilot` there. There is one
connector and one AdCopilot account whichever AdCopilot plugins are added. In
Claude Code, `/mcp` lists it once, under whichever AdCopilot plugin loaded first,
and the sign-in belongs to that entry. If Claude asks for a sign-in again after an
AdCopilot plugin was added or removed, run `/mcp` and sign in once.

End with the one next step that fits: the `check` command to check the X Pixel in Tag
Manager, or the `plan` command to plan a campaign and draft its posts.
