# 中心衝撃波Helper

## StateDef 503000: 基本パターン初期化

Helper ID `503000`の用途別出現StateDefである。Action、表示倍率および描画優先順位をHelper変数へ保存し、同じtickにStateDef `503990`へ遷移する。

## StateDef 503990: 共通基盤接続

責務マスク`8`、共通経過tick `0`、アニメーション終了管理を示す最終実行tick `-1`および初期化完了フラグを設定し、StateDef `599000`へ移る。

## StateDef 503900: 表示・寿命管理

用途別出現StateDefが保存したAction、表示倍率および描画優先順位で生成位置へ表示する。Action終了時は終了要求bitを設定し、StateDef `599050`へ進む。HelperはPlayerPush、被弾、画面追従および影を無効化し、共通寿命判定で消滅する。

## 予約範囲

- 専用StateDef：`503000`〜`503999`
- 基本パターンHelper ID・初動StateDef：`503000`
- 将来の用途別初動StateDef：`503010`から10刻み
- 共通基盤接続StateDef：`503990`
- 共通管理StateDef：`503900`

## 使用変数

[中心衝撃波Helper変数](var-list-helper-503000.md)を参照する。
