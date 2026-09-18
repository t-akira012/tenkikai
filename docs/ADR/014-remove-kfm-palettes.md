# ADR 014: KFM由来パレットの撤去

## 状態

採用

## 背景

`pal2.act`から`pal6.act`はKFM由来のパレットであり、TENKIKAIのキャラクターデザインに必要な差分ではない。TENKIKAIは独自の宇宙生命体として設計するため、KFM由来の揺らぎを残す理由がない。

## 決定

`binary/pal2.act`から`binary/pal6.act`を削除する。`tenkikai.def`の`pal2`から`pal6`の参照も削除し、標準パレットとして`binary/pal1.act`だけを使用する。

フォーマッターのDEF参照検査とコーディング規則も、`pal1.act`だけを対象とする。

## 結果

KFM由来のパレットを配布物とキャラクター定義から除外し、TENKIKAI固有のパレット構成へ統一する。
