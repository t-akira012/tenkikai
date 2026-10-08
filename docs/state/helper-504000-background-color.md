# 背景色変更Helper

## StateDef 504000: 青暗転初期化

Helper ID `504000`の用途別出現StateDefである。青暗転の寿命、三時間区間、一周期、開始・ピーク・終了時の乗算RGB・加算RGB・彩度、反転フラグおよび`BgPalFX`適用時間をHelper変数へ保存し、同じtickにStateDef `504900`へ遷移する。

暗転開始からピークまでを60tick、ピーク維持と背景復帰を0tickとし、60tick周期を600tickの寿命まで反復する。開始加算RGBとピーク加算RGBの差を60tickで線形補間することで、移行前の各成分`8/tick`減少を維持する。

## StateDef 504010: 突進用黒背景暗転初期化

Helper ID `504010`の用途別出現StateDefである。フェードイン3tick、ピーク維持5tick、フェードアウト3tickを設定する。乗算RGBは通常値`256,256,256`からピーク値`64,64,64`へ変化し、通常明度の25%まで背景を暗くしてから通常値へ戻す。加算RGBは全区間`0,0,0`、彩度は全区間`256`とする。

RootのStateDef `1201`が、Root原点の`ScreenPos X`と進行方向の速度から画面端を横切ったtickを検出し、本Helperを一度だけ生成する。

## StateDef 504900: 背景色変更・寿命管理

用途別出現StateDefが保存した時間区間と開始・ピーク・終了値から、現在周期内の経過tickを求める。暗転開始からピークと、ピークから背景復帰は線形補間し、ピーク区間は指定値を維持して`BgPalFX`を背景へ適用する。キャラクター、Helper、ExplodおよびProjectileの色は変更しない。

用途別初期化StateDefと共通実行StateDefの両方でHelper本体を不可視にする。HelperはPlayerPush、被弾、画面追従、表示および影を無効化し、設定寿命またはラウンド終了時に消滅する。

## 共通モデル契約

[共通エフェクト設計・実装規約](../design/effect/AGENTS.md)により、背景色変更の用途別パターンは、個別数値をHelper変数へ保存して同じ共通実行StateDef `504900`へ遷移する。StateDef `504900`はHelper ID、用途番号、発出元StateDefおよびRootの技状態を参照しない。

## 予約範囲

- 専用StateDef：`504000`〜`504999`
- 青暗転Helper ID・初動StateDef：`504000`
- 突進用黒背景暗転Helper ID・用途別初動StateDef：`504010`
- 将来の用途別初動StateDef：`504020`から10刻み
- 共通管理StateDef：`504900`

## 使用変数

[背景色変更Helper変数](var-list-helper-504000.md)を参照する。
