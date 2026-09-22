# the_controller Helper

## StateDef 99004000: the_controller集約

ID `99004`の常駐Helper。Rootの状態を監視し、ライフ管理、Helper Armor、オーラバウンド、部位変換、表示制御、暗転を一つの処理列で管理する。

### 毎tickの処理順

```text
99004000 集約・完成値初期化
  → 99004001 / 99004010 ライフ管理・Helper Armor
  → 99004002 / 99004011〜99004013 オーラバウンド
  → 99004005 / 99004021〜99004023 Head位置補正
  → 99004004 / 99004020 Head・Head Aura変換完成
  → 99004003 / 99004100 暗転
  → 99004999 最終処理
  → 5150
```

各ルーターは該当する個別StateDefを0個または1個実行し、必ず次の機能へ進む。詳細な追加規則は[ADR 015](../ADR/015-the-controller-99004-routing.md)に従う。

### 機能

| StateDef | 機能 |
| --- | --- |
| `99004000` | Rootアニメーション時間の保持、暗転時間の更新、AngleDraw・位置・表示の完成値初期化、Body系変換値、PlayerPush無効化、無敵を管理する |
| `99004001`、`99004010` | Rootへ追従するHelper ArmorとしてPlayerPush、攻撃受付、ダメージ値と無敵期間を管理する |
| `99004002`、`99004011`〜`99004013` | RootのStateDef `4001`〜`4003`に対応するオーラバウンドを開始し、残量を消費する |
| `99004005`、`99004021`〜`99004023` | StateDef `300`、`110`、`111`に対応するHead位置補正を完成値へ設定する |
| `99004004`、`99004020` | HeadのOffsetとAngleDrawをHead Auraへ同期し、通常AuraまたはAura Bound時だけ対象別の完成値へ分岐する |
| `99004003`、`99004100` | 暗転ビットフィールドを読み、暗転番号0の全画面黒を適用する |
| `99004999` | 処理列を終了してStateDef `5150`へ戻す |

Body系AngleDrawはStateDef `100`、`110`、`111`、`300`で管理する。Head系表示は短距離ワープと異形回避に応じて切り替える。暗転番号0はRootのStateDef `1000`で開始する。

### 使用変数

変数とbit割当は[the_controller変数一覧](var-list-helper-99004.md)を参照する。

### 重要な実装契約

- Rootアニメーション変更時は、アニメーション時間を保存してからアニメーション番号を保存する。[Rootアニメーション時間保持規約](../AGENTS.root-animtime.md)に従う。
- HeadとHead AuraはControllerが対象別に確定した値を読み、個別HelperでRootのStateDefから変換値を再計算しない。[ADR 023](../ADR/023-head-head-aura-transform-synchronization.md)および[ADR 024](../ADR/024-head-head-aura-controller-managed-position-and-visibility.md)に従う。
- AngleDrawはControllerが完成値と適用フラグを管理し、Aura Boundが通常同期より優先される。[ADR 020](../ADR/020-controller-angledraw-sharing.md)に従う。
- 暗転はControllerの保持値から適用する。[ADR 021](../ADR/021-controller-allpalfx-routing.md)に従う。
