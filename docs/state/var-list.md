# 変数一覧

この文書は、TENKIKAIの定義ファイルで使用している通常変数とシステム変数を列挙する。変数番号ごとの意味は、CNSでの代入と参照の用途に基づいて記載する。

## 通常変数

### `var(0)` — `private-gametime`

| 項目 | 定義 |
| --- | --- |
| 定義ファイル | `cns/observ.cns` |
| 使用コンテキスト | StateDef `-2`、`-3` |
| 用途 | キャラクター固有の経過tickと `AfterImage` の初回生成を制御 |
| 設定値 | StateDef `-2` で初期化後、毎tick `1` 加算 |

本体のStateDef `-2` で管理し、`gametime` と同期して進める。周期運動と定期演出の時間基準として使用し、頭部ヘルパーからは本体の値を参照する。

### `var(1)` — `private-time`

| 項目 | 定義 |
| --- | --- |
| 定義ファイル | `cns/observ.cns` |
| 使用コンテキスト | StateDef `-2` |
| 用途 | 現在Stateの経過tickを保持する `time` 代用品 |
| 設定値 | StateDef開始時に `0`、毎tick `1` 加算 |

本体のStateDef `-2` で `time=0` のときに初期化する。StateDefが変更されると再び `0` から加算される。

### `var(2)` — 入力ビットフィールド

| 項目 | 定義 |
| --- | --- |
| 定義ファイル | `cns/observ.cns`、`cns/command.cmd` |
| 使用コンテキスト | StateDef `-2`、`-1`、入力を参照する各StateDef |
| 用途 | ビット31の自動運用フラグと、通常操作・オートメーションが共有する下位入力状態 |
| 設定値 | StateDef `-2`で自動運用フラグを設定し、StateDef `-1`でビット31を維持して下位ビットを解除後、成立した入力ビットをOR演算で設定 |

StateDef `-2`の最上部でビット31を自動運用フラグとして設定する。StateDef `-1`では、このフラグを維持したまま下位ビットを毎tick解除し、通常操作時だけCommandを下位ビットへ変換する。後続の状態遷移、移動、アニメーション、StateDef `-3`の浮遊移動と状態変更は、対応する入力ビットを参照する。下位ビットの正規定義は[Command入力ビットマップ](../AGENTS.input-map.md)、ビット31の規約は[オートメーション規約](../AGENTS.automation.md)を参照する。

### `var(6)` — 異形回避の出現領域

StateDef `300`で追加入力を記録する。`0`は未選択、`1`〜`3`は下段の左・中央・右、`4`〜`6`は上段の左・中央・右を表す。StateDef `301`はこの値を参照して出現位置へ移動する。`0`の場合は相手の向きに対して25px背後へ移動し、画面外になる場合は反対側の画面端から20px内側へ回り込む。

### `var(7)` — 異形回避の追加入力受付

StateDef `300`へ入った直後は`0`とし、開始入力の`X+Y`を解除した後に`1`へ変更する。`1`の間だけ次のボタン入力を出現領域として受け付け、入力成立後は`0`へ戻す。

### `var(10)`

| 項目 | 定義 |
| --- | --- |
| 定義ファイル | `cns/observ.cns` |
| 使用コンテキスト | StateDef `-3` |
| 用途 | `AfterImage` の初回生成を制御するフラグ |
| 設定値 | `1` |

本体または頭部ヘルパーで未設定のときに `1` を代入し、同じ実行条件での初回生成後に再生成しないようにする。

### `var(11)` — Helper Armorダメージ保持

| 項目 | 定義 |
| --- | --- |
| 定義ファイル | `cns/helper.cns`、`cns/observ.cns` |
| 使用コンテキスト | ID `99004`の`the_controller`、本体のStateDef `-2` |
| 用途 | `GetHitVar(damage)`から取得したダメージを次のフレームまで保持 |
| 設定値 | ダメージ受付時に正のダメージ値、本体の読取り後に`0` |

`the_controller`が無敵期間外で攻撃を受けた場合に設定する。本体はHelperリダイレクトで値を読み取り、低ライフ時の減衰後に負の`LifeAdd`として適用する。

### `var(12)` — Helper Armor無敵期間

| 項目 | 定義 |
| --- | --- |
| 定義ファイル | `cns/helper.cns`、`cns/observ.cns` |
| 使用コンテキスト | ID `99004`の`the_controller` |
| 用途 | 次のダメージを受け付けるまでの残りtick数 |
| 設定値 | ダメージ受付時に`GetHitVar(damage)`、以後毎tick`1`減算 |

