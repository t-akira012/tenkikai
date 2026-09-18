# ADR 016: StateDef 5150の本体専用化

## 状態

採用

## 背景

常駐Helperは処理完了後にStateDef `5150`へ移動して、通常のHelper処理から離脱する。一方、共通StateDef `5150`には本体の死亡状態を前提とした型、移動型、物理、アニメーション、速度、無敵処理が定義されている。これらをHelperへ適用すると、Helperの終了処理と本体の死亡処理が混在する。

## 決定

StateDef `5150`のヘッダーから本体状態の固定指定を削除し、状態設定をState Controllerへ移す。`StateTypeSet`を`!IsHelper`で制限し、本体にだけ`StateType=L`、`MoveType=H`、`Physics=N`を適用する。

StateDef `5150`内ではアニメーション変更を行わない。速度処理と無敵処理は、各State Controllerへ`triggerall=!IsHelper`を付けて本体専用とする。描画優先度は`SprPriority`を`!IsHelper`で制限して本体にだけ適用する。

Helperが`5150`へ移動する場合は、State Controllerを実行せず、常駐Helperの情報を隠す終了経路として利用する。

## 結果

本体は従来どおり死亡処理を行い、Helperは`5150`を経由しても本体用の型、アニメーション、速度、無敵処理を受けない。Helperの終了経路と本体の死亡状態が分離される。
