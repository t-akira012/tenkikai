# Trigger記述規則

## `triggerall` と `command`

`triggerall` に `command` トリガーを記述してはならない。

キャラクターの自動操作時には `command` トリガーが機能しないため、`triggerall=command=...` を前提にした条件は成立しない。`command` を使用する場合は、実際に入力遷移を評価する個別の `trigger1`、`trigger2` などへ記述する。

自動操作にも対応させる必要がある処理では、`command` 以外の状態・位置・時間などのトリガーを使用する。
