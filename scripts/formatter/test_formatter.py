from __future__ import annotations

import unittest

from formatter import formatter


class FormatterTest(unittest.TestCase):
    def test_double_semicolon_comments_are_preserved(self) -> None:
        source = [
            "; 通常コメント",
            ";; 浮遊移動: trigger1 = 1 && trigger2 = 2",
            "[Statedef 105]",
            ";; 表示機能",
            "[State 105, move]",
            "type = PosAdd",
        ]

        actual = formatter.transform_definition(source, format_states=True)

        self.assertEqual(
            actual,
            [
                ";; 浮遊移動: trigger1 = 1 && trigger2 = 2",
                "",
                "[statedef 105]",
                ";; 表示機能",
                "",
                "[state ]",
                "type=posadd",
            ],
        )

    def test_quoted_state_values_are_not_operator_normalized(self) -> None:
        source = [
            "[Statedef -2]",
            "[State -2, debug]",
            'text = "time: %d\\npos y: %f"',
        ]

        actual = formatter.transform_definition(source, format_states=True)

        self.assertIn('text="time: %d\\npos y: %f"', actual)

    def test_semicolon_inside_quoted_value_is_preserved(self) -> None:
        source = [
            "[Statedef -2]",
            "[State -2, debug]",
            'text = "left;right" ; outside comment',
        ]

        actual = formatter.transform_definition(source, format_states=True)

        self.assertIn('text="left;right"', actual)

    def test_ascii_spaces_inside_quoted_values_are_preserved(self) -> None:
        source = ['name = "TEN KIKAI"', "value = 1"]

        actual = formatter.remove_ascii_spaces(source)

        self.assertEqual(actual, ['name="TEN KIKAI"', "value=1"])

    def test_comments_and_state_format_are_normalized(self) -> None:
        source = [
            "; 説明",
            ";====================",
            "[StateDef 105] ; 後方ステップ",
            "  type = S",
            "",
            "[State 105, move] ; 移動",
            "  trigger1 = AnimTime = 0",
            "  value = 0",
        ]

        actual = formatter.transform_definition(source, format_states=True)

        self.assertEqual(
            actual,
            [
                formatter.DIVIDER,
                "",
                "[statedef 105]",
                "type=s",
                "",
                "[state ]",
                "trigger1=AnimTime=0",
                "value=0",
            ],
        )

    def test_type_values_are_lowercase(self) -> None:
        source = [
            "[Statedef 191]",
            "type = S",
            "[State 191, intro]",
            "type = AssertSpecial",
        ]

        actual = formatter.transform_definition(source, format_states=True)

        self.assertIn("type=s", actual)
        self.assertIn("type=assertspecial", actual)

    def test_spaces_around_operators_are_removed(self) -> None:
        source = [
            "[Statedef 0]",
            "[State 0, animation]",
            "trigger1 = Anim != 0 && Anim != 5",
            "trigger2 = Anim = 5 || AnimTime = 0",
            "trigger3 = abs(vel x) < 2",
        ]

        actual = formatter.transform_definition(source, format_states=True)

        self.assertIn("trigger1=Anim!=0&&Anim!=5", actual)
        self.assertIn("trigger2=Anim=5||AnimTime=0", actual)
        self.assertIn("trigger3=abs(vel x)<2", actual)

    def test_ascii_spaces_are_removed_from_constants(self) -> None:
        source = ["[Data]", "life = 1000", "head.pos = -5, -90"]

        actual = formatter.remove_ascii_spaces(source)

        self.assertEqual(actual, ["[Data]", "life=1000", "head.pos=-5,-90"])

    def test_ascii_spaces_are_removed_only_from_selected_sections(self) -> None:
        source = [
            "[Info]",
            'name = "TENKIKAI"',
            "",
            "[Other]",
            "value = 1",
        ]

        actual = formatter.remove_ascii_spaces_from_sections(source, {"info"})

        self.assertEqual(
            actual,
            ["[Info]", 'name="TENKIKAI"', "", "[Other]", "value = 1"],
        )

    def test_command_spaces_are_removed_before_state_minus_one(self) -> None:
        source = [
            "[Command]",
            'name = "QCF_x"',
            "command = ~D, DF, F, x",
            "",
            "[statedef -1]",
            "[state ]",
            "trigger1=p2bodydist X<3",
        ]

        actual = formatter.remove_ascii_spaces_from_command_definitions(source)

        self.assertIn('name="QCF_x"', actual)
        self.assertIn("command=~D,DF,F,x", actual)
        self.assertIn("trigger1=p2bodydist X<3", actual)

    def test_command_trigger_is_allowed_in_command_state_minus_one(self) -> None:
        source = [
            "[Command]",
            'name="holdfwd"',
            "command=/$F",
            "[statedef -1]",
            "[state ]",
            "type=varset",
            'trigger1=command="holdfwd"',
            "v=2",
            "value=1",
        ]

        formatter.verify_command_trigger_scope("cns/command.cmd", source)

    def test_command_trigger_is_rejected_outside_command_file(self) -> None:
        source = [
            "[statedef 0]",
            "[state ]",
            "type=changestate",
            'trigger1=command="holdfwd"',
            "value=20",
        ]

        with self.assertRaisesRegex(
            RuntimeError,
            r"cns/state\.cns:4 \(StateDef 0, changestate\)",
        ):
            formatter.verify_command_trigger_scope("cns/state.cns", source)

    def test_command_trigger_is_rejected_outside_state_minus_one(self) -> None:
        source = [
            "[statedef 100]",
            "[state ]",
            "type=null",
            'trigger1=command!="holdback"',
        ]

        with self.assertRaisesRegex(
            RuntimeError,
            r"cns/command\.cmd:4 \(StateDef 100, null\)",
        ):
            formatter.verify_command_trigger_scope("cns/command.cmd", source)

    def test_command_trigger_after_non_state_section_is_rejected(self) -> None:
        source = [
            "[statedef -1]",
            "[state ]",
            "type=null",
            "trigger1=1",
            "[Command]",
            'trigger1=command="holdfwd"',
        ]

        with self.assertRaisesRegex(
            RuntimeError,
            r"cns/command\.cmd:6 \(StateDef外, State Controller外\)",
        ):
            formatter.verify_command_trigger_scope("cns/command.cmd", source)

    def test_command_trigger_is_rejected_in_state_minus_one_changestate(self) -> None:
        source = [
            "[statedef -1]",
            "[state ]",
            "type=changestate",
            'trigger1=command="x"',
            "value=4001",
        ]

        with self.assertRaisesRegex(
            RuntimeError,
            r"cns/command\.cmd:4 \(StateDef -1, changestate\)",
        ):
            formatter.verify_command_trigger_scope("cns/command.cmd", source)

    def test_command_text_outside_trigger_is_ignored(self) -> None:
        source = [
            "[Command]",
            'name="holdfwd"',
            "command=/$F",
            "; trigger1=command=\"holdfwd\"",
            "[statedef 0]",
            "[state ]",
            "type=null",
            "trigger1=1",
        ]

        formatter.verify_command_trigger_scope("cns/state.cns", source)

    def test_existing_state_controller_is_allowed_case_insensitively(self) -> None:
        source = [
            "[statedef 0]",
            "type=S",
            "[state ]",
            "type=ChangeState",
            "trigger1=1",
            "value=20",
        ]

        formatter.verify_state_controller_types_in_lines("cns/state.cns", source)

    def test_unknown_state_controller_is_rejected(self) -> None:
        source = [
            "[statedef 0]",
            "[state ]",
            "type=changeestate",
            "trigger1=1",
        ]

        with self.assertRaisesRegex(
            RuntimeError,
            r"cns/state\.cns:3 \(changeestate\)",
        ):
            formatter.verify_state_controller_types_in_lines("cns/state.cns", source)

    def test_mugen_1_state_controller_is_rejected(self) -> None:
        source = [
            "[statedef 0]",
            "[state ]",
            "type=RemapPal",
            "trigger1=1",
        ]

        with self.assertRaisesRegex(RuntimeError, r"RemapPal"):
            formatter.verify_state_controller_types_in_lines("cns/state.cns", source)


if __name__ == "__main__":
    unittest.main()
