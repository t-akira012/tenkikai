# ADR 032: ラウンド終了後のCtrl制御と接地復帰

## 状態

採用

## 背景

ラウンド決着後に異常に長いStopが発生した。常駐HelperのCtrl、RootのCtrl、ラウンド終了時にRootが空中へ残ることを順に切り分ける必要があった。

WinMUGENの`RoundState`は、`3`がラウンド決着直後のpre-over、`4`が勝利演出中のoverを表す。ラウンド番号を表す`RoundNo`とは別の値である。

常駐Helperはプレイヤー操作の対象ではなく、Ctrlを必要とする処理を持たない。Rootは`RoundState=3`でCtrlを有効にし、空中に残った場合は技途中へ割り込まず専用の接地復帰を行う必要がある。

## 決定

常駐Helperは、毎tick通過する共通ルーターStateDef `99000`の先頭で`CtrlSet value=0`を実行する。ラウンド進行状態にかかわらず、常駐HelperのCtrlは常に無効とする。

RootはStateDef `-2`で`RoundState=3`を監視し、StateDef `303`以外では毎tick`CtrlSet value=1`を実行する。

StateDef `-3`は、`RoundState=3`または`4`、`Pos Y<0`、`StateNo<200`の場合にRootをStateDef `303`へ移す。`StateNo>=200`を技・回避・被弾中として扱い、その途中には接地復帰を開始しない。

StateDef `303`は移動要求を解除し、4tickの間、毎tick位置を`Y=0`、速度を`0,0`へ固定する。`the_controller`へ`4tick / type 3`の全身縦長復元を予約し、終了時にCtrlを有効にしてStateDef `0`へ戻る。StateDef `303`ではPlayerPushとHelper Armorの攻撃受付を無効化する。

Ctrlと遷移のControllerには`ignorehitpause=1`を指定する。

## 結果

常駐HelperがCtrlを有効にしたまま処理される状態を防止する。Rootは技・回避・被弾をStateNo `200`以上で継続し、それらを終えてStateNo `200`未満へ戻った後、空中なら専用復帰で即座に接地する。

WinMUGEN実機で、ラウンド終了時に技途中へ割り込まず、接地復帰後に異常な長時間Stopが発生しないことを確認した。
