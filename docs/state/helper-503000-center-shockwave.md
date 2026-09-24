# 中心衝撃波Helper

## StateDef 503000: 基本パターン初期化

Helper ID `503000`の用途別初動StateDefである。表示倍率をHelper変数へ保存し、同じtickにStateDef `503900`へ遷移する。

## StateDef 503900: 表示・寿命管理

Action `16998`を生成位置へ倍率`0.5`で表示する。HelperはPlayerPush、被弾、画面追従および影を無効化し、Action終了またはラウンド終了時に消滅する。

## 予約範囲

- 専用StateDef：`503000`〜`503999`
- 基本パターンHelper ID・初動StateDef：`503000`
- 将来の用途別初動StateDef：`503010`から10刻み
- 共通管理StateDef：`503900`

## 使用変数

[中心衝撃波Helper変数](var-list-helper-503000.md)を参照する。
