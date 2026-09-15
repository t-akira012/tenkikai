from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
STATEDEF_PATTERN = re.compile(r"^\[statedef\s+(-?\d+)\]$", re.MULTILINE)
STATE_HEADING_PATTERN = re.compile(
    r"^#{2,3} StateDef (-?\d+): .+$", re.MULTILINE
)


def read_text(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def source_state_numbers(relative_path: str) -> set[int]:
    text = (ROOT / relative_path).read_bytes().decode("latin-1")
    return {int(number) for number in STATEDEF_PATTERN.findall(text)}


def documented_state_numbers(relative_path: str) -> list[int]:
    return [int(number) for number in STATE_HEADING_PATTERN.findall(read_text(relative_path))]


def controller_count(controller_type: str) -> int:
    pattern = re.compile(
        rf"^type={re.escape(controller_type)}$", re.IGNORECASE | re.MULTILINE
    )
    total = 0
    for relative_path in (
        "t-command.cmd",
        "t-state.cns",
        "t-observ.cns",
        "t-helper.cns",
        "t-common1.cns",
    ):
        text = (ROOT / relative_path).read_bytes().decode("latin-1")
        total += len(pattern.findall(text))
    return total


def state_block(relative_path: str, state_number: int) -> str:
    text = (ROOT / relative_path).read_bytes().decode("latin-1")
    start_pattern = re.compile(
        rf"^\[statedef {state_number}\]$", re.IGNORECASE | re.MULTILINE
    )
    start_match = start_pattern.search(text)
    if start_match is None:
        raise AssertionError(f"StateDefがありません: {relative_path}:{state_number}")

    next_match = re.search(
        r"^\[statedef -?\d+\]$",
        text[start_match.end() :],
        re.IGNORECASE | re.MULTILINE,
    )
    finish = len(text)
    if next_match is not None:
        finish = start_match.end() + next_match.start()
    return text[start_match.start() : finish]


def direct_damage_values(relative_path: str, state_number: int) -> list[int]:
    block = state_block(relative_path, state_number)
    return [
        int(value)
        for value in re.findall(r"^damage=(\d+)(?:,|$)", block, re.MULTILINE)
    ]


class DocumentationTest(unittest.TestCase):
    def test_state_documents_cover_each_source_state_once(self) -> None:
        state_numbers = source_state_numbers("t-state.cns")
        default_numbers = {
            -1,
            100,
            101,
            102,
            105,
            106,
            107,
            180,
            181,
            191,
            195,
        }
        super_numbers = {3000, 3050, 3051}
        expected = {
            "docs/state-default.md": default_numbers,
            "docs/state-attack.md": state_numbers - default_numbers - super_numbers,
            "docs/super-attack.md": super_numbers,
            "docs/state-helper.md": source_state_numbers("t-observ.cns")
            | source_state_numbers("t-helper.cns"),
            "docs/state-stcommon.md": source_state_numbers("t-common1.cns"),
        }

        actual_all: list[int] = []
        for relative_path, expected_numbers in expected.items():
            actual_numbers = documented_state_numbers(relative_path)
            self.assertEqual(
                len(actual_numbers),
                len(set(actual_numbers)),
                f"{relative_path} に重複したStateDef見出しがあります",
            )
            self.assertEqual(
                set(actual_numbers),
                expected_numbers,
                f"{relative_path} と実装のStateDefに差異があります",
            )
            actual_all.extend(actual_numbers)

        source_all = (
            {-1}
            | state_numbers
            | source_state_numbers("t-observ.cns")
            | source_state_numbers("t-helper.cns")
            | source_state_numbers("t-common1.cns")
        )
        self.assertEqual(set(actual_all), source_all)
        self.assertEqual(len(actual_all), len(source_all))

    def test_state_document_titles(self) -> None:
        expected_titles = {
            "docs/state-default.md": "# デフォルトステート",
            "docs/state-attack.md": "# アタックステート",
            "docs/super-attack.md": "# 超必殺技ステート",
            "docs/state-helper.md": "# ヘルパーステート",
            "docs/state-stcommon.md": "# stcommon共有ステート",
        }

        for relative_path, expected_title in expected_titles.items():
            first_line = read_text(relative_path).splitlines()[0]
            self.assertEqual(first_line, expected_title)

    def test_generated_object_lists_match_controller_counts(self) -> None:
        expected = {
            "helper": (1, "docs/helper-list.md"),
            "explod": (3, "docs/explod-list.md"),
            "projectile": (0, "docs/projectile-list.md"),
        }

        for controller_type, (documented_count, relative_path) in expected.items():
            self.assertEqual(controller_count(controller_type), documented_count)
            self.assertIn(
                f"{controller_type.capitalize()}` コントローラーは{documented_count}個",
                read_text(relative_path),
            )

    def test_head_helper_uses_state_number_as_id(self) -> None:
        observer = (ROOT / "t-observ.cns").read_bytes().decode("latin-1")
        helper_states = (ROOT / "t-helper.cns").read_bytes().decode("latin-1")
        helper_document = read_text("docs/helper-list.md")

        self.assertIn("id=99001", observer)
        self.assertIn("!numhelper(99001)", observer)
        self.assertEqual(observer.count("ishelper(99001)"), 5)
        self.assertIn("ishelper(99001)", helper_states)
        self.assertIn("| ID | `99001` |", helper_document)

    def test_documented_damage_totals_are_mathematically_consistent(self) -> None:
        attack_document = read_text("docs/state-attack.md")
        super_document = read_text("docs/super-attack.md")

        crouching_strong_punch = direct_damage_values("t-state.cns", 410)
        enhanced_knee = sum(
            direct_damage_values("t-state.cns", state_number)[0]
            for state_number in (1070, 1071, 1075)
        )
        triple_palm_damage = direct_damage_values("t-state.cns", 3000)
        triple_palm = triple_palm_damage[0] * 2 + triple_palm_damage[1]

        self.assertEqual(sum(crouching_strong_punch), 73)
        self.assertIn("合計73ダメージ", attack_document)
        self.assertEqual(enhanced_knee, 145)
        self.assertIn("直接ダメージは145", attack_document)
        self.assertEqual(triple_palm, 219)
        self.assertIn("直接ダメージは219", super_document)

        smash_upper = state_block("t-state.cns", 3050)
        self.assertIn("damage=155, 12", smash_upper)
        self.assertIn("fall.damage=70", smash_upper)
        self.assertIn("155ダメージと12のガードダメージ", super_document)
        self.assertIn("70の追加ダメージ", super_document)

    def test_local_markdown_links_exist(self) -> None:
        for document_path in (ROOT / "docs").glob("*.md"):
            text = document_path.read_text(encoding="utf-8")
            links = re.findall(r"\]\(([^):]+\.md)\)", text)

            for link in links:
                linked_path = document_path.parent / link
                self.assertTrue(
                    linked_path.is_file(),
                    f"リンク先がありません: {document_path.name}:{link}",
                )


if __name__ == "__main__":
    unittest.main()
