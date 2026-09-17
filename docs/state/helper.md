# ヘルパーステート

この文書は、`cns/helper.cns` にあるヘルパー用StateDefを説明する。

## 頭部ヘルパー

### StateDef 99000: ヘルパー振り分け

ヘルパーID `99001` であればStateDef `99001` へ移る。それ以外のヘルパーには、このStateDef内で追加動作を行わない。

### StateDef 99001: 頭部待機

Action `99001`を表示し続け、Rootの位置・向き・アニメーションへ追従する。詳細は[the_head Helper](helper-99001-the-head.md)を参照する。

## オーラヘルパー

### StateDef 99002: オーラ常駐

本体の位置・向き・アニメーション・描画オフセットへ毎フレーム追従する。詳細は[the_aura Helper](helper-99002-the-aura.md)を参照する。

## 頭部オーラヘルパー

### StateDef 99003: 頭部オーラ常駐

頭部Helperの位置・向き・アニメーションへ毎フレーム追従する。詳細は[the_head_aura Helper](helper-99003-the-head-aura.md)を参照する。

### StateDef 99004: Controller

RootのStateDefとprivate-timeを監視し、Helper Armorと技ごとのオーラバウンドを管理する。バウンドの進行状態は本体オーラと頭部オーラから参照される。

#### Helper Armorダメージ取得

`HitOverride`によってStateDef `99004`へ移ったフレームに`GetHitVar(damage)`を取得する。無敵期間用`var(12)`が`0`の場合だけ、ダメージを`var(11)`へ、同じ値を無敵期間用`var(12)`へ設定する。StateDefヘッダーは`MoveType=I`とし、Helper自身への直接ダメージを無効化する。

### StateDef 99101: 4001バウンド定義

RootがStateDef `4001`に入ったときのバウンド設定を、`the_controller`自身の変数へ初期化する。

### StateDef 99102: 4002バウンド定義

RootがStateDef `4002`に入ったときのバウンド設定を、`the_controller`自身の変数へ初期化する。

### StateDef 99103: 4003バウンド定義

RootがStateDef `4003`に入ったときのバウンド設定を、`the_controller`自身の変数へ初期化する。

### StateDef 99199: 常駐Helper最終処理

個別バウンド設定の完了後に経由し、処理完了時に`SelfState value=5150`を実行する。
