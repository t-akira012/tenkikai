# throw-v1

## 根拠

KFM StateDef `800`の投げ始動、StateDef `810`の投げ実行、StateDef `820`・`821`の被投げ処理を基準とする。

## 試験候補

- State属性：`S, NT`
- HitFlag：`M-`
- Priority：`1, Miss`
- Spark：なし
- Guard Distance：`0`
- Fall：有効
- 投げ成立時は攻撃側・相手側の専用Stateへ遷移する。
- 投げ中は`TargetBind`で相手を継続拘束する。
- ダメージ：`78`
- 解放時速度：`2.8, -7`
- 落下加速度：`0.4`
- 防御突破、無敵、アーマー、ReversalDef：なし

TargetStateを使用するため、投げ中断時と拘束喪失時に相手を自己Stateへ戻す経路を必須とする。投げ間合いとTargetBind座標はTENKIKAIの素材から個別に解決する。
