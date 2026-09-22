# the_aura Helper

## StateDef 99002000: オーラ常駐

`the_aura`はRootの描画を基礎として、Root・頭部・Head auraと向きを一致させ、ダッシュ方向に応じたBody auraの傾斜を表示する。

### Root位置追従

Rootの位置を読み取り、Auraの基準位置へ反映する。

### Root向き同期

Rootの向きを読み取り、Aura自身の`facing`へ毎フレーム同期する。向きを一致させるためにRootへ合わせて`Turn`する。

### Rootアニメーション同期

Rootのアニメーション番号と要素位置を読み取り、Auraの表示アニメーションを同期する。

### Aura倍率・傾斜同期

前後ダッシュに合わせてBody auraを傾斜させる。傾斜はRootのダッシュ状態と同じ向きで適用し、Aura側の独立した符号補正は行わない。詳細な判断は[ADR 008](../ADR/008-aura-facing-synchronization.md)を参照する。

ControllerのBody Aura適用フラグが有効で、Aura Boundフラグが無効な場合は、Controllerが保持するBody系完成角度およびX・Y倍率を適用する。Aura Bound中は既存のAura倍率を優先し、共有AngleDrawを適用しない。

Body Aura適用中は、Controllerが保持するBody系完成Y Offsetも使用する。これによりBodyの浮遊表示と、縮小時のaxis基準による中心移動補正へ同じ位置で追従する。

### Aura浮遊オフセット

Rootの浮遊表示に合わせて、Auraの表示位置を補正する。バウンド中は`the_controller`の進行量も反映する。

### Aura透過表示

Aura専用の透過表示を適用する。

### Aura残像

Aura専用のAfterImageを生成し、Auraの移動と表示変化に残像を付加する。

RootがStateDef `301`の場合はAura本体を非表示にして残像を消去する。StateDef `302`で残像の初回生成フラグを解除し、再出現後の残像を再開する。

## StateDef 99002999: 最終処理

オーラ追従の完了後に`SelfState value=5150`を実行する。
