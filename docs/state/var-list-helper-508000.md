# 明光弾攻撃判定Helper変数

明光弾攻撃判定責務を持つHelperへ適用する。両手光弾ではHelper ID `506000`〜`506005`が使用する。

| 変数 | 用途 |
| --- | --- |
| `var(20)`、`var(21)` | Damageと削り`20,3` |
| `var(22)` | Priority `3` |
| `var(23)`、`var(24)` | P1・P2 PauseTime `4,4` |
| `var(25)` | Ground SlideTime `8` |
| `var(26)` | Ground HitTime `10` |
| `var(27)` | Air HitTime `10` |
| `var(28)` | 攻撃開始tick `12` |
| `var(29)` | 命中またはガード済みフラグ |
| `var(30)` | 寿命末尾の攻撃停止時間`20tick` |
| `var(31)` | 位相ごとのHitDef ID `506000`〜`506005` |
| `fvar(16)` | 地上命中X速度`-4` |
| `fvar(17)`、`fvar(18)` | 空中命中・空中ガード速度`-3,-2.5` |
| `fvar(19)` | 地上ガードX速度`-3.5` |

## 共通ヘッダー

`sysvar`は[非常駐Helper共通変数](var-list-helper-transient-common.md)に従う。両手光弾では明光弾表示および三次元巡回移動と同じHelper上で併用する。
