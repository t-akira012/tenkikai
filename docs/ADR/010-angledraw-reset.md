# ADR 010: AngleDrawの無効化時に残留傾斜を解除する

## 状態

採用

## 背景

WinMUGENの`AngleDraw`は、別のStateDefへ移動しただけでは前の傾斜が自動的に中立へ戻らないことがある。ダッシュ以外の技や演出でも傾斜を使用するため、特定のダッシュStateDefだけを傾斜状態として扱う方法では、利用範囲を拡張できず残留傾斜も除去できない。

## 決定

AngleDrawの値と適用フラグは`the_controller`が管理する。個別StateDefはAngleDrawの値や有効状態を管理しない。本体自由傾斜では、`the_controller`がRootの状態を監視して目標角度、角速度および残存時間を自身へ登録する。

RootのStateDef `-2`は毎tick、AngleDrawを中立値へ設定して前tickの傾斜と倍率を解除する。その後、`the_controller`のBody適用フラグが有効な場合だけ、Controllerが保持する完成角度と完成倍率をRootへ適用する。

AngleDrawを必要とする挙動は、`the_controller`で完成値と適用フラグを設定する。Rootの個別StateDefへAngleDrawまたは専用フラグを追加してはならない。

RootはHelperより先に処理されるため、StateDef `-2`は`the_controller`が前tickに完成させた値を使用する。この1tick遅延は許容し、Root側へ補償用のAngleDraw状態を追加しない。

Body AuraはControllerのBody Aura適用フラグを参照し、Controllerが保持するBody系の完成角度と完成倍率を使用する。RootとAuraで独立した計算式や符号補正は追加しない。Aura Bound中はBoundを優先する。

## 結果

AngleDrawを使用しない挙動へ移行した時点で、`-2`が残留傾斜を自動的に除去する。新しい技や演出はController側の値生成だけを追加し、RootとBody Auraの共通適用口を変更しない。
