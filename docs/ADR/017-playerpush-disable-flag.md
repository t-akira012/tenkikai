# ADR 017: the_controllerのPlayerPush無効化フラグ

## 状態

採用

## 背景

`the_controller`のHelper Armorは、相手との接触判定を保持するために`PlayerPush`を使用する。一方、相手をすり抜ける挙動では、Helper Armorの接触判定がRootの移動を妨げる。

技や移動のStateDefへHelper操作を分散させず、Rootの現在StateDefに応じて`the_controller`自身が接触判定を切り替える必要がある。

## 決定

`the_controller`のHelper Armor状態ビットフィールド`var(11)`のbit 24をPlayerPush無効化フラグとする。共通IDルーティング後、個別挙動1のライフ管理へ移る前に、Rootの`StateNo`を監視してフラグを定義する。

フラグは各tickの判定前に解除し、同じ変数のダメージと無敵期間領域は保持する。Rootが前方近距離ワープ予備StateDef `100`、後方近距離ワープ予備StateDef `105`、前方ダッシュStateDef `110`、後方ダッシュStateDef `111`、または異形回避StateDef `300`〜`302`の場合にbit 24を設定する。ライフ管理ではbit 24が無効な場合に`PlayerPush`を有効とし、有効な場合に`PlayerPush`を無効とする。

PlayerPush無効化の対象となるRootのStateDefは、`the_controller`の監視処理へ集約する。Root側の各StateDefからHelper変数を直接変更しない。

## 結果

Helper Armorは通常時の接触判定を維持しながら、指定された挙動中だけ相手をすり抜けられる。判定をライフ管理前に完了させるため、同じtickのPlayerPush処理へ反映できる。

フラグを毎tick再定義することで、すり抜け挙動の終了後にPlayerPushの無効状態が残留しない。
