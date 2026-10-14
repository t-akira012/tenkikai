# 両手光弾発出管理Helper変数

## 通常変数

| 変数 | 用途 |
| --- | --- |
| `var(0)` | 二個一組の生成間隔`6tick` |
| `var(1)` | 生成組数`3` |
| `var(2)` | 各明光弾の発出開始基準の安全上限`600tick` |
| `var(3)` | 発出管理Helper寿命`60tick` |
| `var(4)` | 最初の明光弾入口StateDef `506000` |
| `var(5)` | Root基準の発出中心Y Offset `-55px` |
| `var(6)` | A/B/C分岐選択。`1`はA、`2`はB、`3`はC。初期値は`1` |

## 共通ヘッダー

`sysvar`は[非常駐Helper共通変数](var-list-helper-transient-common.md)に従う。責務bitmapは`512`、最終実行tickは`59`とする。
