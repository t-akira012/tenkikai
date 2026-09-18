# ADR 012: 常駐Helperの自動最大ライフ維持

## 状態

採用

## 背景

常駐Helperが死亡すると、Helperルーティングや演出・管理処理が停止し、キャラクターの挙動が壊れる。`helpertype=player`の常駐Helperは相手の攻撃対象になるため、常駐中の死亡を防ぐ必要がある。

## 決定

StateDef `-2`のautomation flag群の直後、既存の`SelfState`群およびその他の常時監視処理より前に、Helper全体を対象とする`LifeSet`を置く。

`ishelper`だけを条件にし、Helper番号は指定しない。値にはキャラクター設定の最大ライフ`const(data.life)`を使用し、毎tickすべてのHelperのライフを最大値へ戻す。

## 結果

常駐Helperは死亡状態へ移行せず、`-2`の共通ルーティングと専用処理を継続できる。automation flagはユーザー編集用として`-2`の最上部に維持し、最大ライフ処理はその直後に置く。
