"""The manifests: plugin.json, marketplace.json and .mcp.json.

The plugin directory reads plugin.json for the listing, and Claude Code reads
.mcp.json for the connector. This file holds the values the listing was decided
with, so a later edit cannot change one by accident:

* the plugin's name (permanent once published) and its display name;
* the author, the URLs and the licence;
* the keywords (at most 15, lower-case kebab-case);
* the icon, which must be a PNG and AdCopilot's own mark;
* .mcp.json, which is the same file, byte for byte, in every AdCopilot plugin.
  Claude Code connects one server per address, and Claude links a connector by its
  address, so the same address under the same key means one connection and one
  sign-in however many AdCopilot plugins are installed.

Stdlib only; it reads no environment variable. Run with
`python3 -m unittest discover -s tests -v` from the repository root.
"""

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

NAME = "adcopilot-x-ads"
REPO = "adcopilot-x-ads-plugin"
DISPLAY_NAME = "AdCopilot for X Ads (Twitter Ads)"
OWNER_NAME = "X"  # the platform: the description must say the plugin is not by it
NAME_PATTERN = re.compile(r"^[a-z0-9]([a-z0-9-]{0,62}[a-z0-9])?$")
KEYWORD_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")

# The same file, byte for byte, in every AdCopilot plugin.
CANON_MCP_TEXT = ('{"mcpServers":{"adcopilot":{"type":"http",'
                  '"url":"https://mcp.adcopilot.cloud/mcp"}}}')
CANON_MCP = {"mcpServers": {"adcopilot": {
    "type": "http", "url": "https://mcp.adcopilot.cloud/mcp"}}}

PLUGIN_KEYS = [
    "name", "version", "description", "author", "homepage", "documentationUrl",
    "privacyPolicyUrl", "termsOfServiceUrl", "supportUrl", "repository", "license",
    "keywords", "displayName", "icon",
]
URL_KEYS = ["homepage", "documentationUrl", "privacyPolicyUrl", "termsOfServiceUrl",
            "supportUrl", "repository"]


def load(relpath):
    return json.loads((ROOT / relpath).read_text(encoding="utf-8"))


class PluginJson(unittest.TestCase):

    def setUp(self):
        self.plugin = load(".claude-plugin/plugin.json")

    def test_the_fields_are_exactly_the_decided_set_in_the_decided_order(self):
        self.assertEqual(list(self.plugin), PLUGIN_KEYS)

    def test_name_display_name_and_author(self):
        p = self.plugin
        self.assertEqual(p["name"], NAME)
        self.assertRegex(p["name"], NAME_PATTERN)
        self.assertEqual(p["displayName"], DISPLAY_NAME)
        self.assertEqual(p["author"], {"name": "Atromx Intelligence",
                                       "url": "https://adcopilot.cloud"})
        self.assertEqual(p["license"], "MIT")

    def test_version_is_semver(self):
        self.assertRegex(self.plugin["version"], SEMVER)

    def test_urls(self):
        p = self.plugin
        for key in URL_KEYS:
            self.assertTrue(p[key].startswith("https://"), key)
        self.assertEqual(p["homepage"], "https://adcopilot.cloud")
        self.assertEqual(p["documentationUrl"], "https://adcopilot.cloud/docs/")
        self.assertEqual(p["privacyPolicyUrl"], "https://adcopilot.cloud/privacy")
        self.assertEqual(p["termsOfServiceUrl"], "https://adcopilot.cloud/terms")
        self.assertEqual(p["repository"], "https://github.com/AtromxIntelligence/" + REPO)
        self.assertEqual(p["supportUrl"], p["repository"] + "/issues")
        self.assertTrue(p["author"]["url"].startswith("https://"))

    def test_keywords(self):
        words = self.plugin["keywords"]
        self.assertLessEqual(len(words), 15)
        self.assertEqual(len(words), len(set(words)), "a keyword is repeated")
        for w in words:
            self.assertRegex(w, KEYWORD_PATTERN)
        self.assertIn("adcopilot", words)

    def test_description_is_keyword_led_short_and_honest_about_what_it_is(self):
        d = self.plugin["description"]
        self.assertLessEqual(len(d), 650, len(d))
        self.assertTrue(d.startswith("X Ads (Twitter Ads)"), d[:40])
        self.assertTrue(d.endswith("Made by Atromx Intelligence, not by %s." % OWNER_NAME), d[-60:])
        # The platform plugins say plainly what works today and what does not.
        self.assertIn("Today it", d)
        self.assertIn("It does not read your X ad account.", d)
        self.assertIn("proposed first and made only on your yes", d)

    def test_icon_is_a_png_and_is_the_adcopilot_mark(self):
        rel = self.plugin["icon"]
        self.assertEqual(rel, "./.claude-plugin/icon.png")
        data = (ROOT / rel).read_bytes()
        self.assertTrue(data.startswith(b"\x89PNG\r\n\x1a\n"))
        self.assertEqual(len(data), 12402, "the icon is the reference plugin's own mark")
        self.assertFalse((ROOT / ".claude-plugin" / "icon.svg").exists())


class McpJson(unittest.TestCase):

    def test_the_file_is_the_canonical_one_byte_for_byte(self):
        text = (ROOT / ".mcp.json").read_text(encoding="utf-8")
        self.assertEqual(json.loads(text), CANON_MCP)
        self.assertEqual(text.rstrip("\n"), CANON_MCP_TEXT)
        self.assertEqual(text, CANON_MCP_TEXT + "\n")

    def test_the_address_is_https_lower_case_with_no_query_and_no_trailing_slash(self):
        url = load(".mcp.json")["mcpServers"]["adcopilot"]["url"]
        self.assertTrue(url.startswith("https://"))
        self.assertEqual(url, url.lower())
        self.assertNotIn("?", url)
        self.assertFalse(url.endswith("/"))


class MarketplaceJson(unittest.TestCase):

    def test_it_names_the_plugin_with_source_dot_slash_and_no_listing_fields(self):
        m = load(".claude-plugin/marketplace.json")
        self.assertEqual(m["name"], REPO)
        self.assertEqual(m["owner"], {"name": "Atromx Intelligence",
                                      "url": "https://adcopilot.cloud"})
        self.assertEqual(len(m["plugins"]), 1)
        entry = m["plugins"][0]
        self.assertEqual(entry["name"], NAME)
        self.assertEqual(entry["source"], "./")
        self.assertEqual(entry["category"], "Marketing")
        # The directory's listing fields live in plugin.json, and the validator
        # reports them as unknown in a marketplace entry.
        listing = {"displayName", "icon", "keywords", "version", "author", "license",
                   "homepage", "privacyPolicyUrl", "documentationUrl",
                   "termsOfServiceUrl", "supportUrl", "repository"}
        self.assertEqual(listing & set(entry), set())
        self.assertEqual(set(entry), {"name", "source", "description", "category"})


if __name__ == "__main__":
    unittest.main()
