# the_aura Helper

## StateDef 99002000: Body Aura追従

| 機能 | 実装 |
| --- | --- |
| 位置・向き・Action | Rootへ同期する |
| AngleDraw | ControllerのBody Aura適用フラグが有効な場合に完成値を使う。Aura Bound中はBoundを優先する |
| Offset | Rootの浮遊表示へ追従し、Body Aura適用中はControllerの完成Y Offsetを使う |
| 表示 | Aura用透過を適用する |
| 残像 | Aura用AfterImageを生成する。StateDef `301`で本体と残像を消し、`302`で再開する |

傾斜の向きは[ADR 008](../ADR/008-aura-facing-synchronization.md)に従う。処理後はStateDef `99002999`から`5150`へ移る。

所有変数は[the_aura変数一覧](var-list-helper-99002.md)を参照する。
