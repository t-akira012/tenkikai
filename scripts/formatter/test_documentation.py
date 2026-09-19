from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent.parent
STATE_H3_PATTERN = re.compile(r"^### StateDef -?\d+: .+$")


def read_text(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


class DocumentationTest(unittest.TestCase):
    def test_state_document_titles(self) -> None:
        expected = {
            "docs/state/default.md": "# デフォルトステート",
            "docs/state/attack.md": "# アタックステート",
            "docs/state/superattack.md": "# 超必殺技ステート",
            "docs/state/observ.md": "# 常時監視ステート",
            "docs/state/helper.md": "# ヘルパーステート",
            "docs/state/stcommon.md": "# stcommon共有ステート",
        }
        for relative_path, title in expected.items():
            self.assertEqual(read_text(relative_path).splitlines()[0], title)

    def test_state_document_headings_use_behavior_h2_and_statedef_h3(self) -> None:
        documents = (
            "docs/state/default.md",
            "docs/state/attack.md",
            "docs/state/superattack.md",
            "docs/state/observ.md",
            "docs/state/helper.md",
            "docs/state/stcommon.md",
            "docs/state/explod-list.md",
        )
        for relative_path in documents:
            has_behavior = False
            for line_number, line in enumerate(read_text(relative_path).splitlines(), start=1):
                if line.startswith("## "):
                    self.assertFalse(line.startswith("## StateDef "), f"{relative_path}:{line_number}")
                    has_behavior = True
                elif line.startswith("### StateDef "):
                    self.assertTrue(has_behavior, f"{relative_path}:{line_number}")
                    self.assertRegex(line, STATE_H3_PATTERN, f"{relative_path}:{line_number}")

    def test_design_has_no_individual_state_numbers(self) -> None:
        self.assertNotIn("StateDef", read_text("docs/DESIGN.md"))

    def test_local_markdown_links_exist(self) -> None:
        for document_path in (ROOT / "docs").rglob("*.md"):
            text = document_path.read_text(encoding="utf-8")
            for link in re.findall(r"\]\(([^):]+(?:\.md|/))\)", text):
                self.assertTrue((document_path.parent / link).exists(), f"{document_path}:{link}")


if __name__ == "__main__":
    unittest.main()
