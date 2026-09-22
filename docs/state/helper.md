# ヘルパーステート

この文書は、`cns/helper.cns` にあるヘルパー用StateDefを説明する。

## 共通ルーター

### StateDef 99000: Helper ID振り分け

常駐HelperをIDに対応する専用StateDefへ振り分ける。ID `99001`は`99001000`、ID `99002`は`99002000`、ID `99003`は`99003000`、ID `99004`は`99004000`へ移る。

## the_head

### StateDef 99001000: 頭部追従

Action `99001`を表示し、Rootの位置・向き・アニメーションへ追従する。処理後は`99001999`へ移る。詳細は[the_head Helper](helper-99001-the-head.md)を参照する。

### StateDef 99001999: 最終処理

`the_head`の処理完了後に`SelfState value=5150`を実行する。

## the_aura

### StateDef 99002000: オーラ追従

Rootの位置・向き・アニメーション・描画オフセットへ追従し、処理後は`99002999`へ移る。詳細は[the_aura Helper](helper-99002-the-aura.md)を参照する。

### StateDef 99002999: 最終処理

`the_aura`の処理完了後に`SelfState value=5150`を実行する。

## the_head_aura

### StateDef 99003000: 頭部オーラ追従

頭部Helperの位置・向き・アニメーションへ追従し、処理後は`99003999`へ移る。詳細は[the_head_aura Helper](helper-99003-the-head-aura.md)を参照する。

### StateDef 99003999: 最終処理

`the_head_aura`の処理完了後に`SelfState value=5150`を実行する。

## the_controller

### StateDef 99004000: the_controller集約

Rootを監視し、最初の挙動塊のルーター`99004001`へ移る。詳細は[the_controller Helper](helper-99004-the-controller.md)を参照する。

### StateDef 99004001: ライフ管理ルーター

毎tick実行するライフ管理個別StateDef `99004010`へ移る。

### StateDef 99004010: ライフ管理個別

Helper Armorのダメージ取得、無敵期間、private-timeを管理し、次の挙動塊である`99004002`へ移る。

### StateDef 99004002: オーラバウンドルーター

RootのStateNoとprivate-timeを監視し、該当するバウンド個別StateDefへ振り分ける。該当しない場合はHead位置補正ルーター`99004005`へ移る。

### StateDef 99004005: Head位置補正ルーター

Rootの状態からHead位置補正パターンを一つ、または0個選択する。該当しない場合はHead・Head Aura変換完成ルーター`99004004`へ移る。

### StateDef 99004021: 異形回避Head位置補正

Rootアニメーション前半でHead完成Pos補正を中心位置まで線形補間し、`99004004`へ移る。

### StateDef 99004022: 前方ダッシュHead位置補正

前方ダッシュ用のHead完成Pos補正を設定し、`99004004`へ移る。

### StateDef 99004023: 後方ダッシュHead位置補正

後方ダッシュ用のHead完成Pos補正を設定し、`99004004`へ移る。

### StateDef 99004004: Head・Head Aura変換完成ルーター

毎tick実行するHead・Head Aura変換完成個別StateDef `99004020`へ移る。

### StateDef 99004020: Head・Head Aura変換完成個別

HeadとHead Auraの対象別完成OffsetおよびAngleDrawを確定し、暗転個別挙動ルーター`99004003`へ移る。

### StateDef 99004003: 暗転個別挙動ルーター

暗転ビットフィールドの残り時間と暗転番号を読み、対応する色指定個別StateDefへ振り分ける。暗転がない場合と未割当の番号では`99004999`へ移る。

### StateDef 99004011: 4001バウンド定義

RootのStateDef `4001`に対応するバウンド設定を適用し、Head位置補正ルーター`99004005`へ移る。

### StateDef 99004012: 4002バウンド定義

RootのStateDef `4002`に対応するバウンド設定を適用し、Head位置補正ルーター`99004005`へ移る。

### StateDef 99004013: 4003バウンド定義

RootのStateDef `4003`に対応するバウンド設定を適用し、Head位置補正ルーター`99004005`へ移る。

### StateDef 99004100: 暗転番号0・全画面黒

`AllPalFX`を1tick適用して画面全体を黒にし、`99004999`へ移る。

### StateDef 99004999: 最終処理

`the_controller`の処理完了後に`SelfState value=5150`を実行する。
