# 005: ライフ管理方式

## 動作モデル

TENKIKAIは、原作作品における特殊な強者として、宇宙的で極めて頑強な肉体と非常に硬質な外殻を持つ。この外殻によって一般的な攻撃が通りにくい存在感を、Helper Armor式のライフ管理によって表現する。

AIRファイルでは、`the_controller`用Action以外から当たり判定をすべて除去する。本体と常に重なる`the_controller`だけが当たり判定を持ち、相手の攻撃を受ける。攻撃は`the_controller`へ命中するが、Helper Armorによって直接のライフ減少を無効化し、攻撃が持つDamage情報から本体へ反映する削り値を決定する。

通常Damageは、利用者が設定するダメージ減衰率と、現在Lifeに応じて連続変化する耐性によって減衰する。特定のLife以下で補正を切り替える閾値は設けない。Lifeが減るほど耐性が滑らかに強まり、残りLifeが少ないほど同じ攻撃から受ける削り値が小さくなる。

極大Damageは外殻の通常減衰を突破する。設定した閾値以上のDamageを受けた場合は、ダメージ減衰率とLife補正を適用せず、元のDamageを本体へ反映する。

自動回復量、ダメージ減衰率、被弾後無敵時間、極大Damage閾値は、利用者が`the_controller`の単一configから変更できる。自動回復量を`0`にすると回復を行わない。

`the_controller`は本体の外殻を代理するため、相手との位置衝突では相手を押し返す。攻撃のダメージを無効化することと、位置衝突を無効化することは別であり、相手が`the_controller`をすり抜ける状態は採用しない。

## ダメージ処理の流れ

1. 相手の攻撃が、本体へ追従する`the_controller`の当たり判定へ命中する。
2. `the_controller`は`HitOverride`によって直接のダメージを受けず、`GetHitVar(damage)`から元Damageを取得する。
3. 元Damageが極大Damage閾値以上なら、元Damageをそのまま削り値とする。
4. 通常Damageなら、ダメージ減衰率と現在Lifeによる連続補正を適用して削り値を決定する。
5. 決定した削り値を`the_controller`自身の保留ダメージ領域へ保存する。
6. 次のフレームに、本体が保留ダメージを読み取り、負の`LifeAdd`として自身へ反映する。
7. 本体が値を読み取ったフレームに、`the_controller`が保留ダメージを初期化する。

ダメージ保持値の初期化は、本体による読取りより前に行ってはならない。命中フレームで保存した値を次のフレームまで維持し、本体のライフ減算へ一度だけ使用してから解除する。

## 通常Damageの連続減衰

現在Lifeと最大Lifeの比率を`r`とする。

```text
r = 現在Life / 最大Life
```

Life補正には、最大Lifeで`1`、Lifeが減るほど`0`へ連続的に近づく二次式を使用する。

```text
Life補正 = 2r - r²
```

ダメージ減衰率configは`0`から`25`までの整数とし、1段階を元Damageの4%として倍率へ変換する。

```text
ダメージ減衰率 = ダメージ減衰率config / 25
```

通常Damageの削り値は次の式で決定する。

```text
削り値 = floor(GetHitVar(damage) * ダメージ減衰率 * (2r - r²))
```

元Damageとダメージ減衰率がともに正であり、計算結果が`0`となった場合の最低削り値は`1`とする。ダメージ減衰率configが`0`の場合は削り値も`0`とする。

## 極大Damage

極大Damage閾値configは、1段階を100Damageとして閾値へ変換する。

```text
極大Damage閾値 = 極大Damage閾値config * 100
```

configが`1`以上で、元Damageが閾値以上の場合は極大Damageとする。極大Damageにはダメージ減衰率とLife補正を適用しない。configが`0`の場合は極大Damage判定を無効とする。

## ダメージ受付間隔

`the_controller`は無敵期間用Varを持つ。ダメージを受け付けたとき、configで指定された固定無敵時間を設定する。設定後は1tickごとに値を1ずつ減らし、`0`になった時点で次のダメージを受け付ける。

無敵期間用Varが`0`より大きい間は、新たな攻撃が`the_controller`へ接触しても、そのDamageを保留ダメージへ保存せず、本体Lifeへ反映しない。無敵期間は絶対時刻との比較ではなく、残り時間を減算するタイムカウント方式で管理する。

