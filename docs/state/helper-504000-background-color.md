# 背景色変更Helper

## StateDef 504000: 青暗転初期化

Helper ID `504000`の用途別出現StateDefである。青暗転の寿命、三時間区間、一周期、開始・ピーク・終了時の乗算RGB・加算RGB・彩度、反転フラグおよび`BgPalFX`適用時間をHelper変数へ保存し、同じtickにStateDef `504990`へ遷移する。

暗転開始からピークまでを60tick、ピーク維持と背景復帰を0tickとし、60tick周期を600tickの寿命まで反復する。開始加算RGBとピーク加算RGBの差を60tickで線形補間することで、各成分`8/tick`の減少を維持する。

## StateDef 504010: 突進用黒背景暗転初期化

Helper ID `504010`の用途別出現StateDefである。フェードイン3tick、ピーク維持5tick、フェードアウト3tickを設定する。乗算RGBは通常値`256,256,256`からピーク値`64,64,64`へ変化し、通常明度の25%まで背景を暗くしてから戻す。加算RGBは全区間`0,0,0`、彩度は全区間`256`とする。

RootのStateDef `1201`が画面侵入時に本Helperを一度だけ生成する。

## StateDef 504020: Y技用青背景暗転初期化

Helper ID `504020`の用途別出現StateDefである。RootのStateDef `1301`が10tick目に生成し、20tickのSuperPause中に背景を青く暗くする。寿命と一周期は20tick、開始からピークまで20tickとする。乗算RGBは`84,107,149`、開始加算RGBは`34,46,56`、ピーク加算RGBは`-82,-70,-94`、彩度は`210`、`BgPalFX`適用時間は2tickとする。

Helper本体のAction `505000`は全画面白フラッシュにも使用する。白表示の詳細はStateDef `504900`が適用する。

## StateDef 504990: 共通基盤接続

責務マスク`16`、共通経過tick `0`、最終実行tick `var(1)-1`および初期化完了フラグを設定し、StateDef `599000`へ移る。

## StateDef 504900: 背景色変更と白フラッシュ

用途別出現StateDefが保存した時間区間と開始・ピーク・終了値から、現在周期内の経過tickを求める。暗転開始からピークと、ピークから背景復帰は線形補間し、ピーク区間は指定値を維持して`BgPalFX`を背景へ適用する。キャラクター、Helper、ExplodおよびProjectileのパレットは変更しない。

Helper `504020`本体を画面中央へ置き、`AngleDraw`倍率`40,40`、`SprPriority`値`32767`、通常透過で白面を表示する。共通経過tick `2`〜`4`、`6`、`9`だけ可視にし、ほかの時刻は不可視にする。その他の背景色変更Helperは本体を不可視に保つ。処理後はStateDef `599060`へ進み、設定寿命またはラウンド終了時に共通寿命判定で消滅する。

## 共通モデル契約

背景色の補間はHelper変数だけを使用し、Helper ID、用途番号、発出元StateDefおよびRootの技状態から色を判定しない。Helper `504020`の白フラッシュ表示は、背景色の補間とは別の表示責務として扱う。[ADR 039](../ADR/039-helper-fullscreen-white-flash.md)を参照する。

## 予約範囲

- 専用StateDef：`504000`〜`504999`
- 青暗転Helper ID・初動StateDef：`504000`
- 突進用黒背景暗転Helper ID・用途別初動StateDef：`504010`
- Y技用青背景暗転Helper ID・用途別初動StateDef：`504020`
- 将来の用途別初動StateDef：`504030`から10刻み
- 共通基盤接続StateDef：`504990`
- 共通管理StateDef：`504900`

## 使用変数

[背景色変更Helper変数](var-list-helper-504000.md)を参照する。
