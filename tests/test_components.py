"""The plugin's skills, commands and README.

The plugin is instructions only, so its text is the product. This file holds the
rules that text has to keep:

* every skill and command has front matter that Claude Code can parse, a `name`
  equal to its folder or file name, and a `description` that is one text value;
* every tool a skill or command names is a tool the AdCopilot connector really
  has (`tests/connector_tools.txt`, from AdCopilot's tool registry), and a skill
  names only the tools it is meant to use, by bare name: never the full
  name that starts with the mcp prefix and a plugin name, because that namespace
  belongs to whichever AdCopilot plugin loaded first;
* the first `get_org_context` call carries this plugin's own marker
  (`claude-plugin/<plugin name>/<version>`): never the bare word, which starts the
  main plugin's skills, and never a bare version, which reads as an old version of
  the main plugin;
* every skill holds the approval paragraph, and every skill and `/setup` says in
  the first answer what works today and what does not;
* the README has the trademark line, enough words and the connector paragraph.

Stdlib only; it reads no environment variable. Run with
`python3 -m unittest discover -s tests -v` from the repository root.
"""

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
NAME = PLUGIN["name"]
VERSION = PLUGIN["version"]
MARKER = "claude-plugin/%s/%s" % (NAME, VERSION)

TODAY_LATER = (
    "Today this plugin checks your X Pixel and tags in Google Tag Manager, reads X "
    "traffic and key events in Google Analytics (GA4), checks UTM tags, guides "
    "conversion setup, plans campaigns, drafts post copy and does the budget pacing "
    "math. It does not read your X ad account.")
APPROVAL = (
    "Every change is proposed first, with what it changes and how to undo it, and is "
    "applied only after the customer's explicit yes in this conversation.")
CONTEXT_NOTE = ("`get_org_context`'s `next_step` and `playbook` describe the whole "
                "workspace, not")
TRADEMARK = ("Made by Atromx Intelligence (https://adcopilot.cloud). Not affiliated "
             "with or endorsed by X Corp. X and Twitter are trademarks of X Corp.")
CHECKED = "checked 23 October 2026"

# Each skill and the tools it is meant to use. A skill must name each of these
# and no other tool.
SKILL_TOOLS = {
    "x-ads-tracking": {
        "get_org_context", "gtm_list_accounts", "gtm_list_containers",
        "gtm_list_workspaces", "gtm_list_tags", "gtm_list_triggers",
        "gtm_list_version_headers", "gtm_list_built_in_variables",
        "gtm_enable_built_in_variable", "gtm_create_trigger", "gtm_create_tag"},
    "x-ads-traffic": {
        "get_org_context", "ga4_list_account_summaries", "ga4_get_metadata",
        "ga4_run_report", "ga4_list_conversion_events"},
    "x-ads-plan": {"get_org_context"},
    "x-ads-budget": set(),
}
COMMANDS = {"setup", "check", "plan"}
# Skills that read no X data and say so, and skills that state platform facts.
SAYS_NO_X_DATA = {"x-ads-plan", "x-ads-budget"}
STATES_PLATFORM_FACTS = {"x-ads-tracking", "x-ads-traffic", "x-ads-plan"}

TOOL_TOKEN = re.compile(r"`([a-z][a-z0-9]*(?:_[a-z0-9]+)+)`")
# A backticked name that starts like a tool must be one.
TOOL_PREFIXES = ("gsc_", "ga4_", "gtm_", "create_", "update_", "set_", "add_",
                 "remove_", "list_", "get_", "link_", "attach_", "pause_", "run_",
                 "enable_", "provision_", "analyze_", "lsa_", "shopping_")


class Base(unittest.TestCase):
    """assertHas and assertLacks fail with the needle only, never with a whole
    file in the message."""

    def assertHas(self, needle, haystack, msg=None):
        if needle not in haystack:
            self.fail("%smissing: %r" % ((msg + ": ") if msg else "", str(needle)[:120]))

    def assertLacks(self, needle, haystack, msg=None):
        if needle in haystack:
            self.fail("%sfound: %r" % ((msg + ": ") if msg else "", str(needle)[:120]))


