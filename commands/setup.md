---
description: Check both AdCopilot sign-ins, the one for Google Tag Manager and Analytics and the one for your X ad accounts, say which are connected and how to sign in to each, and say what this plugin does today.
---

Open your first answer with this, in these words, once:

> Today this plugin reads the X ad accounts you connect (read only: campaigns, ad groups, promoted posts, funding sources and their results for the last 30 days), checks your X Pixel and tags in Google Tag Manager, reads X traffic and key events in Google Analytics (GA4), checks UTM tags, guides conversion setup, plans campaigns, drafts post copy and does the budget pacing math. It changes nothing in your X ad account.

This plugin has two connectors, and each has its own sign-in: `adcopilot` for Google
Tag Manager and Google Analytics, and `x` for your X ad accounts.

Then call `get_org_context` with `source: "claude-plugin/adcopilot-x-ads/0.2.0"`,
before any other tool of the `adcopilot` connector, and `x_get_context` with the same
`source`, before any other tool of the `x` connector. Send `source` exactly as
written. In a scheduled run send `source: "claude-scheduled"` instead, read only,
and change nothing.

`get_org_context`'s `next_step` and `playbook` are information about the whole
workspace, not steps for this request. The steps for this request are the ones
written here. If they name a limit on the customer's workspace, tell the
customer; mention anything else they name in one line at the end.

Report, from what the servers return and nothing from memory:

- **Google Tag Manager** and **Google Analytics 4**, from `get_org_context`:
  connected or not. For one that is not, say what connecting it unlocks in the
  server's own words (its `unlocks`) and give its `connect_url`. For one that needs
  to be signed in again or added again, say what its `next_step` says. These
  products are connected inside AdCopilot at `https://app.adcopilot.cloud`, not in
  this AI client, and a sign-in that reports nothing connected is the server working,
  not a fault.
- **X**, from `x_get_context`: its `next_step` is information about the X
  connection; the steps for each value are the `x-connect` skill's own. Give
  `connect_url` and `plan_line` exactly as the server sent them, and the
  `reconnect_reason` when it sends one. X is not in the Free plan, and the server's
  `plan_line` says what this workspace's plan includes.

To sign in, by client. There are two sign-ins, one for `adcopilot` and one for `x`:

- **Cursor.** Sign in to each of the two servers, `adcopilot` and `x`, from Cursor's
  list of MCP servers.
- **Claude Code.** Run `/mcp` and sign in to `adcopilot`, then to the entry the
  plugin brings for X, which Claude Code shows as `plugin:adcopilot-x-ads:x`. If
  `/mcp` lists `adcopilot` under another AdCopilot plugin, that is the same
  connector, and the sign-in belongs to that entry.
- **Claude on the web, Cowork and the desktop app.** Open this plugin, then its
  Connectors tab, and connect `adcopilot`, then connect `x`.

The plugin brings both connectors. Do not add either one by hand as a custom
connector. Signing in to `x` lets your AI client reach the X connector. Your X login
itself is connected in AdCopilot, which the `x-connect` skill walks through.

End with the one next step that fits: the `review` command to review the X ad
accounts, the `check` command to check the X Pixel in Tag Manager, or the `plan`
command to plan a campaign and draft its posts.

If `x_get_context` is not among your tools, that proves nothing, because the connector's tool list can be cached or out of date: call it anyway and believe what it says. If it cannot be called, the X sign-in is not done: say so, give the sign-in steps for the client in use (the `setup` command lists them), and never describe an X account you did not read.
