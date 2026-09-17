# ADR 009: 常駐描画Helperの画面外移動

## 状態

採用

## 背景

頭部やAuraなどのアニメーション描画を担当する常駐Helperは、演出上の位置移動によって画面外へ出ることがある。一方、`helpertype=normal`へ変更すると、常駐Helperに必要なルーティング構造が壊れる。

## 決定

常駐描画Helperは`helpertype=player`を維持する。画面外への移動が必要なHelperは、専用StateDefで`ScreenBound value=0`を毎tick適用し、`movecamera=0,0`でカメラを追従させない。

`ScreenBound`は各Helperへ個別に適用する。Rootや他のHelperへ影響を与える共通設定として扱わない。この方針を頭部、Body aura、Head auraなど、アニメーション描画を担当する常駐Helperへ適用する。

## 結果

常駐Helperの`-2`ルーティングを維持しながら、描画用Helperを画面外へ移動できる。Helperごとに画面外移動の要否を制御でき、カメラの意図しない移動も防止できる。
