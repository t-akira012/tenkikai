# ADR 030: the_controllerによるRoot画面外移動許可

## 状態

採用

## 背景

TENKIKAIの表示は、Rootが担当する本体と、常駐描画Helperが担当するBody Aura、Head、Head Auraから構成される。常駐描画Helperは[ADR 009](009-resident-helper-screenbound.md)により常時画面外移動を許可しているが、Rootの画面外移動許可を技StateDefへ個別に記述すると、許可条件が全身表示の管理責務から分離する。

画面外へ移動する技では、Rootだけが画面端へ拘束される状態を避け、常駐描画Helperとともにキャラクター全体を画面外へ移動できる必要がある。

## 決定

Rootの画面外移動許可条件は`the_controller`がboolean完成値として管理する。`the_controller`の`var(8)`を使用し、`0`を通常の画面内拘束、`1`を画面外移動許可とする。

`the_controller`は毎処理周期の先頭で`var(8)`を`0`へ初期化し、Rootが画面横断突進のStateDef `1200`〜`1204`にいる場合だけ`1`へ設定する。技StateDefは`ScreenBound`を直接実行しない。

RootはStateDef `-2`の共通適用口で、Controllerが完成させたbooleanを次のように適用する。

- `var(8)=0`：`ScreenBound value=1`、カメラ移動許可
- `var(8)=1`：`ScreenBound value=0`、カメラ移動不許可

常駐描画HelperはADR 009の契約を維持し、常時`ScreenBound value=0`とする。Rootのbooleanが`1`の間は、本体、Body Aura、Head、Head Auraの全表示要素が画面外へ移動できる。常駐描画Helperへ技StateDef判定または同じboolean判定を複製しない。

RootはHelperより先に処理されるため、StateDef `-2`は`the_controller`が前tickに完成させたbooleanを使用する。Rootが対象StateDefへ入った次のtickから画面外移動を許可する。

## 結果

画面外移動を使用する技は、Controllerの許可条件へ対象StateDefを登録するだけでRootの共通適用口を利用できる。技StateDefへ`ScreenBound`を重複させず、Rootと常駐描画Helperが分離して画面端へ残る状態を防ぐ。