def tools_available():
    names = (ROOT / "tests" / "connector_tools.txt").read_text(encoding="utf-8").split()
    return set(names)


def read(path):
    return Path(path).read_text(encoding="utf-8")


def flat(path):
    """The file's text with every run of whitespace as one space, so a sentence
    wrapped over two lines is still one sentence."""
    return " ".join(read(path).split())


def front_matter(text):
    """The front matter as a dict, or an AssertionError naming what is wrong. A
    small parser on purpose: stdlib only. It also refuses what YAML would read
    differently from a plain one-line string."""
    assert text.startswith("---\n"), "no front matter"
    end = text.find("\n---\n", 4)
    assert end > 0, "front matter is not closed"
    out = {}
    for line in text[4:end].split("\n"):
        assert re.match(r"^[a-z][a-z-]*: \S", line), "not a `key: value` line: %r" % line
        key, value = line.split(": ", 1)
        assert key not in out, "%s is given twice" % key
        out[key] = value
    return out, text[end + 5:]


def plain_scalar_problem(value):
    if value[0] in "[]{}\"'|>!&*%@`#-?,":
        return "starts with %r, which YAML reads as syntax" % value[0]
    if ": " in value or " #" in value or value.endswith(":"):
        return "holds ': ' or ' #', which YAML reads as syntax"
    return None


def components():
    skills = sorted((ROOT / "skills").glob("*/SKILL.md"))
    commands = sorted((ROOT / "commands").glob("*.md"))
    return skills, commands


class FrontMatter(Base):

    def test_there_are_three_to_five_skills_and_one_to_three_commands(self):
        skills, commands = components()
        self.assertTrue(3 <= len(skills) <= 5, len(skills))
        self.assertTrue(1 <= len(commands) <= 3, len(commands))
        self.assertEqual({p.parent.name for p in skills}, set(SKILL_TOOLS))
        self.assertEqual({p.stem for p in commands}, COMMANDS)

    def test_every_skill_and_command_has_a_name_and_one_text_description(self):
        skills, commands = components()
        for path in skills + commands:
            with self.subTest(path=str(path.relative_to(ROOT))):
                fm, body = front_matter(read(path))
                self.assertEqual(set(fm), {"name", "description"})
                expected = path.parent.name if path.name == "SKILL.md" else path.stem
                self.assertEqual(fm["name"], expected)
                self.assertIsNone(plain_scalar_problem(fm["name"]))
                self.assertTrue(fm["description"].strip())
                self.assertIsNone(plain_scalar_problem(fm["description"]),
                                  plain_scalar_problem(fm["description"]))
                self.assertLessEqual(len(fm["description"]), 700)
                self.assertTrue(body.strip(), "no body")

    def test_skill_descriptions_say_what_the_skill_does_and_when_to_use_it(self):
        skills, _ = components()
        for path in skills:
            with self.subTest(skill=path.parent.name):
                fm, _ = front_matter(read(path))
                self.assertHas("Use when the user asks", fm["description"])

    def test_skill_names_are_unique_to_this_plugin(self):
        # Skill names are unique across the AdCopilot plugins, so the "/" menu
        # never shows two look-alikes.
        skills, _ = components()
        for path in skills:
            self.assertTrue(path.parent.name.startswith("x-ads-"), path.parent.name)
        self.assertLacks("adcopilot-seo", {p.parent.name for p in skills})
        self.assertLacks("adcopilot-meta", {p.parent.name for p in skills})


