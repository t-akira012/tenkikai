# Helperコーディング規約

## 常駐Helperの定義

- 常駐Helperとは、ラウンド中に継続して存在し、本体の常時監視から存在確認と再生成を行い、専用StateDefで毎フレーム処理するHelperを指す。
- HelperType を Player にすることで、常駐helperとして機能する。常駐helperは StateDef -2, -3 を読み込む
- 同一IDは1体以下に制限する。

## Helperルーティング規約

- StateDef `-2` での Helper 処理はには常駐Helperのルーティングだけを記述する。
- ルーティング以外のHelper処理を `-2` に記述しても、機能しない。
- 位置、アニメーション、表示などの実処理は、ルーティング先の個別StateDefで行う。
- 非常駐Helperは常駐Helperルーティングの対象外とする。