## 自動回復

自動回復量configが`1`以上の場合は、本体が生存中、最大Life未満、かつそのtickに保留ダメージがないとき、設定量を本体Lifeへ加算する。回復上限は最大Lifeとする。configが`0`の場合は自動回復を行わない。

常駐Helperへ適用する自動最大Life維持は、本体の自動回復とは異なる。常駐Helperが攻撃受付やルーティングを継続するための基盤処理として維持する。

## 当たり判定と追従

AIRファイル内の全Actionから当たり判定を除去し、`the_controller`用Actionだけに当たり判定を設定する。`the_controller`には、Helper IDと同じ番号のActionを用意し、そのActionへ旧`Begin Action 0`と同一の当たり判定を設定する。

`the_controller`は本体の位置、向き、および当たり判定の基準となる表示状態へ常に追従する。Helperがオーラバウンド用の個別StateDefへ遷移している間も追従とHelper Armorを停止させず、相手から見た攻撃対象を常に本体の位置へ維持する。

## `the_controller`の複数処理

`the_controller`は、Helper Armor式ライフ管理とオーラバウンドを同居させる常駐Helperである。`the_controller`のIDは`99004`とし、ライフ管理を別Helperへ分離しない。

```text
the_controller
  ├─ Helper Armor config
  ├─ 常時処理
  │    ├─ 本体への追従
  │    ├─ HitOverrideの維持
  │    ├─ ダメージ情報の保持と解除
  │    └─ 無敵期間のカウントダウン
  ├─ ライフ管理
  │    ├─ 通常Damageの連続減衰
  │    ├─ 極大Damageの減衰迂回
  │    └─ 本体への削り値と任意の自動回復の反映
  └─ オーラバウンド
       ├─ 技ごとのバウンド定義
       └─ バウンドの共通消費と進行
```

常時性が必要な追従、攻撃受付、ダメージ転送、無敵期間管理は、オーラバウンドの演出処理によって中断されないようにする。

## 実装方式

Helper Armorの攻撃受付、削り値計算、ダメージ保持および無敵期間は、`the_controller`の個別StateDefで管理する。configの設定Controllerは、特例としてStateDef `-2`先頭のAI設定欄へ置き、`IsHelper(99004)`で`the_controller`だけを対象とする。RootのStateDef `-2`処理は、`the_controller`が決定した保留ダメージの減算と、configで有効化された自動回復を実行する。

configは最初のControllerで`var(12)`を`0`へ初期化し、自動回復量、ダメージ減衰率、被弾後無敵時間、極大Damage閾値を独立したControllerからビットORで設定する。各項目は他の項目の設定式と混在させない。

Helper Armorの実行状態は`var(11)`、利用者設定は`var(12)`へ分離する。各bit割当は[the_controller変数一覧](../state/var-list-helper-99004.md)を正本とする。

## 確定済み設計条件

### Helper Armor

- 攻撃受付対象：`the_controller`
- Helper ID：`99004`
- 防御方式：`HitOverride`
- 元Damage取得：`GetHitVar(damage)`
- 本体への反映：次のフレームに負の`LifeAdd`
- ダメージ保持値の解除：本体が読み取ったフレームに初期化
- 通常Damage：ダメージ減衰率とLife比率の二次曲線で減衰
- 極大Damage：設定閾値以上では減衰しない

### 当たり判定

- AIRファイル：`the_controller`用Action以外の当たり判定をすべて除去
- `the_controller`のAction番号：Helper IDと同じ`99004`
- `the_controller`の当たり判定：旧`Begin Action 0`と同一
- `the_controller`の位置衝突：有効。相手を押し返す
- 追従対象：本体

## 現在の設定値

### Helper Armor config

- 自動回復量：`0/tick`。自動回復なし
- ダメージ減衰率config：`4`。Life補正前は元Damageの`16%`とする試験値
- 被弾後無敵時間：`30tick`の試験値
- 極大Damage閾値config：`30`
- 極大Damage閾値：`3000Damage`

### 保持値

- 保留ダメージ上限：`65535`
- 無敵時間上限：`127tick`
- 自動回復量上限：`127/tick`
- ダメージ減衰率config上限：`25`
- 極大Damage閾値config上限：`32`
