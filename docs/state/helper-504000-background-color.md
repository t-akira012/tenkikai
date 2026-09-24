# 背景色変更Helper

## StateDef 504000: 青暗転初期化

Helper ID `504000`の用途別出現StateDefである。青暗転の寿命、色変化周期、乗算RGB、加算RGB初期値、減少量、彩度、反転フラグおよび`BgPalFX`適用時間をHelper変数へ保存し、同じtickにStateDef `504900`へ遷移する。

## StateDef 504900: 背景色変更・寿命管理

用途別出現StateDefが保存した値から、経過tickを用いて加算RGBを周期的に減少させ、`BgPalFX`を背景へ適用する。キャラクター、Helper、ExplodおよびProjectileの色は変更しない。

HelperはPlayerPush、被弾、画面追従、表示および影を無効化し、設定寿命またはラウンド終了時に消滅する。

## 予約範囲

- 専用StateDef：`504000`〜`504999`
- 青暗転Helper ID・初動StateDef：`504000`
- 将来の用途別初動StateDef：`504010`から10刻み
- 共通管理StateDef：`504900`

## 使用変数

[背景色変更Helper変数](var-list-helper-504000.md)を参照する。
