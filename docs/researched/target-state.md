# TargetStateとステート奪取

## TargetStateの調査結果

`TargetState` によるステート奪取について、次の挙動が調査されている。

- TargetStateは、命中後の最速の次フレームで対象のステートを変更する。
- TargetStateは、実際に命中した相手と命中していない相手を区別できない。
- `HitOverride` が発動した相手はTargetを取得できないため、TargetStateの対象にできない。ただし攻撃自体は命中する。
- 相手Helperに対するTargetStateは、相手Helperがガード以外の被弾状態である場合、または `ReversalDef` が成立している場合に効果がある。

TargetStateのパラメータ内で `Target` リダイレクトを直接使用すると、フリーズまたはエラー終了することがある。この挙動は [Target](target.md) にも記載する。

## P2GetP1Stateとの比較

攻撃側の `P2GetP1State`（P2StateNo）とTargetStateでは、ステート奪取のタイミングと対象判定が異なる。

| 項目 | P2GetP1State | TargetState |
| --- | --- | --- |
| 奪取時点 | 命中時点 | 命中直後の次フレーム |
| 命中対象の区別 | 命中した相手を区別する | 命中した相手と未命中の相手を区別できない |
| HitOverride対象 | HitDefでは攻撃自体が命中しない | Targetを取得できず、攻撃自体は命中する |
| Projectileでの挙動 | ステート奪取をしない攻撃と同じ処理になることがある | 対象をTargetとして取得できた場合に使用できる |

ProjectileでのP2GetP1Stateは、処理上の不具合を誘発しやすいという調査結果がある。

## ステート奪取中の実行コンテキスト

ステートを奪われている間は、常時監視ステートの `-3` と `-1` が読み込まれない。読み込ませたステートは、通常のStateDefと同じ処理として実行される。

ステート奪取後に対象を元の処理へ戻すには `SelfState` を使用する。攻撃を再度命中させることで元のステートへ戻る場合もある。

## P1StateNoの相打ち

`P1StateNo` を指定した攻撃が相打ちになると、相手側で意図しないステート番号を読み込むことがある。存在しないステートや攻撃側のステートを読み込む場合があり、変数が変更されるなどの不具合につながる。

この相打ち挙動は `P1StateNo` 使用時の既知の危険な挙動として扱う。`ReversalDef` による相打ちでは同じ危険は確認されていない。

## 未検証事項

- `ReversalDef` でTargetを取得した後、ガード状態のHelperへTargetStateが作用する条件。
- TargetStateでステートを奪われている側の各State Controller・Triggerの詳細な実行可否。
- P2GetP1Stateを指定したProjectileで発生する不具合の再現条件。
