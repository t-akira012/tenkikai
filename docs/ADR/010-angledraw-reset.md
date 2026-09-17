# ADR 010: AngleDrawの無効化時に残留傾斜を解除する

## 状態

採用

## 背景

WinMUGENの`AngleDraw`は、別のStateDefへ移動しただけでは前の傾斜が自動的に中立へ戻らないことがある。ダッシュ以外の技や演出でも傾斜を使用するため、特定のダッシュStateDefだけを傾斜状態として扱う方法では、利用範囲を拡張できず残留傾斜も除去できない。

## 決定

通常変数`var(5)`を、現在のStateDefがAngleDrawを有効にしているかを示すフラグとして使用する。入力ビット用に予約された変数は再利用しない。

StateDef `-2` は毎tick、`var(5)`を`0`（false）へ戻し、AngleDrawを中立値へ設定して前のStateDefから残った傾斜を解除する。

AngleDrawを必要とするStateDefは、自身のAngleDraw処理と同じ条件で`var(5)=1`（true）を設定する。110／111は現在trueになるStateDefであり、傾斜対象をそれらに限定しない。将来の技や演出StateDefも、同じ有効化手順で傾斜を使用できる。

Body auraはRootの`var(5)`を参照し、false時には角度を中立値へ戻す。RootとAuraで独立した有効判定や符号補正は追加しない。

## 結果

AngleDrawを使用しないStateDefへ移行した時点で、`-2`が残留傾斜を自動的に除去する。傾斜を使う技や演出はStateDef単位で明示的に有効化でき、ダッシュ専用の判定に依存しない。
