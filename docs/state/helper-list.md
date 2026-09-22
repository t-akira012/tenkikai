# Helper一覧

常駐HelperはRootのStateDef `-3`が各IDの不存在時に1体ずつ生成する。

| ID | 名前 | 初期StateDef | 主な機能 |
| --- | --- | --- | --- |
| `99001` | `the_head` | `99001000` | 頭部表示とRoot追従 |
| `99002` | `the_aura` | `99002000` | Body Aura表示とRoot追従 |
| `99003` | `the_head_aura` | `99003000` | Head Aura表示とHead追従 |
| `99004` | `the_controller` | `99004000` | Helper Armor、AngleDraw要求・持続カウンター・変換完成値、オーラバウンド、暗転の管理 |

いずれもPause・SuperPause中に長時間動作可能な`player`型Helperである。StateDef対応は[ヘルパーステート](helper.md)を参照する。

非常駐Helperは行動ごとに生成され、自己管理する寿命の終了時に消滅する。

| ID | 名前 | 初期StateDef | 主な機能 |
| --- | --- | --- | --- |
| `500000` | `elliptical_shockwave_left` | `500000` | 楕円衝撃波の左円弧。StateDef `500900`で運動・変形・残像・寿命を管理 |
| `500001` | `elliptical_shockwave_right` | `500001` | 楕円衝撃波の右円弧。StateDef `500901`で運動・変形・残像・寿命を管理 |
| `500010` | `dash_elliptical_shockwave_left` | `500010` | ダッシュ波紋の左円弧。増強した残像を設定してStateDef `500900`へ遷移 |
| `500011` | `dash_elliptical_shockwave_right` | `500011` | ダッシュ波紋の右円弧。増強した残像を設定してStateDef `500901`へ遷移 |

楕円衝撃波の詳細は[楕円衝撃波Helper](helper-500000-elliptical-shockwave.md)を参照する。
