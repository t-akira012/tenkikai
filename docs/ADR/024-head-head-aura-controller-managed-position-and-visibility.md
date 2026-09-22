# ADR 024: HeadとHead Auraの位置・表示判断をControllerで管理する

## 状態

採用

## 背景

HeadにはRoot基準位置へ加える動作別の位置補正があり、Head Auraは完成したHead位置へ追従する。HeadがRootのStateNoを直接判定して位置補正パターンを選ぶ構成では、パターンが増えるたびに表示Helperへ個別動作の知識が追加される。

HeadとHead Auraおよび両者の残像を非表示にする条件も、RootのStateNoを各Helperが直接判定していた。この構成では、同じ演出条件が複数のHelperへ分散し、片方だけ条件が変更されると表示状態が分離する。

個別動作の選択は`the_controller`の責務であり、HeadとHead AuraはControllerが確定した値とフラグを適用する利用側に限定する必要がある。

## 決定

### 適用範囲

本ADRの対象はHeadとHead Auraの位置補正、HeadとHead Auraの非表示、および両者の残像非表示に限定する。Body、Body Aura、Root、将来追加される表示Helperへ本ADRの変数割当や実行順を適用しない。

### Head位置補正

RootのStateNo、アニメーション時間および動作条件を監視し、Headへ適用する位置補正パターンを選択する責務は`the_controller`に置く。Headは個別動作のStateNoや位置パターンを判定しない。

`the_controller`はHead完成Pos補正Xを`fvar(16)`、Head完成Pos補正Yを`fvar(17)`へ保持する。毎tick最初に両方を`0`へ戻し、該当する位置補正パターンがある場合だけ完成値を設定する。位置補正パターンが成立しない場合は`0,0`を完成値とする。

Head位置補正は、一つの位置補正ルーターとパターンごとの個別挙動StateDefで管理する。ルーターは一つのtickに該当するパターンを一つ、または0個選択する。各個別挙動は共通の`fvar(16)`と`fvar(17)`へ完成値を設定し、同じ次の挙動塊へ進む。異なる補間方法、時間条件または基準を持つパターンを一つの個別StateDefへ集約しない。

Headは毎tick、Root基準位置を設定した後、`fvar(16)`と`fvar(17)`を一つの`PosAdd`で無条件に適用して完成Posを確定する。Head Auraは位置補正値や位置パターンを参照せず、常駐Helperの存在順に従ってHeadの完成Posを直接参照する。

Head AuraのPosを意図的に非同期化する場合は、[ADR 023: HeadとHead Auraの変換同期と明示的な非同期制御](023-head-head-aura-transform-synchronization.md)に従い、対象固有の非同期フラグと完成値を別途追加する。

### Head系と残像の非表示

`the_controller`はHeadとHead Auraの完成表示状態を`var(22)`のビットフィールドへ保持する。

- bit 0：Head非表示
- bit 1：Head Aura非表示
- bit 2：Head残像非表示
- bit 3：Head Aura残像非表示

`var(22)`は毎tick最初に`0`へ戻し、RootのStateNoと演出条件に基づいて対象別ビットを設定する。HeadとHead AuraはRootのStateNoを直接判定せず、自身に割り当てられたビットだけを読む。

異形回避の回転中はHeadとHead Auraを表示し、残像も表示する。消失中だけHeadとHead Auraの非表示ビットおよび残像非表示ビットを有効にする。再出現時はすべての非表示ビットを解除する。

残像非表示ビットが有効な場合は、対象Helperが`AfterImageTime time=0`を適用して残像を非表示にする。無効な場合は通常のAfterImage表示を行う。Controllerは残像の停止・再開イベントを管理せず、各tickの完成表示状態として表示または非表示だけを指定する。

### Controllerと利用Helperの責務

`the_controller`は、個別動作のStateNo判定、位置補正パターンの選択、完成Pos補正値の計算、対象別の非表示状態の確定を担当する。

Headは、Root基準位置への完成Pos補正の適用と、自身および残像の表示処理だけを担当する。Head Auraは、Head完成Posの参照と、自身および残像の表示処理だけを担当する。HeadとHead Auraへ個別動作のStateNo判定、位置式、表示条件を追加しない。

## 結果

位置補正パターンが増えても、変更箇所は`the_controller`のルーターと個別挙動StateDefに限定される。Headは常に同じ完成Pos補正値を適用し、Head Auraは常に同じHead完成Posを参照する。

Head、Head Auraおよび両者の残像を非表示にする条件は、対象別の完成フラグとして一か所で確定される。
