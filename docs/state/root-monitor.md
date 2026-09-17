# the_root_monitor StateDef

`the_root_monitor`の常駐Helper内で行う挙動ルーティングを記載する。

## ステート遷移

### 個別ID集約

常駐Helperの`StateDef -2`から共通中継StateDefへ戻り、Helper IDに応じて`the_root_monitor`の専用StateDefへ振り分ける。

### バウンド集約

RootのStateNoと`private-time`を監視し、バウンド発動条件を判定する。発動時は対応するバウンド個別StateDefへ遷移する。

### バウンド個別

技ごとの拡張幅、保持時間、復帰速度を`the_root_monitor`自身の変数へ設定する。設定後は次フレームの`-2`ルーティングでバウンド集約へ戻り、共通消費処理を継続する。

### 別挙動集約・別挙動個別

バウンド以外の挙動も、挙動集約StateDefで発動条件を判定し、挙動個別StateDefで処理する。個別処理の完了後は監視StateDefへ直接戻さず、次フレームの`-2`ルーティングへ戻す。

## 現在のバウンド定義

### StateDef 99004: バウンド監視・共通消費

Rootの状態を監視し、バウンド個別StateDefへの遷移と、設定済みバウンドの消費・復帰を行う。

### StateDef 99101: 4001バウンド個別

StateDef `4001`用のバウンド設定を初期化する。

### StateDef 99102: 4002バウンド個別

StateDef `4002`用のバウンド設定を初期化する。

### StateDef 99103: 4003バウンド個別

StateDef `4003`用のバウンド設定を初期化する。
