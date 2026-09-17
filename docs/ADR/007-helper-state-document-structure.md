# ADR 007: Helper StateDef文書の分離

## 状態

採用

## 背景

`docs/state/helper.md`へ複数のHelperの一覧、要約、機能塊の詳細を同時に記載すると、一覧性が失われる。HelperごとのStateDef処理と、各StateDef内の機能塊を独立して参照できる構造が必要である。

## 決定

`docs/state/helper.md`はHelper StateDefの一覧と短い概要に限定する。個別Helperの詳細は、`docs/state/helper-ID-name.md`形式の専用文書へ分離する。

専用文書には、対象HelperのStateDef遷移、処理内容、CNSの`;;`機能塊コメントとの対応を記載する。個別Helperの詳細文書は`helper.md`からリンクする。

## 結果

Helper一覧を短く保ったまま、個別Helperの実装構造を機能塊単位で参照できる。新しいHelperを追加する場合も、一覧への概要追加と専用詳細文書の作成を分けて行える。
