# the_controller Helper

## StateDef 99004000: the_controller集約

ID `99004`の常駐Helper。Rootの状態を監視し、ライフ管理、Helper Armor、Root画面外移動許可、オーラバウンド、部位変換、表示制御、暗転を一つの処理列で管理する。

### 毎tickの処理順

```text
99004000 集約・完成値初期化
  → 99004001 / 99004010 ライフ管理・Helper Armor
  → 99004002 / 99004011〜99004014 オーラバウンド
  → 99004006 / 99004030 AngleDraw要求・持続カウンター・完成値
  → 99004005 / 99004021〜99004022 Head位置補正
  → 99004007 / 99004040〜99004041 Head眼球表示
  → 99004004 / 99004020 Head・Head Aura変換完成
  → 99004003 / 99004100 全画面色変更
  → 99004999 最終処理
  → 5150
```

各ルーターは該当する個別StateDefを0個または1個実行し、必ず次の機能へ進む。詳細な追加規則は[ADR 015](../ADR/015-the-controller-99004-routing.md)に従う。

### 機能

| StateDef | 機能 |
| --- | --- |
| `99004000` | Root画面外移動許可boolean、Rootアニメーション時間の保持、暗転時間の更新、Head系AngleDraw・位置・表示の初期化、Body系適用フラグ、PlayerPush無効化、無敵を管理する |
| `99004001`、`99004010` | Rootへ追従するHelper ArmorとしてPlayerPush、攻撃受付、通常Damageの連続減衰、極大Damageの減衰迂回、保留ダメージと無敵期間を管理する |
| `99004002`、`99004011`〜`99004014` | RootのStateDef `4001`〜`4003`および`1100`に対応するオーラバウンドを開始し、拡大進行と残量消費を管理する。`1100`は40tickで`0.38`まで拡大後、`0.075/tick`で縮小する |
| `99004006`、`99004030` | StateDef進入からAngleDraw要求を開始し、要求bit、持続カウンター、自由傾斜の目標角度・角速度・現在角度、Body・Head系完成値を管理する |
| `99004005`、`99004021`〜`99004022` | 異形回避または本体自由傾斜に対応するHead位置補正を完成値へ設定する |
| `99004007`、`99004040`〜`99004041` | 通常時の距離同期または前後ダッシュの固定指定からHead眼球の完成表示bitを設定する |
| `99004004`、`99004020` | HeadのOffsetとAngleDrawをHead Auraへ同期し、通常AuraまたはAura Bound時だけ対象別の完成値へ分岐する |
| `99004003`、`99004100`、`99004190` | 暗転ビットフィールドを読み、全画面黒の乗算値を設定して`AllPalFX`を適用する |
| `99004999` | 処理列を終了してStateDef `5150`へ戻す |

### Helper Armor configとダメージ計算

StateDef `-2`先頭のAI設定欄は、`IsHelper(99004)`を条件として`var(12)`へ、自動回復量、ダメージ減衰率、被弾後無敵時間、極大Damage閾値を一つのconfigビットフィールドとして設定する。最初に`var(12)`を`0`へ初期化し、項目ごとに分けたControllerが担当bitをビットORする。現在値は自動回復なし、ダメージ減衰率config `4`、無敵時間`30tick`、極大Damage閾値config `30`である。

StateDef `99004010`は無敵時間が`0`のときだけ正の`GetHitVar(damage)`を受け付ける。極大Damage閾値configが`1`以上で、元Damageが`config * 100`以上の場合は、ダメージ減衰率とLife補正を適用せず元Damageを保留する。極大Damage閾値configは最大`32`へ制限する。

通常Damageは、ダメージ減衰率configを最大`25`へ制限し、現在Life比率`r`を`fvar(20)`、減衰後Damageを`fvar(21)`へ順に求めてから、二次曲線`2r-r²`を使用する次の式で解決する。計算を複数Controllerへ分け、WinMUGENの式パーサーへ長大な単一式を渡さない。

```text
floor(min(GetHitVar(damage), 65535) * ダメージ減衰率config / 25 * (2r - r²))
```

元Damageとダメージ減衰率configが正で計算結果が`0`の場合は、保留ダメージを`1`とする。保留ダメージは最大`65535`とし、Rootが次のフレームにその値をそのまま減算する。攻撃受付時にはconfigの固定無敵時間を登録する。

AngleDrawはStateDef `100`、`110`、`111`、`300`、`302`、`303`、`1202`から開始または更新要求を受け、StateNoと独立した持続カウンターで管理する。StateDef `302`は`16tick / type 1`、StateDef `1202`は`5tick / type 2`、StateDef `303`は`4tick / type 3`として、`var(9)`の本体アニメーション変更・時間付き処理を予約する。予約時間の更新と解除は共通化するが、異形回避復帰、突進復帰、ラウンド終了時接地復帰の倍率計算は独立したtype別モデルとする。本予約はRoot本体アニメーション変更に伴う最大511tickの処理だけに使用し、長時間化し得る非本体アニメーション処理には使用しない。StateDef `110`と`111`は本体自由傾斜の1tickリースを毎tick更新し、現在角度を目標角度へ段階的に近づける。リース終了後は同じ角速度で0度へ戻す。Head位置は現在角度と通常基準位置から求め、前方傾斜ではX移動係数`66`、中立・後方傾斜では`61`、Y移動係数は`61`とする。角度と角速度は実機確認中の試験値であり、設計上の確定値ではない。

Head系表示は短距離ワープと異形回避に応じて切り替える。Head眼球は通常時に相手との距離へ同期し、将来の技固有指定では距離同期を無効にして一つの眼球位置へ固定する。暗転番号0はRootのStateDef `1000`で開始する。背景だけを変える青暗転は独立した背景色変更Helperが担当する。

通常の眼球距離同期は`p2dist x`が12以上ならSprite `1,1`、-12より大きく12未満ならSprite `1,2`、-12以下ならSprite `1,3`を完成表示とする。この境界値は実機確認中の試験値であり、設計上の確定値ではない。

Rootが前方ダッシュStateDef `110`または後方ダッシュStateDef `111`の場合は距離同期を無効にし、Sprite `1,1`を完成表示とする。

### 使用変数

変数とbit割当は[the_controller変数一覧](var-list-helper-99004.md)を参照する。

### 重要な実装契約

- Rootアニメーション変更時は、アニメーション時間を保存してからアニメーション番号を保存する。[Rootアニメーション時間保持規約](../AGENTS.root-animtime.md)に従う。
- HeadとHead AuraはControllerが対象別に確定した値を読み、個別HelperでRootのStateDefから変換値を再計算しない。[ADR 023](../ADR/023-head-head-aura-transform-synchronization.md)および[ADR 024](../ADR/024-head-head-aura-controller-managed-position-and-visibility.md)に従う。
- Rootの画面外移動許可条件はControllerのbooleanへ集約し、RootはStateDef `-2`の共通適用口だけで使用する。[ADR 030](../ADR/030-controller-managed-root-screenbound.md)に従う。
- AngleDrawはControllerが完成値と適用フラグを管理し、Aura Boundが通常同期より優先される。[ADR 020](../ADR/020-controller-angledraw-sharing.md)に従う。
- AngleDrawの開始要求、持続時間、1tickリース、プロパティ別合成は[ADR 025](../ADR/025-angledraw-request-bits-and-duration-counters.md)に従う。本体自由傾斜の管理は[ADR 029](../ADR/029-body-free-tilt-request.md)に従う。
- 暗転はControllerの保持値から適用する。[ADR 021](../ADR/021-controller-allpalfx-routing.md)に従う。
