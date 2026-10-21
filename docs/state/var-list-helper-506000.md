# 明光弾Helper変数

明光弾表示責務を持つHelperへ適用する。両手光弾ではHelper ID `506000`〜`506005`が使用する。

## 明光弾表示責務

| 変数 | 用途 |
| --- | --- |
| `var(0)` | Action番号`506000` |
| `var(1)` | 光弾本体の色反転フラグ。両手光弾では`0` |
| `var(2)` | 出現時間`12tick` |
| `var(3)` | 消滅時間`20tick` |
| `var(4)`、`var(5)` | `addalpha`のAlpha `192,256` |
| `fvar(0)`、`fvar(1)` | 基準X・Y倍率`1.20` |
| `fvar(2)` | 出現・消滅の現在倍率係数 |

## AfterImage・放出粒子

| 変数 | 用途 |
| --- | --- |
| `var(32)` | AfterImage時間`-1` |
| `var(33)` | AfterImage長さ`8` |
| `var(34)`、`var(35)` | `timegap`・`framegap`。各`2` |
| `var(36)` | `palcolor`。`128` |
| `var(37)` | 残像の色反転フラグ。`0` |
| `var(38)`〜`var(40)` | `palbright`。`0,0,0` |
| `var(41)`〜`var(43)` | `palcontrast`。`96,128,192` |
| `var(44)`〜`var(46)` | `palpostbright`。`0,0,0` |
| `var(47)` | 放出粒子Helper ID・StateDef `502020` |
| `var(48)` | AfterImage・放出粒子開始tick。`11` |
| `var(49)` | AfterImage開始済みフラグ |
| `fvar(3)`〜`fvar(5)` | `palmul`。`0.25,0.30,0.45` |

## 共通ヘッダー

`sysvar`は[非常駐Helper共通変数](var-list-helper-transient-common.md)に従う。両手光弾では[三次元巡回移動Helper変数](var-list-helper-507000.md)および[明光弾攻撃判定Helper変数](var-list-helper-508000.md)と同じHelper上で併用し、責務bitmapを`448`、最終実行tickを`599`とする。
