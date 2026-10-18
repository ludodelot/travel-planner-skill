"""Repository hygiene: valid skill metadata, no broken links, no personal data or secrets."""

import re
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {".md", ".py", ".sh", ".yml", ".yaml", ".json", ".txt"}
SKIP_DIRS = {".git", "__pycache__", "assets"}


def text_files():
    for path in ROOT.rglob("*"):
        if not path.is_file() or any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.suffix in TEXT_SUFFIXES or path.name in {"LICENSE", ".gitignore"}:
            yield path


class SkillMetadataTest(unittest.TestCase):
    def test_skill_md_has_name_and_description(self):
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
        self.assertIsNotNone(match, "SKILL.md needs YAML frontmatter")
        front = match.group(1)
        self.assertRegex(front, r"(?m)^name: travel-planner$")
        description = re.search(r"(?m)^description: (.+)$", front)
        self.assertIsNotNone(description)
        self.assertGreater(len(description.group(1)), 80)

    def test_every_reference_file_is_linked_from_skill_md(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        for path in sorted((ROOT / "references").glob("*.md")):
            if path.name == "lessons-learned.md":
                continue  # linked in the file tree rather than the workflow table
            self.assertIn(f"references/{path.name}", skill, f"{path.name} is not mentioned in SKILL.md")


class LinkTest(unittest.TestCase):
    def test_relative_markdown_links_exist(self):
        pattern = re.compile(r"\]\(([^)\s]+)\)")
        for path in text_files():
            if path.suffix != ".md":
                continue
            for target in pattern.findall(path.read_text(encoding="utf-8")):
                if target.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                clean = target.split("#")[0]
                if not clean:
                    continue
                resolved = (path.parent / clean).resolve()
                self.assertTrue(resolved.exists(), f"{path.relative_to(ROOT)} links to missing {target}")

    def test_backticked_repo_paths_exist(self):
        pattern = re.compile(r"`((?:references|templates|scripts|examples|tests|evals|data)/[A-Za-z0-9_\-./]+\.(?:md|py|sh|json))`")
        for path in text_files():
            if path.suffix != ".md":
                continue
            for target in pattern.findall(path.read_text(encoding="utf-8")):
                self.assertTrue((ROOT / target).exists(), f"{path.relative_to(ROOT)} mentions missing {target}")


class PrivacyTest(unittest.TestCase):
    EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
    PHONE = re.compile(r"\+\d{1,3}[ -]?\d[\d -]{7,}\d")
    SECRET = re.compile(r"(?i)(api[_-]?key|secret|password|token)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{12,}")
    FORBIDDEN = re.compile(r"(?i)\b(lvmh|loewe|isla de java)\b")
    ALLOWED_EMAILS = {"noreply@anthropic.com", "user@example.com"}

    def test_no_personal_data_or_secrets(self):
        for path in text_files():
            if path.name == "test_repo_hygiene.py":
                continue
            text = path.read_text(encoding="utf-8")
            rel = path.relative_to(ROOT)
            for email in self.EMAIL.findall(text):
                self.assertIn(email, self.ALLOWED_EMAILS, f"email in {rel}: {email}")
            self.assertIsNone(self.PHONE.search(text), f"phone number in {rel}")
            self.assertIsNone(self.SECRET.search(text), f"possible secret in {rel}")
            self.assertIsNone(self.FORBIDDEN.search(text), f"employer or address in {rel}")


class InstallTest(unittest.TestCase):
    def test_install_script_copies_the_skill(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "travel-planner"
            subprocess.run([str(ROOT / "install.sh"), str(dest)], check=True, capture_output=True)
            self.assertTrue((dest / "SKILL.md").is_file())
            self.assertTrue((dest / "scripts" / "cli.py").is_file())
            self.assertTrue((dest / "data" / "holidays" / "ES-MD-2026.json").is_file())
            self.assertFalse((dest / ".git").exists())
            self.assertFalse((dest / "tests").exists())


if __name__ == "__main__":
    unittest.main()