値が`0`のときだけ新しいダメージを`var(11)`へ保存する。`var(11)`と`var(12)`は`the_controller`専用であり、同じ番号のRoot変数とは別の変数領域である。

### `var(13)` — PlayerPush無効化フラグ

| 項目 | 定義 |
| --- | --- |
| 定義ファイル | `cns/helper.cns` |
| 使用コンテキスト | ID `99004`の`the_controller` |
| 用途 | Helper ArmorのPlayerPushを一時的に無効化 |
| 設定値 | 通常時は`0`、RootがStateDef `110`、`111`、または`300`〜`302`の場合は`1` |

`the_controller`がライフ管理へ移る前にRootのStateNoを監視して毎tick設定する。`1`の場合はPlayerPushを無効にし、前後ダッシュまたは異形回避中のすり抜けを許可する。

### `var(14)` — 無敵フラグ

| 項目 | 定義 |
| --- | --- |
| 定義ファイル | `cns/helper.cns` |
| 使用コンテキスト | ID `99004`の`the_controller` |
| 用途 | Helper Armorの攻撃受付を一時的に無効化 |
| 設定値 | 通常時は`0`、Rootが前後短距離ワープまたは異形回避中の場合は`1` |

`the_controller`がライフ管理へ移る前にRootのStateNoを監視して毎tick設定する。`1`の場合は`NotHitBy`を適用する。現在の対象は前方短距離ワープStateDef `100`〜`102`、後方短距離ワープStateDef `105`〜`107`、異形回避StateDef `300`〜`302`である。

### `var(15)` — Controller保存済みRootアニメーション番号

ID `99004`の`the_controller`が、`var(16)`と対になるRootアニメーション番号を保持する。Rootのアニメーション変更を検出した場合は、先に`var(16)`を更新してから`var(15)`へ`root,anim`を保存する。利用Helperは現在のRootアニメーションとの一致を確認してから`var(16)`を使用する。

### `var(16)` — Controller保存済みRootアニメーション時間

ID `99004`の`the_controller`が、Rootアニメーション変更時の`abs(root,animtime)`を保持する。Rootアニメーションの要素数や各要素の表示時間を固定値として利用Helperへ重複させず、アニメーション全体時間を必要とする処理へ提供する。固定的な契約は[Rootアニメーション時間保持規約](../AGENTS.root-animtime.md)に従う。

### `var(17)` — Controller Head AngleDraw適用フラグ

ID `99004`の`the_controller`が毎tick`0`へ戻し、共有AngleDraw値をHeadへ適用する場合だけ、値の更新後に`1`を設定する。Headは`1`の場合だけControllerの`fvar(2)`〜`fvar(4)`を使用する。

### `var(18)` — Controller Head Aura AngleDraw適用フラグ

ID `99004`の`the_controller`が毎tick`0`へ戻し、共有AngleDraw値をHead Auraへ適用する場合だけ、値の更新後に`1`を設定する。Head Auraは`1`の場合だけControllerの`fvar(2)`〜`fvar(4)`を使用する。

### `var(19)` — Controller Body AngleDraw適用フラグ

ID `99004`の`the_controller`が毎tick`0`へ戻し、Body系完成AngleDrawをBodyへ適用する場合だけ、値の更新後に`1`を設定する。RootのStateDef `-2`は本フラグが`1`の場合だけControllerの`fvar(7)`、`fvar(5)`、`fvar(6)`を使用する。

### `var(20)` — Controller Body Aura AngleDraw適用フラグ

ID `99004`の`the_controller`が毎tick`0`へ戻し、Body系完成AngleDrawをBody Auraへ適用する場合だけ、値の更新後に`1`を設定する。Body AuraはAura Boundフラグ`var(0)`が無効で、かつ本フラグが`1`の場合だけControllerの`fvar(7)`、`fvar(5)`、`fvar(6)`を使用する。

### `var(21)` — Controller暗転ビットフィールド

ID `99004`の`the_controller`が、`AllPalFX`暗転の番号と残り時間を保持する。bit 0〜15は0〜65535tickの残り時間、bit 16〜20は0〜31の暗転番号とし、bit 21〜31は使用しない。残り時間が正の場合は毎tick`1`減算し、0になった場合は値全体を0へ戻す。現在はRootのStateDef `1000`、`private-time=10`で暗転番号0と60tickを保存する。

