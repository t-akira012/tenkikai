# ADR 023: HeadとHead Auraの変換同期と明示的な非同期制御

## 状態

採用

## 背景

Head AuraはHeadへ重ねて表示するため、Headの位置、描画Offset、AngleDrawの角度および倍率へ追従する必要がある。HeadとHead AuraがRootのStateDefを個別に判定して値を再計算すると、条件、式、State Controllerの実行順に差が生じ、一部の変換だけが同期から外れる。

PosとOffsetを合算した最終表示位置だけを一致させる方法では、実座標であるPosと描画補正であるOffsetの役割が混在する。表示上は一時的に重なっても、HeadとHead AuraのPosおよびOffset自体は一致しない。また、同一tickに通常値と同期値のState Controllerを重ねて後段の上書きへ依存すると、どの値が完成値であるかがHead Aura側へ分散する。

Head Auraへ意図的にHeadと異なる変換を与える演出もある。これを特定StateDefの例外処理としてHead Auraへ追加すると、追従機構そのものが動作ごとに分岐するため、Head系の非同期化を明示的に管理する必要がある。

## 決定

### Head系共通原則

HeadとHead AuraのPos、Offset、AngleDrawは、それぞれ独立した値として同期する。複数の値を合算した表示結果だけを一致させる方法を同期とは扱わない。

Head AuraはHeadとの同期を標準動作とする。Head Auraへ意図的に異なる値を与える場合は、対象プロパティに対応する非同期フラグを`the_controller`が明示的に設定する。Posの非同期、Offsetの非同期、AngleDrawの非同期を別々に扱い、あるプロパティの非同期を別のプロパティへ暗黙に波及させない。

RootのStateDef、演出条件、優先順位を監視してHead Auraの非同期フラグを決定する責務は`the_controller`に置く。HeadとHead AuraはRootのStateDefを直接判定して同期方法を変更してはならない。個別動作が非同期を必要とする場合も、HeadまたはHead AuraへStateDef固有の同期分岐を追加せず、`the_controller`が非同期フラグと対象別完成値を設定する。

### Pos

`the_controller`は動作別のHead完成Pos補正を確定する。HeadはRoot基準位置へControllerの完成Pos補正を適用し、完成Posを確定する。後続のHead Auraは、常駐Helperの存在順に従ってHeadの完成Posを直接参照し、X座標とY座標を同じ値へ設定する。Headの位置計算をHead Auraへ複製しない。位置補正パターンと表示状態の管理は[ADR 024: HeadとHead Auraの位置・表示判断をControllerで管理する](024-head-head-aura-controller-managed-position-and-visibility.md)に従う。

Head AuraのPosを非同期にする演出を追加する場合は、`the_controller`へHead Aura Pos非同期フラグと非同期時の完成値を追加する。非同期要求がない状態で、Head AuraにRoot基準の代替位置やStateDef固有の位置経路を設けない。

### Offset

`the_controller`は、Head完成OffsetとHead Aura完成Offsetを保持する。同期時はHead Aura完成OffsetへHead完成Offsetと同じX値およびY値を設定する。非同期時だけ、Head Aura Offset非同期フラグに基づいてHead Aura用の別の完成Offsetを設定する。

HeadとHead Auraは、自身に割り当てられた完成Offsetを一つの`Offset`で適用する。HeadまたはHead AuraへOffset式を複製せず、同一tickに通常Offsetと同期Offsetを重ねて上書き順へ依存しない。

### AngleDraw

`the_controller`は、Head完成角度・X倍率・Y倍率と、Head Aura完成角度・X倍率・Y倍率を保持する。同期時はHead Aura完成AngleDrawへHead完成AngleDrawと同じ値を設定する。非同期時だけ、Head Aura AngleDraw非同期フラグに基づいてHead Aura用の別の完成値を設定する。

HeadとHead Auraは、自身に割り当てられた完成AngleDrawを一つの`AngleDraw`で適用する。同一tickに通常AngleDrawと同期AngleDrawを重ねず、HeadまたはHead Aura側で優先順位を決定しない。AngleDraw値のController管理に関する既存方針は[ADR 020: AngleDraw値と適用対象のController管理](020-controller-angledraw-sharing.md)に従い、本ADRはHeadとHead Auraの対象別完成値と明示的な非同期制御を追加の契約とする。

### 非同期の終了

`the_controller`はHead Auraの非同期フラグを毎tick既定値へ戻し、成立中の演出条件に対応するフラグだけを設定する。非同期条件が終了したtickから、Head Auraの完成値をHeadと同じ値へ戻す。Head Auraは前tickの非同期値を保持しない。

### 適用範囲

本ADRの対象はHeadとHead Auraの関係に限定する。BodyとBody Aura、RootとBody Aura、将来追加される表示Helperへ本ADRのPos確定順、完成値、非同期フラグを適用しない。それらの表示要素を同期または非同期化する場合は、対象固有の実行順と要件に基づいて別途決定する。

## 結果

同期時はHeadとHead AuraのPos、Offset、AngleDrawが個別に一致し、表示結果だけを合わせる隠れた補正がなくなる。Head Auraの非同期演出はプロパティ単位の明示的なフラグと対象別完成値として管理され、個別StateDefやHead Auraへ同期方法が分散しない。

HeadとHead Auraが適用する各State Controllerは一つの完成値だけを使用するため、同一tick内の上書き順に依存せず、Head系の同期と非同期の責任境界が明確になる。
