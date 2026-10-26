"""What the plugin directory's scan and its reviewers look for, held here.

The plugin is instructions only. The directory's pre-submission checklist and its
security scan hold a version for review, or fail it, when it:

* reads a credential from the user's environment, in any file and in a README
  example too;
* runs a package launcher, or quotes a download-and-execute pattern;
* carries a system file (a macOS or Windows one), a symbolic link, a Git submodule
  or a Git LFS pointer, or a bundle (.mcpb, .dxt);
* names itself or its publisher so that it reads as another company's product.

This file also holds three promises of ours: no price figure beyond the one
sentence the README is allowed, no word that calls the plugin the platform's own,
and no commit that carries a co-author trailer or a closing keyword.

The patterns are built by concatenation, so this file never matches itself. It
reads no environment variable. Stdlib only; run with
`python3 -m unittest discover -s tests -v` from the repository root.
"""

import os
import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BINARY = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".woff", ".woff2", ".ttf", ".otf"}
SKIP_DIRS = {".git", "__pycache__"}


def plugin_files():
    """Every file in the plugin folder as a Path relative to it: tracked ones and
    untracked ones that are not ignored, or a walk of the folder when it is not a
    checkout of its own."""
    try:
        top = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=ROOT,
                             capture_output=True, text=True, check=True).stdout.strip()
        if Path(top).resolve() == ROOT.resolve():
            out = subprocess.run(
                ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
                cwd=ROOT, capture_output=True, check=True).stdout
            names = [n for n in out.decode("utf-8").split("\0") if n]
            return sorted({Path(n) for n in names if (ROOT / n).exists()
                           or (ROOT / n).is_symlink()})
    except (OSError, subprocess.CalledProcessError):
        pass
    found = []
    for dirpath, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            if not f.endswith(".pyc"):
                found.append(Path(os.path.relpath(os.path.join(dirpath, f), ROOT)))
    return sorted(found)


def text_files():
    return [p for p in plugin_files()
            if p.suffix.lower() not in BINARY and not (ROOT / p).is_symlink()]


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def hits(pattern, paths, flags=0):
    found = []
    rx = re.compile(pattern, flags)
    for p in paths:
        for n, line in enumerate(read(p).splitlines(), 1):
            if rx.search(line):
                found.append("%s:%d: %s" % (p, n, line.strip()[:100]))
    return found


# What the listing and the skills are read as: the words people read.
LISTING = ("README.md", ".claude-plugin/plugin.json", ".claude-plugin/marketplace.json")


def listing_files():
    return [p for p in plugin_files() if str(p) in LISTING
            or p.parts[0] in ("skills", "commands")]


class Credentials(unittest.TestCase):

    def test_no_file_reads_a_credential(self):
        patterns = [
            "os" + r"\." + "environ",
            "get" + "env" + r"\(",
            "process" + r"\." + "env",
            r"\$" + r"\{[^}]*" + "(TOKEN|SECRET|KEY|PASSWORD)",
            "Author" + "ization" + ":",
            "Bear" + "er ",
        ]
        for pattern in patterns:
            with self.subTest(pattern=pattern):
                self.assertEqual(hits(pattern, text_files()), [])


class Launchers(unittest.TestCase):

    def test_no_package_launcher(self):
        words = ["np" + "x", "bun" + "x", "pnpm " + "dlx", "yarn " + "dlx", "uv" + "x",
                 "pipx " + "run", "uv " + "run"]
        pattern = r"(?<![A-Za-z0-9_-])(" + "|".join(words) + r")(?![A-Za-z0-9_-])"
        self.assertEqual(hits(pattern, text_files()), [])

    def test_no_download_and_execute_pattern(self):
        pattern = ("(curl|wget)" + r"[^|;]*" + r"\|" + r"\s*(sudo\s+)?(ba)?" + "sh")
        # The CI file describes the check in its own comments and is excluded from
        # the repository grep for the same reason.
        paths = [p for p in text_files() if p.name != "checks.yml"]
        self.assertEqual(hits(pattern, paths), [])


class Files(unittest.TestCase):

    def test_no_system_file_link_submodule_or_bundle(self):
        banned_names = {".DS_" + "Store", "Thumbs" + ".db", "desktop" + ".ini",
                        ".git" + "modules", ".git" + "attributes", "CLAUDE" + ".md"}
        banned_suffixes = (".mcp" + "b", ".dx" + "t")
        for p in plugin_files():
            with self.subTest(file=str(p)):
                self.assertNotIn(p.name, banned_names)
                self.assertNotIn("__MAC" + "OSX", p.parts)
                self.assertFalse(str(p).endswith(banned_suffixes))
                self.assertFalse((ROOT / p).is_symlink(), "a symbolic link")

    def test_nothing_that_runs_ships_in_this_release(self):
        for folder in ("bin", "hooks", "agents", "evals", "scripts"):
            self.assertFalse((ROOT / folder).exists(), folder)
        for name in ("package.json", "package-lock.json", "npm-shrinkwrap.json",
                     "bun.lock", "bun.lockb", ".npmrc", "bunfig.toml", "uv.toml"):
            self.assertFalse((ROOT / name).exists(), name)

    def test_no_git_lfs_pointer(self):
        for p in text_files():
            with self.subTest(file=str(p)):
                self.assertFalse(read(p).startswith("version https://git-lfs"))


