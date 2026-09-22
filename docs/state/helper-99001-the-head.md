# the_head Helper

## StateDef 99001000: 頭部追従

### 画面外移動許可

常駐Helperの`helpertype=player`を維持したまま、`ScreenBound value=0`で画面外への移動を許可する。カメラは追従させない。

### Root位置追従

Rootの位置へ毎フレーム追従する。

### Head完成Pos補正

Root基準位置を設定した後、`the_controller`が保持するHead完成Pos補正XとYを一つの`PosAdd`で毎tick適用する。Head自身はRootのStateNo、位置補正パターンまたは位置式を持たない。

### Head完成Offset

`the_controller`が保持するHead完成OffsetのX値とY値を、一つの`Offset`で毎tick適用する。Head自身はOffset式やRootのStateDefによる適用分岐を持たない。

### Root向き同期

Rootの向きと`facing`を一致させるため、Rootに合わせて`Turn`する。

### Rootアニメーション同期

Rootのアニメーションを枚数と要素位置を含めて同期する。

頭部自身はAngleDraw値を計算せず、`the_controller`が保持するHead完成角度、X倍率、Y倍率を一つの`AngleDraw`で毎tick使用する。

### 表示と残像

`the_controller`のHead非表示ビットが有効な場合は頭部を非表示にする。Head残像非表示ビットが有効な場合は`AfterImageTime time=0`で残像を非表示にし、内部の残像生成済みフラグを`0`へ戻す。残像非表示ビットが無効な場合は通常のAfterImage表示を行う。Head自身はRootのStateNoを判定しない。

## StateDef 99001999: 最終処理

頭部追従の完了後に`SelfState value=5150`を実行する。