class ToolNames(Base):

    def test_the_tool_list_is_the_connectors_and_has_no_switched_off_tool(self):
        names = tools_available()
        self.assertGreater(len(names), 100)
        for needed in ("get_org_context", "gtm_create_tag", "ga4_run_report"):
            self.assertHas(needed, names)
        for off in ("shopping_product_issues", "lsa_leads", "lsa_rate_lead"):
            self.assertLacks(off, names, "switched off in production")

    def test_every_tool_a_file_names_is_a_real_connector_tool(self):
        names = tools_available()
        skills, commands = components()
        for path in skills + commands + [ROOT / "README.md"]:
            for token in TOOL_TOKEN.findall(read(path)):
                if token.startswith(TOOL_PREFIXES) or token in names:
                    with self.subTest(file=str(path.relative_to(ROOT)), tool=token):
                        self.assertHas(token, names)

    def test_a_skill_names_exactly_the_tools_it_is_meant_to_use(self):
        names = tools_available()
        skills, _ = components()
        for path in skills:
            skill = path.parent.name
            used = {t for t in TOOL_TOKEN.findall(read(path))
                    if t.startswith(TOOL_PREFIXES) or t in names}
            with self.subTest(skill=skill):
                self.assertEqual(used, SKILL_TOOLS[skill])

    def test_no_full_tool_name_is_used_anywhere(self):
        # Built by concatenation so this file does not match itself.
        full = "mcp__" + "plugin_"
        for path in ROOT.rglob("*"):
            if path.is_file() and ".git" not in path.parts and path.suffix in {
                    ".md", ".json", ".yml", ".txt", ".py"}:
                with self.subTest(file=str(path.relative_to(ROOT))):
                    self.assertLacks(full, read(path))


class FirstCall(Base):

    def test_every_file_that_calls_get_org_context_sends_this_plugins_marker(self):
        skills, commands = components()
        for path in skills + commands:
            text = flat(path)
            if "get_org_context" not in text:
                continue
            with self.subTest(file=str(path.relative_to(ROOT))):
                self.assertHas('source: "%s"' % MARKER, text)

    def test_the_marker_is_never_bare_and_never_a_bare_version(self):
        skills, commands = components()
        for path in skills + commands:
            text = read(path)
            with self.subTest(file=str(path.relative_to(ROOT))):
                for m in re.finditer(r"claude-plugin", text):
                    self.assertTrue(text.startswith("claude-plugin/%s/%s" % (NAME, VERSION),
                                                    m.start()), text[m.start():m.start() + 40])
                self.assertLacks("claude-plugin/" + VERSION, text)

    def test_a_scheduled_run_sends_the_scheduled_marker_and_changes_nothing(self):
        skills, commands = components()
        for path in skills + commands:
            text = flat(path)
            if "get_org_context" not in text:
                continue
            with self.subTest(file=str(path.relative_to(ROOT))):
                self.assertHas('source: "claude-scheduled"', text)
                self.assertHas("change nothing", text)

    def test_the_context_note_is_in_every_file_that_calls_get_org_context(self):
        skills, commands = components()
        for path in skills + commands:
            text = flat(path)
            if "get_org_context" not in text:
                continue
            with self.subTest(file=str(path.relative_to(ROOT))):
                self.assertHas(CONTEXT_NOTE, text)
                self.assertHas("keep any limit `next_step` adds, and offer the rest", text)


class Honesty(Base):

    def test_every_skill_holds_the_approval_paragraph(self):
        skills, _ = components()
        for path in skills:
            with self.subTest(skill=path.parent.name):
                self.assertHas(APPROVAL, " ".join(read(path).split()))
                self.assertHas("deletes nothing", read(path))

    def test_every_skill_and_setup_says_what_works_today_and_what_does_not(self):
        skills, commands = components()
        setup = ROOT / "commands" / "setup.md"
        for path in skills + [setup]:
            with self.subTest(file=str(path.relative_to(ROOT))):
                text = " ".join(read(path).split())
                self.assertHas(TODAY_LATER, text)
                self.assertHas("once", text)

    def test_the_planning_and_budget_skills_say_they_read_no_x_data(self):
        for skill in SAYS_NO_X_DATA:
            with self.subTest(skill=skill):
                text = " ".join(read(ROOT / "skills" / skill / "SKILL.md").split())
                self.assertHas("AdCopilot reads no X data for this", text)

    def test_platform_facts_carry_the_day_they_were_checked(self):
        for skill in STATES_PLATFORM_FACTS:
            with self.subTest(skill=skill):
                self.assertHas(CHECKED, " ".join(read(ROOT / "skills" / skill / "SKILL.md").split()))

    def test_the_tag_manager_skill_stages_and_never_publishes(self):
        text = " ".join(read(ROOT / "skills" / "x-ads-tracking" / "SKILL.md").split())
        self.assertHas("workspace named AdCopilot", text)
        self.assertHas("never published", text)
        self.assertHas("Never publish, and never delete", text)
        # A connected product's own words and link, never a remembered address.
        self.assertHas("`unlocks`", text)
        self.assertHas("`connect_url`", text)
        self.assertHas("Never give a link from memory", text)

    def test_the_budget_skill_calls_no_tool(self):
        path = ROOT / "skills" / "x-ads-budget" / "SKILL.md"
        self.assertLacks("get_org_context", read(path))
        self.assertHas("calls no AdCopilot tool", flat(path))

    def test_commands_follow_their_skill(self):
        for command, skill in (("check", "x-ads-tracking"), ("plan", "x-ads-plan")):
            with self.subTest(command=command):
                self.assertHas("Follow the `%s` skill." % skill,
                              read(ROOT / "commands" / (command + ".md")))
                self.assertHas("$ARGUMENTS", read(ROOT / "commands" / (command + ".md")))


