# AdCopilot for X Ads (Twitter Ads)

X Ads (Twitter Ads) help in your AI client, through AdCopilot. This plugin gives
Claude the steps to read the X ad accounts you connect, to review them, to check your
X Pixel in Google Tag Manager, to read X traffic and conversions in Google Analytics
(GA4), and to plan and write for X Ads. It works through two connectors: the AdCopilot
connector (`adcopilot`), which reaches your Google products, and the X Ads by AdCopilot
connector (`x`), which only reads your X ad accounts.

Made by Atromx Intelligence (https://adcopilot.cloud). Not affiliated with or endorsed by X Corp. X and Twitter are trademarks of X Corp. Not related to other products named AdCopilot.

## What it does today

- **Reads your X ad accounts, read only** (`x_get_context`, `x_ad_accounts`,
  `x_account_overview`, `x_campaigns`, `x_ad_groups`, `x_promoted_posts`,
  `x_funding_sources`): campaigns, ad groups, promoted posts, funding sources and
  their results for the last 30 days, under X's own metric names for each objective.
- **Reviews them** (`x_account_audit`, `x_budget_pacing`, `x_period_compare`,
  `x_wasted_spend`, `x_bidding_audit`): an audit, budget pacing, a period against the
  one before, spend with no results, and bids against the real cost. These are
  AdCopilot's own checks and arithmetic on X's figures, and they read nothing more
  from X.
- **Keeps X on its own.** X figures are never added to figures from any other source.
  Beside X traffic from Analytics it shows X's own figure of the same kind and names
  each source.
- **Checks your X Pixel in Google Tag Manager** (`gtm_list_accounts`,
  `gtm_list_containers`, `gtm_list_workspaces`, `gtm_list_tags`,
  `gtm_list_triggers`, `gtm_list_version_headers`). It finds X's base code and event
  code in your tags, says which pixel id and trigger they use and whether they sit in
  a draft, and names the proof that the pixel fires. When you paste the code from your
  own Events Manager, it proposes a Custom HTML tag and a thank-you-page trigger and,
  on your yes, stages them (`gtm_create_trigger` and `gtm_create_tag`, with
  `gtm_list_built_in_variables` and `gtm_enable_built_in_variable` for the Page Path
  variable). Staged means in a workspace named AdCopilot, never published.
- **Reads X traffic and key events in Google Analytics (GA4)**
  (`ga4_list_account_summaries`, `ga4_get_metadata`, `ga4_run_report`,
  `ga4_list_conversion_events`) by source, medium and campaign, and finds UTM
  mistakes: t.co rows with no campaign, one campaign spelled several ways, and a
  medium that Analytics does not group as paid.
- **Guides conversion setup** in X's Events Manager, from X's own help pages, checked
  23 October 2026.
- **Plans campaigns and drafts promoted-post copy.** This is Claude's own work and
  uses no tool beyond reading your saved business profile (`get_org_context`).
- **Does the budget pacing math** from the figures you give it. Claude's own work,
  with no tool. With X connected, the review reads the spend from X itself.

## What it does not read

Every skill and command opens with this, once:

> Today this plugin reads the X ad accounts you connect (read only: campaigns, ad groups, promoted posts, funding sources and their results for the last 30 days), checks your X Pixel and tags in Google Tag Manager, reads X traffic and key events in Google Analytics (GA4), checks UTM tags, guides conversion setup, plans campaigns, drafts post copy and does the budget pacing math. It changes nothing in your X ad account.

From X it never reads post text or media, audiences, demographics, locations,
targeting, other people's data or the description of a funding source. X results
cover the last 30 days. Spend for the last 3 days is X's estimate and can change for
up to 14 days.

## The connectors

The plugin is MIT licensed. The two connectors it brings, `adcopilot` and `x`, are
hosted services, so you need an AdCopilot account to use them.

X Ads is not part of Free. The X connector's own answer says what your workspace's
plan includes.

## Install

**Claude on the web, Cowork and the desktop app.** Open Customize, then Plugins,
search for AdCopilot for X Ads, and Add it. Then open the plugin's Connectors tab,
Connect `adcopilot` and `x`, and sign in to each.

**Claude Code.** Run `/plugin marketplace add AtromxIntelligence/adcopilot-x-ads-plugin`,
then `/plugin install adcopilot-x-ads@adcopilot-x-ads-plugin`, then `/mcp` to sign in
to `adcopilot` and to `x`, which Claude Code shows as `plugin:adcopilot-x-ads:x`.

The first time you sign in to `x`, AdCopilot's page asks you to let your AI client use
X Ads by AdCopilot. Press **Approve**.

**Then, once,** connect your Google products in AdCopilot at https://app.adcopilot.cloud.
For this plugin that is Google Tag Manager and Google Analytics. Which containers and
properties the plugin can see depends on the Google login you connect. Then connect
your X login on the AdCopilot dashboard, under Platforms: the `setup` command gives
you the link. Which X ad accounts the plugin can read depends on your role on each
one at X, and AdCopilot reads only the ones switched on there.

## Already use another AdCopilot plugin?

The `adcopilot` connector is one connector and one AdCopilot account, whichever
AdCopilot plugins you add. Every AdCopilot plugin points at the same address for it,
so your AI client treats them as one connector. In Claude Code, `/mcp` shows it once,
under whichever AdCopilot plugin loaded first, and the sign-in belongs to that entry.
If Claude asks you to sign in again after you add or remove an AdCopilot plugin, run
`/mcp` and sign in once. The `x` connector belongs to this plugin and has its own
sign-in.

## What you get

Four commands. `setup` checks both sign-ins and says what is connected, `review`
follows the `x-review` skill, `check` follows the `x-ads-tracking` skill, and `plan`
follows the `x-ads-plan` skill. In Claude Code they are named
`/adcopilot-x-ads:setup`, `/adcopilot-x-ads:review`, `/adcopilot-x-ads:check` and
`/adcopilot-x-ads:plan`.

Six skills. `x-connect` connects your X login and passes on the link, the plan line
and any reconnect reason exactly as the X connector sends them. `x-review` reviews
your X ad accounts. `x-ads-tracking`, `x-ads-traffic`, `x-ads-plan` and
`x-ads-budget` are the X Pixel check, X traffic in Analytics, the campaign plan and
budget pacing. Every skill that uses a tool starts with its connector's first call,
`get_org_context` or `x_get_context`.

Every figure it shows from Analytics is the tool's figure, and every figure from X is
X's. A figure you give it is labelled as yours.

## Example prompts

After you sign in, ask in your own words. For example:

- "Review my X ad account: where is the money going, and is it on pace?"
- "Compare my X results this period with the one before."
- "Is my X Pixel set up in Google Tag Manager, and how do I know it fires?"
- "How much traffic did X send to my site in Google Analytics, and are my UTM tags right?"
- "Plan a campaign for our launch and draft three promoted posts under 280 characters."

## What it will not do

- Change anything in your X ad account. The X connector only reads.
- Read post text or media, audiences, demographics, locations or targeting.
- Add X figures to figures from any other source.
- Publish Tag Manager. Staged tags wait for your own Submit and Publish.
- Delete anything. Its skills call no tool that deletes or removes, and neither
  connector has a tool that deletes in Tag Manager, Analytics or your X ad account.
- Change anything in Google without your explicit yes, after it has told you what the
  change is and how to undo it.
- Set up X's server-side Conversion API, create or change a campaign on X, check your
  ads against X's ad policies, or promise a result.

## Data

The plugin is instructions only: it runs no code and sends nothing anywhere itself. The AdCopilot connector at mcp.adcopilot.cloud reads and, on your yes, writes your Google products through Google's APIs with your Google sign-in.

The X Ads by AdCopilot connector at mcp.adcopilot.cloud/x/mcp reads your X ad accounts
with your own X sign-in, and changes nothing in X. AdCopilot keeps your X sign-in and
the ad accounts it reaches with your role on each, encrypted, and a 90-day log of
which tool ran, with no campaign data. Results are held encrypted for up to 15
minutes, then deleted. AdCopilot deletes your X sign-in at once when you disconnect
X Ads or ask us to, within 10 days if your seat is removed or your plan stops
including X Ads, within 3 weeks if the connection stops working and you do not
reconnect it, and within 90 days of its last use if you do not use it for 80 days. If
this X login is also connected in another of your AdCopilot workspaces, it stays
connected there.

When you ask your AI assistant, such as Claude or ChatGPT, AdCopilot passes these
results to it. It is made by a separate company: its terms and your settings there
decide how long it keeps them and whether it trains on them, and AdCopilot cannot see
or delete them there. X does not allow its data to be used to train AI models, so
before you ask your assistant about X Ads, turn off any setting that lets it train on
your conversations. AdCopilot is AI-powered: what your assistant says from X results
is AI-generated and may be wrong, so check it before you act on it. AdCopilot does
not train AI models on X data. How AdCopilot handles your X Ads data:
https://adcopilot.cloud/privacy#x-ads. How to connect X Ads and what each X tool
reads: https://adcopilot.cloud/docs/connect/x-ads/.

The plugin itself never contacts X. A tag you publish that loads X's pixel script from
static.ads-twitter.com does so from your own site, in your visitors' browsers, because
you chose to install it. The links in this plugin's answers to X's and Google's help
pages are for you to read. Privacy policy: https://adcopilot.cloud/privacy. Terms:
https://adcopilot.cloud/terms. Documentation: https://adcopilot.cloud/docs/.

## Support

Open an issue at https://github.com/AtromxIntelligence/adcopilot-x-ads-plugin/issues,
or write to support@adcopilot.cloud.

To report a security problem, write to support@adcopilot.cloud rather than opening a public issue.

## Version

**0.2.0 (2026-11-25, written against AdCopilot v2.46.45, live since 2026-11-25)**: adds the X Ads by AdCopilot connector (`x`, at https://mcp.adcopilot.cloud/x/mcp) beside `adcopilot`, with seven reads and five review tools for your X ad accounts, all read only. New skills `x-connect` and `x-review`, a new `review` command, and `setup` covers both sign-ins. The four 0.1 skills show X's own figure beside Analytics figures for X traffic, each source named, never added together. Results by day and by placement.

**0.1.2 (2026-11-05)**: text only. The plugin folder now holds only the files Claude loads. The skills take what AdCopilot suggests doing next as information and keep to their own steps, each skill's description names X Ads and AdCopilot, and this README says where to report a security problem.

**0.1.1 (2026-10-26, written against AdCopilot v2.44.0, live since 2026-10-22)**: text only. The sentence about your X ad account, which every skill and command opens with, now says only: it does not read your X ad account. The skills, the commands, the tools they name and the connector are as in 0.1.0.

**0.1.0 (2026-10-23, written against AdCopilot v2.44.0, live since 2026-10-22)**: the first release. Three commands and four skills for X Ads: the X Pixel check and staging in Google Tag Manager, X traffic and key events in Google Analytics (GA4) with UTM checks, campaign plans and post drafts, and budget pacing math. It reads no X ad account. X's help pages were checked on 23 October 2026.

## Licence

MIT. See the LICENSE file.
