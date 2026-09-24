# フィボナッチ・ライトHelper

## StateDef 502000: 基本黄金角パターン初期化

Helper ID `502000`の用途別初動StateDefである。黄金角係数、生成番号と増分、同一tick生成数、粒子寿命およびHelper寿命をHelper自身の変数へ保存し、同じtickにStateDef `502900`へ遷移する。

## StateDef 502900: 粒子生成・寿命管理

生成番号へ黄金角係数を乗じてAction `18553`の粒子位置を求める。自己遷移によって1tickに37個を生成し、各粒子へ外向きの初速度と加速度を与える。Helper本体は非表示で、600tick経過またはラウンド終了時に消滅する。

使用変数は[フィボナッチ・ライトHelper変数](var-list-helper-502000.md)を参照する。

## 予約範囲

- 専用StateDef：`502000`〜`502999`
- 基本黄金角パターンHelper ID・初動StateDef：`502000`
- 将来の用途別初動StateDef：`502010`から10刻み
- 共通管理StateDef：`502900`
- 粒子Explod ID：`502100`
