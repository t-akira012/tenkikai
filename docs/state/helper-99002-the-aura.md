# the_aura Helper

## StateDef 99002: オーラ常駐

`the_aura`はRootの描画を基礎として、位置、向き、アニメーション、倍率、浮遊オフセット、透過、残像を毎フレーム更新する。

### Root位置追従

Rootの位置を読み取り、Auraの基準位置へ反映する。

### Root向き同期

Rootの向きを読み取り、Aura自身の`facing`へ毎フレーム同期する。`facing`は左右反転の同期だけに使用し、傾斜角の計算には使用しない。

### Rootアニメーション同期

Rootのアニメーション番号と要素位置を読み取り、Auraの表示アニメーションを同期する。

### Aura倍率・傾斜同期

RootのStateNoを確認し、通常時またはダッシュ時の表示倍率と傾斜を一つの`AngleDraw`で適用する。前後ダッシュの傾斜はRootの正規定義と同じ値を使い、Aura側で符号反転や追加補正を行わない。詳細な判断は[ADR 008](../ADR/008-aura-facing-synchronization.md)を参照する。

### Aura浮遊オフセット

Rootの浮遊表示に合わせて、Auraの表示位置を補正する。バウンド中は`the_root_monitor`の進行量も反映する。

### Aura透過表示

Aura専用の透過表示を適用する。

### Aura残像

Aura専用のAfterImageを生成し、Auraの移動と表示変化に残像を付加する。
