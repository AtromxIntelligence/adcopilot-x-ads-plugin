# AdCopilot for X Ads (Twitter Ads)

X Ads (Twitter Ads) help in your AI client, through AdCopilot. This plugin gives
Claude the steps to check your X Pixel in Google Tag Manager, to read X traffic and
conversions in Google Analytics (GA4), and to plan and write for X Ads. It works
through the AdCopilot connector, which reaches your Google products.

Made by Atromx Intelligence (https://adcopilot.cloud). Not affiliated with or endorsed by X Corp. X and Twitter are trademarks of X Corp. Not related to other products named AdCopilot.

## What it does today

- **Checks your X Pixel in Google Tag Manager** (`gtm_list_accounts`,
  `gtm_list_containers`, `gtm_list_workspaces`, `gtm_list_tags`,
  `gtm_list_triggers`, `gtm_list_version_headers`). It finds X's base code and event
  code in your tags, says which pixel id and which trigger they use and whether they
  sit in a draft, and names the proof that the pixel fires: X's Events Manager, the X
  Pixel Helper and Tag Manager's Preview. When you paste the code from your own
  Events Manager, it proposes a Custom HTML tag and a thank-you-page trigger and, on
  your yes, stages them (`gtm_create_trigger` and `gtm_create_tag`, with
  `gtm_list_built_in_variables` and `gtm_enable_built_in_variable` for the Page Path
  variable the trigger reads). Staged means in a workspace named AdCopilot, never
  published.
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
  with no tool.

## What comes later

Every skill and command opens with this, once:

> Today this plugin checks your X Pixel and tags in Google Tag Manager, reads X traffic and key events in Google Analytics (GA4), checks UTM tags, guides conversion setup, plans campaigns, drafts post copy and does the budget pacing math. It does not read your X ad account.

Reading your X ad account is not part of this plugin, and nothing in it pretends
otherwise.

## Plans

The plugin is free (MIT). The AdCopilot connector is a hosted service: Free plan available; paid plans on https://adcopilot.cloud/pricing

## Install

**Claude on the web, Cowork and the desktop app.** Open Customize, then Plugins,
search for AdCopilot for X Ads, and Add it. Then open the plugin's Connectors tab,
Connect `adcopilot`, and sign in.

**Claude Code.** Run `/plugin marketplace add AtromxIntelligence/adcopilot-x-ads-plugin`,
then `/plugin install adcopilot-x-ads@adcopilot-x-ads-plugin`, then `/mcp` to sign in
to `adcopilot`.

**Then, once,** connect your Google products in AdCopilot at https://app.adcopilot.cloud.
For this plugin that is Google Tag Manager and Google Analytics. Which containers and
properties the plugin can see depends on the Google login you connect.

## Already use another AdCopilot plugin?

There is one connector and one AdCopilot account, whichever AdCopilot plugins you
add. Every AdCopilot plugin points at the same address, so your AI client treats
them as one connector. In Claude Code, `/mcp` shows the connector once, under
whichever AdCopilot plugin loaded first, and the sign-in belongs to that entry. If
Claude asks you to sign in again after you add or remove an AdCopilot plugin, run
`/mcp` and sign in once.

## What you get

Three commands. `setup` checks the connector and says what is connected, `check` follows the `x-ads-tracking` skill, and `plan` follows the `x-ads-plan` skill. In Claude Code they are named `/adcopilot-x-ads:setup`, `/adcopilot-x-ads:check` and `/adcopilot-x-ads:plan`.

Four skills. `x-ads-tracking` is the X Pixel check and staging, `x-ads-traffic` is X traffic, key events and UTM mistakes in Analytics, `x-ads-plan` is the campaign plan and post drafts, and `x-ads-budget` is budget pacing, with no tool. The tools each one uses are the ones named above, and every skill that uses a tool starts with `get_org_context`.

Every figure it shows from Analytics is the tool's figure. A figure you give it is labelled as yours.

## What it will not do

- Read your X ad account, or state an X click, impression or spend figure it was not
  given.
- Publish Tag Manager. Staged tags wait for your own Submit and Publish.
- Delete anything.
- Change anything without your explicit yes, after it has told you what the change
  is and how to undo it.
- Set up X's server-side Conversion API, create or change a campaign on X, check your
  ads against X's ad policies, or promise a result.

## Data

The plugin is instructions only: it runs no code and sends nothing anywhere itself. The AdCopilot connector at mcp.adcopilot.cloud reads and, on your yes, writes your Google products through Google's APIs with your Google sign-in.

The plugin never contacts X. A tag you publish that loads X's pixel script from
static.ads-twitter.com does so from your own site, in your visitors' browsers, because
you chose to install it. The links in this plugin's answers to X's and Google's help
pages are for you to read. Privacy policy: https://adcopilot.cloud/privacy. Terms:
https://adcopilot.cloud/terms. Documentation: https://adcopilot.cloud/docs/.

## Support

Open an issue at https://github.com/AtromxIntelligence/adcopilot-x-ads-plugin/issues,
or write to support@adcopilot.cloud.

## Version

**0.1.1 (2026-10-26, written against AdCopilot v2.44.0, live since 2026-10-22)**: text only. The sentence about your X ad account, which every skill and command opens with, now says only: it does not read your X ad account. The skills, the commands, the tools they name and the connector are as in 0.1.0.

**0.1.0 (2026-10-23, written against AdCopilot v2.44.0, live since 2026-10-22)**: the first release. Three commands and four skills for X Ads: the X Pixel check and staging in Google Tag Manager, X traffic and key events in Google Analytics (GA4) with UTM checks, campaign plans and post drafts, and budget pacing math. It reads no X ad account. X's help pages were checked on 23 October 2026.

## Licence

MIT. See the LICENSE file.

## What CI runs

Two GitHub Actions workflows run on every push to main and every pull request, and neither holds a secret. `checks` installs Claude Code at a pinned version from npm, runs plugin validation in strict mode on the plugin folder and its manifest, parses the three JSON files, checks that every skill and command has a name and a description, runs the plugin's tests, looks for a download-and-execute pattern anywhere in the repository, and checks that the manifest version is not behind the latest tag. `leak-check` runs gitleaks over every commit, from an image pinned by digest.

The tests use only the Python standard library and read no environment variable. Run them from the repository root with `python3 -m unittest discover -s tests -v`.
