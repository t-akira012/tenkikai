from __future__ import annotations

import unittest

import formatter


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
            'text = "private-time: %d\\npos y: %f"',
        ]

        actual = formatter.transform_definition(source, format_states=True)

        self.assertIn('text="private-time: %d\\npos y: %f"', actual)

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

    def test_legacy_cns_is_split_by_state_number(self) -> None:
        source = formatter.transform_definition(
            [
                "[Data]",
                "life = 1000",
                "",
                "[Statedef 100]",
                "type = S",
                "",
                "[Statedef 99000]",
                "type = S",
                "",
                "[Statedef -2]",
                "[State -2, test]",
                "type = Null",
            ],
            format_states=True,
        )

        constants, states, observers, helpers = formatter.split_cns(source)

        self.assertIn("[Data]", constants)
        self.assertIn("[statedef 100]", states)
        self.assertIn("[statedef -2]", observers)
        self.assertIn("[statedef 99000]", helpers)

    def test_def_references_are_rewritten(self) -> None:
        source = [
            "[Files]",
            "cmd = t.cmd",
            "cns = t.cns",
            "st = t.cns",
            "stcommon = common1.cns",
        ]

        actual = formatter.update_def(source)

        self.assertEqual(
            actual,
            [
                "[Files]",
                "cmd=cns/command.cmd",
                "cns=cns/constants.cns",
                "st=cns/state.cns",
                "st1=cns/observ.cns",
                "st2=cns/helper.cns",
                "stcommon=cns/common1.cns",
            ],
        )

    def test_other_state_files_take_priority_over_common_states(self) -> None:
        common = formatter.transform_definition(
            [
                ";--------------------",
                "[Statedef 0]",
                "type = S",
                ";--------------------",
                "[Statedef 100]",
                "type = S",
                ";--------------------",
                "[Statedef 105]",
                "type = S",
            ],
            format_states=True,
        )

        actual, removed = formatter.remove_duplicate_common_states(common, {100, 105})

        self.assertIn("[statedef 0]", actual)
        self.assertNotIn("[statedef 100]", actual)
        self.assertNotIn("[statedef 105]", actual)
        self.assertEqual(removed, [100, 105])

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


if __name__ == "__main__":
    unittest.main()