class Readme(Base):

    def setUp(self):
        self.text = read(ROOT / "README.md")
        self.flat = " ".join(self.text.split())

    def test_it_has_the_title_and_the_trademark_line(self):
        self.assertTrue(self.text.startswith("# " + PLUGIN["displayName"] + "\n"))
        self.assertHas(TRADEMARK, self.flat)
        self.assertHas("Not related to other products named AdCopilot.", self.flat)

    def test_it_has_enough_words_outside_code_fences(self):
        outside = re.sub(r"```.*?```", "", self.text, flags=re.S)
        words = len(outside.split())
        self.assertGreaterEqual(words, 600)
        self.assertLessEqual(words, 1200)
        self.assertGreater(words, 40)

    def test_it_holds_the_sections_and_the_connector_paragraph(self):
        for heading in ("## What it does today", "## What it does not read", "## Plans",
                        "## Install", "## Already use another AdCopilot plugin?",
                        "## What you get", "## What it will not do", "## Data",
                        "## Support", "## Version", "## Licence", "## What CI runs"):
            self.assertHas("\n" + heading + "\n", self.text, heading)
        self.assertHas("There is one connector and one AdCopilot account, whichever "
                      "AdCopilot plugins you add.", self.flat)
        self.assertHas("`/mcp` shows the connector once, under whichever AdCopilot plugin "
                      "loaded first, and the sign-in belongs to that entry.", self.flat)
        self.assertHas("If Claude asks you to sign in again after you add or remove an "
                      "AdCopilot plugin, run `/mcp` and sign in once.", self.flat)
        self.assertHas(TODAY_LATER, self.flat)

    def test_it_holds_the_plans_and_data_sentences(self):
        self.assertHas("The plugin is free (MIT). The AdCopilot connector is a hosted "
                      "service: Free plan available; paid plans on "
                      "https://adcopilot.cloud/pricing", self.flat)
        self.assertHas("The plugin is instructions only: it runs no code and sends nothing "
                      "anywhere itself. The AdCopilot connector at mcp.adcopilot.cloud "
                      "reads and, on your yes, writes your Google products through "
                      "Google's APIs with your Google sign-in.", self.flat)
        for link in ("https://adcopilot.cloud/privacy", "https://adcopilot.cloud/terms",
                     "https://github.com/AtromxIntelligence/adcopilot-x-ads-plugin/issues",
                     "support@adcopilot.cloud"):
            self.assertHas(link, self.text)

    def test_the_version_paragraph_names_the_manifest_version(self):
        m = re.search(r"^\*\*(\d+\.\d+\.\d+) \((\d{4}-\d{2}-\d{2}), written against "
                      r"AdCopilot v([\d.]+), live since (\d{4}-\d{2}-\d{2})\)\*\*",
                      self.text, flags=re.M)
        self.assertIsNotNone(m, "no version paragraph")
        self.assertEqual(m.group(1), VERSION)


if __name__ == "__main__":
    unittest.main()