class Promises(unittest.TestCase):

    def test_no_price_figure_beyond_the_one_allowed_sentence(self):
        allowed = ("The plugin is free (MIT). The AdCopilot connector is a hosted "
                   "service: Free plan available; paid plans on "
                   "https://adcopilot.cloud/pricing")
        for p in listing_files():
            text = " ".join(read(p).split()).replace(allowed, "")
            with self.subTest(file=str(p)):
                self.assertIsNone(re.search(r"\$" + r"\s?\d", text))
                self.assertIsNone(re.search("/" + "mo" + r"\b", text))
                self.assertIsNone(re.search(r"\bper (month|year|seat)\b", text, re.I))

    def test_the_allowed_sentence_is_in_the_readme(self):
        self.assertIn("Free plan available; paid plans on https://adcopilot.cloud/pricing",
                      " ".join(read("README.md").split()))

    def test_no_word_that_calls_the_plugin_the_platforms_own(self):
        word = "off" + "icial"
        self.assertEqual(hits(r"\b" + word + r"\b", listing_files(), re.I), [])
        # "by X" and the like are allowed only as "not by", and in the trademark
        # sentence "not affiliated with or endorsed by".
        owners = "(X|Twitter|Google|Meta|LinkedIn|TikTok|Microsoft)"
        pattern = r"(?<!not )(?<!endorsed )\bby " + owners + r"\b"
        self.assertEqual(hits(pattern, listing_files()), [])

    def test_the_description_says_who_made_it(self):
        text = read(".claude-plugin/plugin.json")
        self.assertIn("Made by Atromx Intelligence, not by X.", text)


# Words that read as a claim about a relationship with X: an approval, a
# partnership, an access level, an app or an integration. The plugin makes none of
# these claims. Every pattern is built from pieces, so this file never matches itself.
X_RELATIONSHIP_PATTERNS = [
    r"(?i)\bapproved\s+by\s+X\b",
    r"(?i)\bX\s+partners?\b",
    r"(?i)\bAds\s+API\b",
    r"(?i)\bStandard\s+access\b",
    "3357" + "2174",
    r"(?i)\bintegration\s+with\s+X\b",
    r"(?i)\bwhen\s+X\s+approves\b",
    r"(?i)\bX\s+approves\b",
    r"(?i)\bapproval\s+(?:from|by)\s+X\b",
    r"(?i)\bX['\u2019]s\s+approval\b",
]


class NoXRelationshipWords(unittest.TestCase):

    def test_no_file_says_x_approved_partnered_or_gave_access(self):
        # Every text file, the tests and the CI files included.
        for p in text_files():
            text = " ".join(read(p).split())
            for pattern in X_RELATIONSHIP_PATTERNS:
                hit = re.search(pattern, text)
                with self.subTest(file=str(p), pattern=pattern):
                    self.assertIsNone(hit, hit and hit.group(0))

    def test_the_ban_catches_the_ways_it_is_said_and_leaves_the_plain_sentences(self):
        # The phrases are built at run time, so this file carries none of them.
        caught = [
            "approved by {o}", "{o} partner", "{o} partners", "Ads " + "API",
            "Standard " + "access", "3357" + "2174", "integration with {o}",
            "when {o} approves", "{o} approves", "approval from {o}",
            "approval by {o}", "{o}'s approval", "{o}\u2019s approval",
        ]
        passed = [
            "It does not read your {o} ad account.",
            "Not affiliated with or endorsed by {o} Corp.",
            "Made by Atromx Intelligence, not by {o}.",
            "the {o} Pixel and the Conversion API",
            "your Google products through Google's APIs",
        ]

        def matched(phrase):
            return [p for p in X_RELATIONSHIP_PATTERNS
                    if re.search(p, phrase.format(o="X"))]

        for phrase in caught:
            self.assertNotEqual(matched(phrase), [], phrase)
        for phrase in passed:
            self.assertEqual(matched(phrase), [], phrase)


class Commits(unittest.TestCase):

    def commits(self):
        # Real commits only. On a pull request the checkout is a merge commit that
        # GitHub makes in the name of the person who opened it; it is never pushed.
        try:
            out = subprocess.run(
                ["git", "log", "--no-merges", "--format=%an <%ae>|%cn <%ce>|%B%x00"],
                cwd=ROOT, capture_output=True, text=True, check=True).stdout
        except (OSError, subprocess.CalledProcessError):
            self.skipTest("not a Git checkout")
        entries = [e for e in out.split("\0") if e.strip()]
        if not entries:
            self.skipTest("no commits yet")
        return entries

    def test_every_commit_is_by_atromx_intelligence(self):
        who = "Atromx Intelligence <support@atromx.com>"
        for entry in self.commits():
            author, committer, _ = entry.strip().split("|", 2)
            self.assertEqual(author, who)
            self.assertEqual(committer, who)

    def test_no_commit_has_a_co_author_trailer_or_a_closing_keyword(self):
        trailer = "Co-" + "Authored-" + "By"
        closing = r"\b(fix|fixes|fixed|close|closes|closed|resolve|resolves|resolved)\b"
        for entry in self.commits():
            body = entry.split("|", 2)[2]
            self.assertNotIn(trailer.lower(), body.lower())
            self.assertIsNone(re.search(closing, body, re.I), body)


if __name__ == "__main__":
    unittest.main()
