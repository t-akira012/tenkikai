# ADR 020: AngleDraw値と適用対象のController管理

## 状態

採用

## 背景

`AngleDraw`が変更する角度と倍率は、適用したHelper自身の描画へだけ作用する。ある表示Helperの位置へ別の表示Helperを追従させても、角度と倍率は追従先へ伝播しない。

Bodyと複数の表示Helperを同期して描画するために、各対象へ同じ計算式を記述すると、式と条件が重複する。調整時に一部だけが変更されると表示が分離するため、計算と適用対象を一元管理する必要がある。

一方、Head AuraとBody Auraには、`the_controller`のAura Boundフラグ`var(0)`と拡張量`fvar(0)`を使用する既存のAngleDrawがある。共有AngleDrawがAura Boundを上書きすると表示を破壊するため、同一tickで成立する場合の優先順位も共通契約に含める必要がある。

## 決定

### Head・Body共通

Bodyと複数の表示Helperで共有する`AngleDraw`値は、`the_controller`が計算して保持する。利用側は計算式を複製せず、対象固有の同期フラグが有効な場合だけControllerの完成値を読む。

AngleDrawの値生成、適用対象、優先制御を管理する基盤は、常に`the_controller`とする。個別StateDefへAngleDrawの値生成や適用条件を記述してはならず、例外を設けない。Root自身へState Controllerを作用させる適用口だけはRootのStateDef `-2`へ置き、`the_controller`の完成値をそのまま使用する。表示Helperも同様に完成値を読むだけとする。

`the_controller`は毎tick、最初に適用フラグを`0`へ戻す。適用条件が成立した場合は、角度、X倍率、Y倍率の順に完成値を保存し、その後で対象の適用フラグを`1`にする。値より先に適用フラグを有効にしてはならない。

Aura Boundと同期AngleDrawが同一tickで成立する場合は、Head系とBody系のどちらでもAura Boundを優先する。`the_controller`のAura Boundフラグ`var(0)`が有効な場合、Head AuraとBody Auraへ同期AngleDrawを適用してはならない。したがって、Aura Bound中はHeadとHead Aura、BodyとBody Auraが意図的に非同期となる。

今後、別の表示Helperを同じAngleDrawへ同期する場合は、`the_controller`へ対象固有の適用フラグを追加する。利用Helperへ共有計算式を複製してはならない。

### Head

`the_controller`の`fvar(2)`を共有角度、`fvar(3)`をHead X倍率、`fvar(4)`をHead Y倍率とする。`var(17)`をHeadへの適用フラグ、`var(18)`をHead Auraへの適用フラグとする。

HeadとHead Auraは角度と倍率を計算しない。対応する適用フラグが`1`の場合だけ、`the_controller`が保持する完成値を自身の`AngleDraw`へそのまま設定する。利用Helper側で追加の倍率補正を行わない。Head AuraはAura Boundフラグが無効な場合に限って同期値を適用する。

### Body

Body系の完成角度を`the_controller`の`fvar(7)`、X倍率を`fvar(5)`、Y倍率を`fvar(6)`、完成Y Offsetを`fvar(8)`へ保持し、Body適用フラグを`var(19)`、Body Aura適用フラグを`var(20)`とする。Body系はHead用角度`fvar(2)`を使用しない。

Bodyの縮小はアニメーション要素5の開始時点から行う。要素数や各要素の表示時間を固定せず、`AnimeElemTime(5)`と`AnimTime`から要素5以降の進捗率を求める。進捗率0では倍率1、終了時には倍率0.05とし、余弦曲線によって後半ほど縮小速度を上げる。X倍率とY倍率には同じ完成値を設定する。

Scaleの中心となるSprite axisがBody中心より下にあるため、縮小時はBody中心が下方向へ移動する。異形回避では通常の浮遊Offsetへ`-48*(1-Y倍率)`を加えた値を完成Y Offsetとし、BodyとBody Auraへ同じ値を適用する。倍率1では補正を行わず、倍率0.05では上方向へ45.6px補正する。

BodyはRootのStateDef `-2`にある共通適用口で、`var(19)`が`1`の場合だけ`fvar(7)`、`fvar(5)`、`fvar(6)`を使用する。Body AuraはAura Boundフラグが無効で、かつ`var(20)`が`1`の場合だけ同じ完成値を使用する。

現在の異形回避ではBody系完成角度を`0`とし、Scaleだけを変化させる。Body系の角度同期能力は汎用基盤として保持し、今後Body AngleDrawを必要とする挙動も個別StateDefへ実装せず、`the_controller`が同じ完成値と適用フラグを設定する。

具体的なX位置、Trans、アニメーション同期は本ADRの対象としない。

## 結果

AngleDrawの計算式は`the_controller`だけが保持し、Head、Head Aura、Body、Body Auraは対象ごとの完成値を使用する。角度または倍率を調整する際に、複数箇所の式を個別に同期する必要がなくなる。

適用対象は個別フラグで制御されるため、同じ共有値を保持しながら、表示HelperごとにAngleDrawの有効・無効を選択できる。

既存のAura Boundは共有AngleDrawより優先されるため、Bound表示を維持できる。ただしAura Bound中は同期対象同士が意図的に非同期となる。
