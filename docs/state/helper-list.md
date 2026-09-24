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
| `500020` | `ground_floating_ripple_left` | `500020` | 足元波紋の左円弧。横長倍率と静止速度を設定してStateDef `500900`へ遷移 |
| `500021` | `ground_floating_ripple_right` | `500021` | 足元波紋の右円弧。横長倍率と静止速度を設定してStateDef `500901`へ遷移 |
| `500030` | `gravity_sphere_planetary_ring_left` | `500030` | 重力球惑星リングの背面円弧。暗色・収縮・角度揺動を設定してStateDef `500902`へ遷移 |
| `500031` | `gravity_sphere_planetary_ring_right` | `500031` | 重力球惑星リングの前面円弧。暗色・収縮・角度揺動を設定してStateDef `500902`へ遷移 |
| `501000` | `gravity_sphere` | `501000` | 全設定値を保存し、StateDef `501900`で出現・三層内部流動・浮遊・寿命を共通実行する |
| `502000` | `fibonacci_light` | `502000` | 黄金角係数を保存し、StateDef `502900`で全画面へ光粒子を展開する |
| `503000` | `center_shockwave` | `503000` | 表示倍率を保存し、StateDef `503900`で中心から円形衝撃波を広げる |
| `504000` | `background_color` | `504000` | 青暗転値を保存し、StateDef `504900`で背景だけへ色変化を適用する |

楕円衝撃波の詳細は[楕円衝撃波Helper](helper-500000-elliptical-shockwave.md)を参照する。
重力球の詳細は[重力球Helper](helper-501000-gravity-sphere.md)を参照する。
フィボナッチ・ライトの詳細は[フィボナッチ・ライトHelper](helper-502000-fibonacci-light.md)を参照する。
中心衝撃波の詳細は[中心衝撃波Helper](helper-503000-center-shockwave.md)を参照する。
背景色変更の詳細は[背景色変更Helper](helper-504000-background-color.md)を参照する。
