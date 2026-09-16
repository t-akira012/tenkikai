from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
STATEDEF_PATTERN = re.compile(r"^\[statedef\s+(-?\d+)\]$", re.MULTILINE)
STATE_HEADING_PATTERN = re.compile(r"^#{2,3} StateDef (-?\d+): .+$", re.MULTILINE)
STATE_H3_PATTERN = re.compile(r"^### StateDef -?\d+: .+$")


def read_text(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def source_text(relative_path: str) -> str:
    return (ROOT / relative_path).read_bytes().decode("latin-1")


def source_state_numbers(relative_path: str) -> set[int]:
    return {int(number) for number in STATEDEF_PATTERN.findall(source_text(relative_path))}


def documented_state_numbers(relative_path: str) -> list[int]:
    return [int(number) for number in STATE_HEADING_PATTERN.findall(read_text(relative_path))]


def controller_count(controller_type: str) -> int:
    pattern = re.compile(rf"^type={re.escape(controller_type)}$", re.IGNORECASE | re.MULTILINE)
    return sum(
        len(pattern.findall(source_text(relative_path)))
        for relative_path in (
            "cns/command.cmd",
            "cns/state.cns",
            "cns/observ.cns",
            "cns/helper.cns",
            "cns/common1.cns",
        )
    )


class DocumentationTest(unittest.TestCase):
    def test_state_documents_cover_each_source_state_once(self) -> None:
        state_numbers = source_state_numbers("cns/state.cns")
        expected = {
            "docs/state/default.md": {-1} | state_numbers,
            "docs/state/attack.md": set(),
            "docs/state/superattack.md": set(),
            "docs/state/observ.md": source_state_numbers("cns/observ.cns"),
            "docs/state/helper.md": source_state_numbers("cns/helper.cns"),
            "docs/state/stcommon.md": source_state_numbers("cns/common1.cns"),
        }

        actual_all: list[int] = []
        for relative_path, expected_numbers in expected.items():
            actual_numbers = documented_state_numbers(relative_path)
            self.assertEqual(len(actual_numbers), len(set(actual_numbers)))
            self.assertEqual(set(actual_numbers), expected_numbers, relative_path)
            actual_all.extend(actual_numbers)

        source_all = (
            {-1}
            | state_numbers
            | source_state_numbers("cns/observ.cns")
            | source_state_numbers("cns/helper.cns")
            | source_state_numbers("cns/common1.cns")
        )
        self.assertEqual(set(actual_all), source_all)
        self.assertEqual(len(actual_all), len(source_all))

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

    def test_generated_object_lists_match_controller_counts(self) -> None:
        expected = {
            "helper": (2, "docs/state/helper-list.md"),
            "explod": (2, "docs/state/explod-list.md"),
            "projectile": (0, "docs/state/projectile-list.md"),
        }
        for controller_type, (documented_count, relative_path) in expected.items():
            self.assertEqual(controller_count(controller_type), documented_count)
            self.assertIn(
                f"{controller_type.capitalize()}` コントローラーは{documented_count}個",
                read_text(relative_path),
            )

    def test_kfm_actions_and_attacks_are_removed(self) -> None:
        self.assertNotIn("type=hitdef", source_text("cns/state.cns").lower())
        self.assertEqual(source_text("cns/command.cmd").lower().count("type=changestate"), 4)
        air = source_text("binary/animation.air")
        removed_actions = {
            6, 10, 11, 12, 40, 41, 42, 43, 47, 195, 200, 210, 230, 240,
            400, 410, 430, 440, 600, 610, 630, 640, 800, 810, 820, 1000,
            1010, 1020, 1025, 1027, 1050, 1051, 1052, 1055, 1056, 1060,
            1061, 1070, 1071, 1100, 1110, 1120, 1200, 1210, 1220, 3000,
            3050, 3051,
        }
        actions = [int(number) for number in re.findall(r"^\[Begin Action (\d+)\]$", air, re.MULTILINE)]
        self.assertFalse(removed_actions & set(actions))
        self.assertEqual(actions.count(105), 1)

    def test_head_helper_and_airjump_safety(self) -> None:
        observer = source_text("cns/observ.cns")
        self.assertIn("id=99001", observer)
        self.assertIn("!numhelper(99001)", observer)
        self.assertIn("airjump.num=0", source_text("cns/constants.cns"))

        common = source_text("cns/common1.cns")
        for state_number in (10, 11, 12, 40):
            pattern = rf"\[statedef {state_number}\].*?type=changestate.*?value=0"
            self.assertRegex(common, re.compile(pattern, re.DOTALL))
        landing = re.search(r"\[statedef 52\](.*?)(?:\[statedef|\Z)", common, re.DOTALL)
        self.assertIsNotNone(landing)
        self.assertIn("type=velset", landing.group(1))
        self.assertIn("type=posset", landing.group(1))

    def test_design_has_no_individual_state_numbers(self) -> None:
        self.assertNotIn("StateDef", read_text("docs/DESIGN.md"))

    def test_local_markdown_links_exist(self) -> None:
        for document_path in (ROOT / "docs").rglob("*.md"):
            text = document_path.read_text(encoding="utf-8")
            for link in re.findall(r"\]\(([^):]+(?:\.md|/))\)", text):
                self.assertTrue((document_path.parent / link).exists(), f"{document_path}:{link}")


if __name__ == "__main__":
    unittest.main()
