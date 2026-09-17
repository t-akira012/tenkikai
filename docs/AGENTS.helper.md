# Helperコーディング規約

## 常駐Helperの定義

- 常駐Helperとは、ラウンド中に継続して存在し、本体の常時監視から存在確認と再生成を行い、専用StateDefで毎フレーム処理するHelperを指す。
- HelperType を Player にすることで、常駐helperとして機能する。常駐helperは StateDef -2, -3 を読み込む
- 同一IDは1体以下に制限する。
- 常駐Helperは必ずRootから生成し、HelperからHelperを生成する孫Helper構成は禁止する。

## Helperルーティング規約

- StateDef `-2` での Helper 処理はには常駐Helperのルーティングだけを記述する。
- ルーティング以外のHelper処理を `-2` に記述しても、機能しない。
- 位置、アニメーション、表示などの実処理は、ルーティング先の個別StateDefで行う。
- 非常駐Helperは常駐Helperルーティングの対象外とする。

## Helperの機能とアニメーション

Helperの役割は固定しない。Helperは、変数管理、時間・状態の監視、アニメーション描画、エフェクト表示のうち、任意の複数を担当してよい。

アニメーションを描画するHelperが、同時に全体の速度や時間管理用Var/FVarを常駐管理してもよい。Controller専用Helperと描画専用Helperへ分離してもよい。

機能処理とアニメーション処理は、必ず同一Helperへまとめる必要はない。また、必ず分離する必要もない。演出の要件とHelper数、変数数、処理負荷に応じて構成を選択する。

技ごとの一時的なHelperは必要に応じて生成してよい。ただし、常駐Helperを過剰に増やすと処理負荷とHelper数制限に影響するため、常駐Helperは必要最小限にする。

## 常駐Helperのステート遷移

1. Rootが常駐Helperを生成する。
2. Helperの`StateDef -2`が共通ルーティングStateDefへ遷移させる。
3. 共通ルーティングStateDefがHelper IDに応じて専用StateDefへ振り分ける。
4. 専用StateDefがRootの状態や経過時間を監視し、必要に応じて個別挙動用StateDefへ遷移させる。
5. 個別挙動用StateDefで処理を実行する。
6. 次のフレームには`StateDef -2`から共通ルーティングへ戻り、専用StateDefへの振り分けを再開する。
7. 複数フレームにわたる挙動は、専用StateDefで進行状態を保持し、ルーティング後に継続して処理する。

## 個別挙動終了時の復帰

- 個別挙動用StateDefの処理完了時に、監視StateDefへ直接戻してはならない。
- 処理を終了状態にした後、次のフレームの`StateDef -2`から共通ルーティングを経由して監視StateDefへ復帰する。
- 監視StateDefへ直接復帰すると、発動条件が残ったまま再び個別挙動用StateDefへ遷移し、同じ遷移を繰り返す無限ループになって必ず起動時にクラッシュする。
