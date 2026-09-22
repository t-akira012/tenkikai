# Helper一覧

常駐HelperはRootのStateDef `-3`が各IDの不存在時に1体ずつ生成する。

| ID | 名前 | 初期StateDef | 主な機能 |
| --- | --- | --- | --- |
| `99001` | `the_head` | `99001000` | 頭部表示とRoot追従 |
| `99002` | `the_aura` | `99002000` | Body Aura表示とRoot追従 |
| `99003` | `the_head_aura` | `99003000` | Head Aura表示とHead追従 |
| `99004` | `the_controller` | `99004000` | Helper Armor、変換完成値、オーラバウンド、暗転の管理 |

いずれもPause・SuperPause中に長時間動作可能な`player`型Helperである。StateDef対応は[ヘルパーステート](helper.md)を参照する。
