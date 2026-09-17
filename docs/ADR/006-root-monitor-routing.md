# ADR 006: the_root_monitorの挙動ルーティング

## 状態

採用

## 背景

`the_root_monitor`はオーラバウンド以外の挙動も管理する。各挙動の判定と処理を一つのStateDefへ集約すると、監視条件と個別処理が混在し、追加時の影響範囲が大きくなる。

## 決定

常駐Helperの共通IDルーティング後、`the_root_monitor`内の挙動を次の階層で分離する。

```text
個別ID集約
→ 挙動集約
→ 挙動個別
```

バウンドでは、`bound集約 → bound個別`の順に遷移する。別の挙動を追加する場合も、`別挙動集約 → 別挙動個別`の階層を追加する。

個別挙動用StateDefの処理完了後は監視StateDefへ直接戻さず、次フレームの`StateDef -2`から共通IDルーティングを経由して監視へ復帰する。監視StateDefへ直接復帰すると、発動条件が残ったまま再び個別挙動用StateDefへ遷移し、同じ遷移を繰り返す無限ループになって必ず起動時にクラッシュする。

## 結果

挙動の追加は対応する集約StateDefと個別StateDefの増設で行える。共通ルーティング、挙動判定、個別処理の責務が分離され、Root側の技StateDefへ演出制御を追加せずに拡張できる。

具体的なStateDef番号と現在の遷移は[the_root_monitor StateDef](../state/root-monitor.md)に記載する。
