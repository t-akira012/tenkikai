# the_controller StateDef

`the_controller`の常駐Helper内で行う挙動ルーティングを記載する。

## Helper Armor

### StateDef 99004: 攻撃受付とダメージ取得

Action `99004`の当たり判定をRootの位置へ常時追従させ、PlayerPushで相手を押し返しながら、`HitOverride`によって相手の攻撃を受ける。命中時は`GetHitVar(damage)`を`var(11)`へ保存し、同じ値を`var(12)`へ設定してダメージ量に応じた無敵期間を開始する。本体は次のフレームに`var(11)`を読み取ってライフへ反映し、その後`var(11)`を初期化する。

## ステート遷移

### 個別ID集約

常駐Helperの`StateDef -2`から共通中継StateDefへ戻り、Helper IDに応じて`the_controller`の専用StateDefへ振り分ける。

### バウンド集約

RootのStateNoと`private-time`を監視し、バウンド発動条件を判定する。発動時は対応するバウンド個別StateDefへ遷移する。

### バウンド個別

技ごとの拡張幅、保持時間、復帰速度を`the_controller`自身の変数へ設定する。個別処理の完了後は最終処理StateDefへ遷移し、完了時に`SelfState value=5150`を実行する。次フレームの`-2`ルーティングでバウンド集約へ戻り、共通消費処理を継続する。

### 別挙動集約・別挙動個別

バウンド以外の挙動も、挙動集約StateDefで発動条件を判定し、挙動個別StateDefで処理する。個別処理の完了後は最終処理StateDefで完了処理を行い、`SelfState value=5150`を実行する。監視StateDefへは次フレームの`-2`ルーティングから戻る。

## 現在のバウンド定義

### StateDef 99004: バウンド監視・共通消費

Rootの状態を監視し、バウンド個別StateDefへの遷移と、設定済みバウンドの消費・復帰を行う。

### StateDef 99101: 4001バウンド個別

StateDef `4001`用のバウンド設定を初期化する。

### StateDef 99102: 4002バウンド個別

StateDef `4002`用のバウンド設定を初期化する。

### StateDef 99103: 4003バウンド個別

StateDef `4003`用のバウンド設定を初期化する。

### StateDef 99199: 常駐Helper最終処理

個別バウンド処理の完了後に経由し、`SelfState value=5150`で終了する。
