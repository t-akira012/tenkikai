# 常時監視ステート

## 常時監視

### StateDef -2: State奪取中も動く監視

| 機能 | 動作 |
| --- | --- |
| 自動運用 | `var(2)`のbit 31を管理する。常時有効化は無効で、パレット`6`〜`12`で有効 |
| Helper Armor config | AI設定欄でHelper ID `99004`だけを対象に`var(12)`を初期化し、自動回復量、ダメージ減衰率、被弾後無敵時間、極大Damage閾値を項目別ControllerからビットORする |
| Root試合終了直後Ctrl有効化 | `RoundState=3`かつStateDef `303`以外では、RootのCtrlを毎tick有効化する |
| ライフ | Controllerが倍率・Life二次曲線・極大Damage判定から解決した保留ダメージをそのまま反映する。保留ダメージなし・生存中・最大Life未満で、Controllerの自動回復量configが正の場合だけ設定量を回復する。現在の回復量は`0` |
| ScreenBound同期 | ControllerのRoot画面外移動許可booleanが有効な間だけ本体の`ScreenBound`を無効化し、カメラを追従させない。無効時は通常の画面内拘束とカメラ移動を許可する |
| 時間・デバッグ | `private-gametime`などの変数とデバッグ表示を更新する |
| Body変換 | 通常AngleDrawとOffsetを初期化し、Controllerの適用フラグが有効な場合だけ完成値を使う |
| 地面隣接浮遊時の足元波紋 | `Pos Y>=-20`かつ`abs(Vel X)<1`の間、24tickごとにHelper ID `500020`・`500021`を一組生成する。`postype=p1`の`pos=0,-pos y+26`で生成時のRoot直下にあるステージ地面へSprite軸補正を加えて置き、生成後はRootへ追従させない。`abs(Vel X)>=1`では波紋も砂埃も生成しない |

### StateDef -3: 通常時の移動・表示・Helper生成

| 機能 | 動作 |
| --- | --- |
| 接地許可フラグ | 毎tick bit 17を消去し、StateDef `1200`〜`1204`以外で設定する。通常の接地判定は各処理に残る従来条件が行う |
| 試合終了時の接地復帰 | `RoundState=3`または`4`、`Pos Y<0`、`StateNo<200`の場合にStateDef `303`へ移る。`StateNo>=200`の技・回避・被弾中には割り込まない |
| 期限付き移動要求 | 要求元のStateDef番号を判定せず、`private-gametime`期限内の目標X・Y速度へ加速する。最低速度保証中は同方向の目標以上のX速度を維持する。水平期限切れ後は開始時の`abs(Vel X)`が`3`以下なら32tick、`3`を超える場合は16tickの半コサイン曲線、垂直期限切れ後は最後の加減速度で0へ減速し、個別処理の排他期限中は対象軸を変更しない |
| 浮遊移動 | 上入力は上部制動を含む目標Y速度、空中の下入力は下降目標速度、無入力時は高度に応じた下降または停止要求へ変換する。接地許可フラグが立ち、各Controllerの従来の接地条件も成立する場合にY位置・速度補正と地上StateType/Physics設定を行う |
| 空中歩行 | StateDef `60`、`61`は対応する前後入力がなければStateDef `0`へ戻す |
| 浮遊表示 | 対象Actionへ`private-gametime`基準の周期Offsetを適用する。StateDef `1000`～`1999`の攻撃を含み、被弾中と`crunch`は対象外 |
| Helper生成 | ID `99004`、`99001`、`99003`、`99002`の常駐Helperを個別に存在確認して生成する |
| 残像 | Rootの加算残像を初回と600tickごとに更新する |

使用変数は[Root変数一覧](var-list-root.md)を参照する。