## 浮動小数点変数

### `fvar(0)` — 浮遊表示位相

| 項目 | 定義 |
| --- | --- |
| 定義ファイル | `cns/observ.cns` |
| 使用コンテキスト | StateDef `-2`、`-3` |
| 用途 | 浮遊感表示の正規化位相 |
| 設定値 | `-1`から`1`までを往復 |

本体が保持する位相を頭部ヘルパーがRoot参照で利用する。本体と頭部ヘルパーの浮遊感表示は同じ位相で同期する。

### `fvar(2)` — Controller共有AngleDraw角度

ID `99004`の`the_controller`が、複数表示Helperへ適用するAngleDrawの完成角度を保持する。利用Helperは対応する適用フラグが有効な場合だけ参照する。

### `fvar(3)` — Controller共有AngleDraw X倍率

ID `99004`の`the_controller`が、複数表示Helperへ適用するAngleDrawの完成X倍率を保持する。

### `fvar(4)` — Controller共有AngleDraw Y倍率

ID `99004`の`the_controller`が、複数表示Helperへ適用するAngleDrawの完成Y倍率を保持する。

### `fvar(5)` — Controller Body AngleDraw X倍率

ID `99004`の`the_controller`がBodyへ適用する完成X倍率を保持する。Rootのアニメーション要素5以降、余弦曲線によって1から0.05まで縮小する。

### `fvar(6)` — Controller Body AngleDraw Y倍率

ID `99004`の`the_controller`がBodyへ適用する完成Y倍率を保持する。X倍率と同じ完成値を使用する。

### `fvar(7)` — Controller Body AngleDraw角度

ID `99004`の`the_controller`がBodyとBody Auraへ適用する完成角度を保持する。Head系の`fvar(2)`とは独立し、異形回避では`0`を設定する。

### `fvar(8)` — Controller Body完成Y Offset

ID `99004`の`the_controller`がBodyとBody Auraへ適用する完成Y Offsetを保持する。異形回避では通常の浮遊Offsetへ`-48*(1-fvar(6))`を加え、Scale縮小によってBody中心がSprite axisへ近づく移動を上方向へ補正する。

## システム変数

### `sysvar(0)`

| 項目 | 定義 |
| --- | --- |
| 定義ファイル | `cns/common1.cns` |
| 使用StateDef | `132`、`155`、`5081`、`5110` |
| 用途1 | 着地判定の一時フラグ |
| 用途2 | StateDef `5081` からの落下処理完了フラグ |
| 設定値 | 条件成立時に `1`、StateDef `5110` の処理開始時に `0` |

StateDef `132` と `155` では、`pos y>=0` かつ `vel y>0` を設定し、接地時の速度・位置補正と遷移に使用する。StateDef `5081` ではヒット処理後に `1` を設定し、StateDef `5110` で落下処理の分岐と遷移条件に使用する。

### `sysvar(1)`

| 項目 | 定義 |
| --- | --- |
| 定義ファイル | `cns/common1.cns` |
| 使用StateDef | `5100`、`5110` |
| 用途 | 落下開始時のY速度を整数化して保持 |
| 設定値 | `floor(vel y)` |

保持した値を、落下時の `GameMakeAnim` の種類、効果音の番号、接地エフェクトの `under` 判定に使用する。StateDef `5110` では、落下Y速度がある場合に更新する。

### `sysvar(2)`

| 項目 | 定義 |
| --- | --- |
| 定義ファイル | `cns/common1.cns` |
| 使用StateDef | `5080` |
| 用途 | ヒット時に使用するアニメーション番号の選択 |
| 初期値 | `GetHitVar(yvel)=0` のとき `5080`、それ以外は `5090` |

現在のアニメーション番号末尾を加算して対応するアニメーションを選択する。選択したアニメーションが存在しない場合は `5030` にフォールバックする。

## 集計

通常変数は`var(0)`、`var(1)`、`var(2)`、`var(6)`、`var(7)`、`var(10)`〜`var(21)`の17種類、浮動小数点変数は`fvar(0)`、`fvar(2)`〜`fvar(8)`の8種類、システム変数は`sysvar(0)`、`sysvar(1)`、`sysvar(2)`の3種類を使用している。`sysfvar`は使用していない。
