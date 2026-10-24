# ADR 038: Controller管理の全体非表示フラグ

## 状態

採用

## 背景

Root、Head、Head Aura、Body Auraの非表示判断がRootのStateDef、Controllerの対象別bit、各HelperのAfterImage処理へ分散していた。部分的な非表示と全体非表示が区別されず、全体が消える動作でもAfterImageが残ることがあった。

## 決定

### 全体非表示フラグ

全体非表示は`the_controller`の`var(22)` bit 8（マスク`256`）で管理する。`the_controller`はRootの状態から全体非表示の成立を毎tick判定し、bit 8を完成させる。Root、Head、Head Aura、Body AuraはRootのStateDefを直接判定せず、このbitを読む。

bit 8が有効な間、各表示対象は`AssertSpecial flag=invisible`を適用する。同じbitをAfterImageの消去と生成抑止にも使用し、各対象のAfterImage所有側が`AfterImage time=0`を発行して過去の残像を消す。非表示中は通常のAfterImageを再生成せず、フラグ解除後に各対象の生成済みbitを戻して残像を再開する。

### 部分非表示との関係

Headだけを非表示にする既存区間のため、`var(22)` bit 0（マスク`1`）はHead専用の部分非表示フラグとして維持する。Headの非表示条件はbit 0または全体非表示bit 8の成立とする。

Head Aura、Head AfterImage、Head Aura AfterImageの対象別bit 1〜3は全体非表示bit 8へ統合し、再割り当てしない。bit 4〜7のOffset非同期、AngleDraw非同期、Body AngleDraw適用、Body Aura AngleDraw適用は維持する。

### 非表示成立の判定

`the_controller`は、Rootが全体非表示になる状態でbit 8を設定する。短距離ワープの消失区間、異形回避の消失区間、および技固有の消失区間を対象とする。Rootが表示されたままHeadだけを隠す区間はbit 0で扱い、bit 8を立てない。

## 結果

- Root、Head、Head Aura、Body Auraの全体非表示とAfterImage停止が一つのController bitで同期する。
- AuraはRootのStateDefを直接判定しない。
- Headだけを隠す既存表現は個別bit 0で維持できる。
- AfterImageは非表示開始時に消去され、非表示中に再生成されない。
