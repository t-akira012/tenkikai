# ADR 025: AngleDraw演出の要求bitと持続カウンター管理

## 状態

採用

## 背景

Body、Head、Body Aura、Head AuraのAngleDraw演出をRootのStateNoへ直接結び付けると、Rootが別のStateDefへ移った時点で変形が終了する。異形回避の再出現後に操作を再開しながら変形だけを継続する演出や、手入力によってStateDefが細かく変動する前後ダッシュでは、Rootの行動可能期間と表示変形の持続期間を同一にできない。

また、再出現のScale変形中に前後ダッシュの角度変形が始まる場合がある。演出種別を一つの値で排他的に管理すると、一方の変形が他方を不要に上書きするため、角度、X倍率、Y倍率へ複数の要求を合成できる管理方式が必要となる。

## 決定

### StateNoの責務

RootのStateNoはAngleDraw演出の開始または更新要求を検出するためだけに使用する。AngleDraw完成値の継続条件へRootのStateNoを直接使用しない。

演出開始時に`the_controller`へ要求bitと持続カウンターを設定する。以後はRootが別のStateDefへ移っても、カウンターが残っている間は要求bitを有効にし、カウンターの進行率からAngleDraw完成値を計算する。

### 要求bit

`the_controller`の`var(2)`をAngleDraw演出要求bitとして使用する。

| bit | マスク | 要求 |
| ---: | ---: | --- |
| 0 | `1` | 異形回避中のHead回転・縮小 |
| 1 | `2` | 異形回避中のBody縮小 |
| 2 | `4` | 前方ダッシュのBody傾斜 |
| 3 | `8` | 後方ダッシュのBody傾斜 |
| 4 | `16` | 異形回避再出現後の全身縦長復元 |
| 5 | `32` | 前方短距離ワープのBody変形 |

要求bitは毎tick、対応する持続カウンターから再構成する。複数の要求bitを同時に有効にできる。完成角度とX・Y倍率はプロパティごとに合成し、一つの演出を選ぶための排他的な種別値として扱わない。

### 持続カウンター

異形回避のHead回転・縮小はStateDef `300`への進入時に、Controllerが保持したRootアニメーション残り時間を全体時間と残り時間へ保存する。Body縮小はAction `300`の要素5開始時に、その時点のアニメーション残り時間を保存する。RootがStateDef `300`を離れても、保存した残り時間が0になるまで変形を継続する。

前方短距離ワープはStateDef `100`への進入時に、Controllerが保持したRootアニメーション残り時間を全体時間と残り時間へ保存する。既存の要素進行に対応する二段階のBody変形をカウンター経過時間へ置き換え、StateNoを完成値の継続条件にしない。

前方ダッシュと後方ダッシュは、RootがStateDef `110`または`111`にいる各tickで対応するカウンターを1tickへ更新する。これは手入力による細かなStateDef変動へ追従する1tickのリースとする。該当StateDefを離れると更新を停止し、最後のリース終了後に通常角度へ戻す。

異形回避の再出現はStateDef `302`への進入を開始信号とし、Helperが確実に観測できる`root,time=1`で固定16tickのカウンターを設定する。StateDef `302`は2frameで終了し、Rootは操作可能な別StateDefへ移る。全身の縦長復元だけをStateNoと無関係に16tick継続する。

### 完成値と適用対象

要求bitと持続カウンターからAngleDraw完成値を生成する責務は`the_controller`に置く。Body、Head、Body Aura、Head AuraはRootのStateNoや持続カウンターを参照せず、[ADR 020](020-controller-angledraw-sharing.md)で割り当てられた完成値と適用フラグだけを使用する。

再出現後の縦長復元はBody、Head、Body Aura、Head Auraへ同じ進行率を適用する。前後ダッシュの要求と同時に成立した場合は、ダッシュ由来の角度と再出現由来のX・Y倍率を合成する。

Aura Boundは要求bitと持続カウンターへ含めず、従来どおり独立して管理する。Aura Boundと共有AngleDrawが同時に成立する場合の優先関係はADR 020に従う。

## 結果

Rootの操作可能期間とAngleDraw演出の持続期間を分離できる。StateDef `302`の2frame経過後も再出現変形を継続でき、変形中は移動、攻撃、被弾を含む通常のStateDef遷移を妨げない。

前後ダッシュは1tickリースによって入力方向の変化へ追従し、再出現Scaleとダッシュ角度はプロパティ単位で共存する。StateNo固有の条件と進行式は表示要素へ分散せず、`the_controller`へ集約される。
