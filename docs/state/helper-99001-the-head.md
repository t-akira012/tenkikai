# the_head Helper

## StateDef 99001000: 頭部追従

| 機能 | 実装 |
| --- | --- |
| 位置 | Root位置へ追従し、Controllerの`fvar(16)`、`fvar(17)`をPos補正として加える |
| Offset | Controllerの`fvar(12)`、`fvar(13)`を適用する |
| 向き・Action | Rootの向きへ同期し、Controllerの`var(24)`で完成した前方・正面・後方視線からAction `99001`、`99011`、`99012`を選択する |
| AngleDraw | Controllerの`fvar(2)`〜`fvar(4)`を適用する |
| 表示・残像 | Controllerの`var(22)`にあるHead用ビットへ従う |
| 画面外 | `ScreenBound value=0`、カメラ追従なし |

Head自身はRootのStateDefから変換値を計算しない。処理後はStateDef `99001999`から`5150`へ移る。

視線はControllerの完成表示bitに従い、bit 1ならAction `99001`、bit 2ならAction `99011`、bit 3ならAction `99012`を使用する。各Actionは単一の無限時間要素とし、Head自身は距離やRootのStateDefを判定しない。

Headは`Trans addalpha alpha=128,128`で半透明描画する。

所有変数は[the_head変数一覧](var-list-helper-99001.md)を参照する。
