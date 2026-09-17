from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
INPUTS = (
    ("holdfwd", "/$F", 1),
    ("holdback", "/$B", 2),
    ("holdup", "/$U", 4),
    ("holddown", "/$D", 8),
    ("x", "x", 16),
    ("y", "y", 32),
    ("z", "z", 64),
    ("a", "a", 128),
    ("b", "b", 256),
    ("c", "c", 512),
    ("s", "s", 1024),
    ("recovery", "x+y", 2048),
    ("FF", "F,F", 4096),
    ("BB", "B,B", 8192),
)


def source_text(relative_path: str) -> str:
    return (ROOT / relative_path).read_bytes().decode("latin-1")


class InputMapTest(unittest.TestCase):
    def test_command_definitions_match_input_map(self) -> None:
        command_text = source_text("cns/command.cmd")
        command_header = command_text.split("[statedef -1]", 1)[0]
        actual = {
            name: input_definition
            for name, input_definition in re.findall(
                r'^\[Command\]\nname="([^"]+)"\ncommand=(.+)\ntime=\d+$',
                command_header,
                re.MULTILINE,
            )
        }
        expected = {name: input_definition for name, input_definition, _ in INPUTS}

        self.assertEqual(actual, expected)

    def test_command_conversion_matches_input_map(self) -> None:
        command_text = source_text("cns/command.cmd")
        state_minus_one = command_text.split("[statedef -1]", 1)[1]

        first_change_state = state_minus_one.index("type=changestate")
        self.assertLess(state_minus_one.index("var(2)=0"), first_change_state)
        for name, _, mask in INPUTS:
            conversion = (
                "type=varset\n"
                f'trigger1=command="{name}"\n'
                f"var(2)=var(2)|{mask}"
            )
            self.assertEqual(state_minus_one.count(conversion), 1, name)
            self.assertLess(state_minus_one.index(conversion), first_change_state)

    def test_input_consumers_do_not_use_command(self) -> None:
        for relative_path in (
            "cns/state.cns",
            "cns/observ.cns",
            "cns/helper.cns",
            "cns/common1.cns",
        ):
            self.assertNotRegex(
                source_text(relative_path),
                re.compile(r"\bcommand\b", re.IGNORECASE),
            )

    def test_retired_input_variables_are_not_used(self) -> None:
        combined = "\n".join(
            source_text(relative_path)
            for relative_path in (
                "cns/command.cmd",
                "cns/state.cns",
                "cns/observ.cns",
                "cns/helper.cns",
                "cns/common1.cns",
            )
        )
        self.assertNotRegex(
            combined,
            re.compile(r"(?<!sys)var\((?:3|4)\)", re.IGNORECASE),
        )

    def test_fixed_document_contains_each_bit_assignment(self) -> None:
        document = (ROOT / "docs/AGENTS.input-map.md").read_text(encoding="utf-8")
        for bit, (name, input_definition, mask) in enumerate(INPUTS):
            row = f"| {bit} | `{mask}` | `{name}` | `{input_definition}` |"
            self.assertIn(row, document)


if __name__ == "__main__":
    unittest.main()
