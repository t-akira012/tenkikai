from __future__ import annotations

import unittest

import formatter


class FormatterTest(unittest.TestCase):
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
                "cmd=t-command.cmd",
                "cns=t-constants.cns",
                "st=t-state.cns",
                "st1=t-observ.cns",
                "st2=t-helper.cns",
                "stcommon=t-common1.cns",
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


if __name__ == "__main__":
    unittest.main()
