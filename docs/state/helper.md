# ヘルパーステート

## 共通ルーター

StateDef `99000`はHelper IDを専用処理へ振り分ける。

| Helper | 処理StateDef | 最終StateDef | 詳細 |
| --- | --- | --- | --- |
| `99001` the_head | `99001000` | `99001999` | [頭部追従](helper-99001-the-head.md) |
| `99002` the_aura | `99002000` | `99002999` | [Body Aura追従](helper-99002-the-aura.md) |
| `99003` the_head_aura | `99003000` | `99003999` | [Head Aura追従](helper-99003-the-head-aura.md) |
| `99004` the_controller | `99004000` | `99004999` | [Controller処理列](helper-99004-the-controller.md) |

各最終StateDefは`SelfState value=5150`を実行する。

## the_controller内部StateDef

| StateDef | 機能 |
| --- | --- |
| `99004001`、`99004010` | ライフ管理ルーターとHelper Armor処理 |
| `99004002`、`99004011`〜`99004013` | オーラバウンドルーターと3種類の定義 |
| `99004006`、`99004030` | AngleDraw要求ルーターと持続カウンター・本体自由傾斜・完成値処理 |
| `99004005`、`99004021`〜`99004022` | Head位置補正ルーターと異形回避・本体自由傾斜補正 |
| `99004004`、`99004020` | Head・Head Aura変換完成ルーターと完成処理 |
| `99004003`、`99004100`、`99004190` | 全画面色変更ルーター、全画面黒設定、`AllPalFX`共通実行 |
