# Helper一覧

常駐HelperはRootのStateDef `-3`が各IDの不存在時に1体ずつ生成する。

| ID | 名前 | 初期StateDef | 主な機能 |
| --- | --- | --- | --- |
| `99001` | `the_head` | `99001000` | 頭部表示とRoot追従 |
| `99002` | `the_aura` | `99002000` | Body Aura表示とRoot追従 |
| `99003` | `the_head_aura` | `99003000` | Head Aura表示とHead追従 |
| `99004` | `the_controller` | `99004000` | Helper Armor、AngleDraw要求・本体自由傾斜・変換完成値、オーラバウンドの管理 |

いずれもPause・SuperPause中に長時間動作可能な`player`型Helperである。StateDef対応は[ヘルパーステート](helper.md)を参照する。

非常駐Helperは行動ごとに生成され、自己管理する寿命の終了時に消滅する。

| ID | 名前 | 初期StateDef | 主な機能 |
| --- | --- | --- | --- |
| `500000` | `elliptical_shockwave_left` | `500000` | 楕円衝撃波の左円弧。StateDef `500990`から共通基盤へ接続する |
| `500001` | `elliptical_shockwave_right` | `500001` | 楕円衝撃波の右円弧。StateDef `500990`から共通基盤へ接続する |
| `500010` | `dash_elliptical_shockwave_left` | `500010` | ダッシュ波紋の左円弧。増強した残像を設定して共通基盤へ接続する |
| `500011` | `dash_elliptical_shockwave_right` | `500011` | ダッシュ波紋の右円弧。増強した残像を設定して共通基盤へ接続する |
| `500020` | `ground_floating_ripple_left` | `500020` | 足元波紋の左円弧。横長倍率と静止速度を設定して共通基盤へ接続する |
| `500021` | `ground_floating_ripple_right` | `500021` | 足元波紋の右円弧。横長倍率と静止速度を設定して共通基盤へ接続する |
| `500030` | `gravity_sphere_planetary_ring_left` | `500030` | 重力球惑星リングの背面円弧。暗色・収縮・角度揺動を設定して共通基盤へ接続する |
| `500031` | `gravity_sphere_planetary_ring_right` | `500031` | 重力球惑星リングの前面円弧。暗色・収縮・角度揺動を設定して共通基盤へ接続する |
| `500040` | `rush_elliptical_shockwave_left` | `500040` | 突進波紋の左円弧。突進角度、専用倍率と残像を設定して共通基盤へ接続する |
| `500041` | `rush_elliptical_shockwave_right` | `500041` | 突進波紋の右円弧。突進角度、専用倍率と残像を設定して共通基盤へ接続する |
| `501000` | `gravity_sphere` | `501000` | 全設定値を保存し、StateDef `501990`から共通基盤へ接続する |
| `502000` | `fibonacci_light` | `502000` | 黄金角係数を保存し、StateDef `502990`から共通基盤へ接続する |
| `502010` | `gravity_sphere_fibonacci_light` | `502010` | 黄金角係数と局所倍率を保存し、StateDef `502990`から共通基盤へ接続する |
| `502020` | `bright_energy_projectile_fibonacci_light` | `502020` | 親明光弾へ追従し、少数のフィボナッチ粒子光を外向きへ放出する |
| `503000` | `center_shockwave` | `503000` | 表示倍率を保存し、StateDef `503990`から共通基盤へ接続する |
| `504000` | `blue_background_darkening` | `504000` | 青暗転値を保存し、StateDef `504990`から共通基盤へ接続する |
| `504010` | `rush_background_darkening` | `504010` | 突進用黒暗転値を保存し、StateDef `504990`から共通基盤へ接続する |
| `505000` | `rush_horizontal_linear_shockwave` | `505000` | 突進角度と線形衝撃波値を保存し、StateDef `505990`から共通基盤へ接続する |
| `506000`〜`506005` | `two_handed_energy_projectile_phase_N` | `506000`〜`506005` | 位相番号を保存し、明光弾表示・A/B/C三次元巡回・攻撃判定を同じHelperで実行する |
| `509000` | `two_handed_energy_projectile_emitter` | `509000` | RootのStateDefから独立して、A/B/C選択を保持し、対向する明光弾二個を三組生成する |

楕円衝撃波の詳細は[楕円衝撃波Helper](helper-500000-elliptical-shockwave.md)を参照する。
重力球の詳細は[重力球Helper](helper-501000-gravity-sphere.md)を参照する。
フィボナッチ・ライトの詳細は[フィボナッチ・ライトHelper](helper-502000-fibonacci-light.md)を参照する。
中心衝撃波の詳細は[中心衝撃波Helper](helper-503000-center-shockwave.md)を参照する。
背景色変更の詳細は[背景色変更Helper](helper-504000-background-color.md)を参照する。
横線形衝撃波の詳細は[横線形衝撃波Helper](helper-505000-horizontal-linear-shockwave.md)を参照する。
明光弾の詳細は[明光弾Helper](helper-506000-bright-energy-projectile.md)を参照する。
三次元巡回移動の詳細は[三次元巡回移動Helper責務](helper-507000-three-dimensional-orbit.md)を参照する。
攻撃判定の詳細は[明光弾攻撃判定Helper責務](helper-508000-bright-energy-projectile-hitdef.md)を参照する。
発出管理の詳細は[両手光弾発出管理Helper](helper-509000-two-handed-energy-projectile-emitter.md)を参照する。
非常駐Helperの共通遷移は[非常駐Helper共通実行基盤](helper-599000-transient-helper-router.md)を参照する。
