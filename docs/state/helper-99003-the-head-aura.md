# the_head_aura Helper

## StateDef 99003000: Head Aura追従

| 機能 | 実装 |
| --- | --- |
| 位置 | Head Helperの完成位置へ追従する |
| Offset | Controllerの`fvar(14)`、`fvar(15)`を適用する |
| 向き・Action | Rootの向きとHeadのアニメーション番号・要素位置へ同期する |
| AngleDraw | Controllerの`fvar(9)`〜`fvar(11)`を適用する |
| 表示・残像 | Controllerの`var(22)`にある全体非表示bit 8へ従う |
| 画面外 | `ScreenBound value=0`、カメラ追従なし |

同期値と非同期値はControllerが確定し、Head Aura自身はRootのStateDefから計算しない。処理後はStateDef `99003999`から`5150`へ移る。

Head Auraは`Trans addalpha alpha=128,256`で加算描画する。

所有変数は[the_head_aura変数一覧](var-list-helper-99003.md)を参照する。
