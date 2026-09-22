# the_controller Helper変数一覧

## 通常変数

| 変数 | 用途 |
| --- | --- |
| `var(0)` | オーラバウンド有効フラグ |
| `var(1)` | オーラバウンド消費開始までの待機tick |
| `var(11)` | Helper Armorが受けた保留ダメージ |
| `var(12)` | 次のダメージ受付までの無敵期間 |
| `var(13)` | PlayerPush無効化フラグ |
| `var(14)` | Helper Armor無敵フラグ |
| `var(15)` | 保存済みRootアニメーション番号 |
| `var(16)` | Rootアニメーション変更時の`abs(root,animtime)` |
| `var(17)` | Head Aura Offset非同期フラグ |
| `var(18)` | Head Aura AngleDraw非同期フラグ |
| `var(19)` | Body AngleDraw適用フラグ |
| `var(20)` | Body Aura AngleDraw適用フラグ |
| `var(21)` | 暗転番号と残り時間のビットフィールド |
| `var(22)` | Head系表示制御ビットフィールド |

### `var(21)` bit割当

| bit | 用途 |
| ---: | --- |
| 0〜15 | 暗転残り時間、0〜65535tick |
| 16〜20 | 暗転番号、0〜31 |
| 21〜31 | 未使用 |

### `var(22)` bit割当

| bit | マスク | 用途 |
| ---: | ---: | --- |
| 0 | `1` | Head非表示 |
| 1 | `2` | Head Aura非表示 |
| 2 | `4` | Head残像非表示 |
| 3 | `8` | Head Aura残像非表示 |
| 4〜31 | — | 未使用 |

## 浮動小数点変数

| 変数 | 用途 |
| --- | --- |
| `fvar(0)` | オーラバウンド残量 |
| `fvar(1)` | オーラバウンドの毎tick消費量 |
| `fvar(2)`〜`fvar(4)` | Head完成AngleDrawの角度、X倍率、Y倍率 |
| `fvar(5)`〜`fvar(7)` | Body系完成AngleDrawのX倍率、Y倍率、角度 |
| `fvar(8)` | Body系完成Y Offset |
| `fvar(9)`〜`fvar(11)` | Head Aura完成AngleDrawの角度、X倍率、Y倍率 |
| `fvar(12)`、`fvar(13)` | Head完成X・Y Offset |
| `fvar(14)`、`fvar(15)` | Head Aura完成X・Y Offset |
| `fvar(16)`、`fvar(17)` | Head系の完成X・Y Pos補正 |

`var(15)`と`var(16)`の更新順序は[Rootアニメーション時間保持規約](../AGENTS.root-animtime.md)に従う。
