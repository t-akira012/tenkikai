# ステート文書の作業規則

## 文書群の責務

`docs/state/`は、CNSとCMDから削除したコメントに代わり、TENKIKAIの各StateDefが担当する挙動を日本語で記録する。上流の方針は[キャラクターデザイン](../DESIGN.md)に従う。

CNS/CMDの実装とステート文書のどちらをマスターとするかは定めない。両者に差異がある場合は、差異をユーザーへ提示し、どちらを正として修正するかはユーザーの指示に従う。

## StateDef文書の構成

StateDef `-1`、`-2`、`-3` は常時監視ステートであり、記述量が多くなるため、1つの段落へまとめず、機能塊ごとに小見出しを作成する。

基本の見出し構造は次のとおりとする。

```markdown
## 挙動名

### StateDef NUM: 機能名

#### 機能塊
```

StateDef `-1`、`-2`、`-3` 以外でも、1つのStateDefに複数の独立した機能がある場合は、同じ小見出し構造を使用してよい。

StateDefの番号、Controllerの順序、Trigger条件、座標、速度、時間、ダメージなどの仕様は、CNS/CMDから確認できる範囲で記載する。文書化のために実装を変更してはならない。

技については、入力、消費パワー、移動、攻撃判定、相手への効果、遷移先をコードから確認できる範囲で記載する。

## StateDefの優先順位

キャラクター固有ファイルと`cns/common1.cns`に同じStateDef番号がある場合は、キャラクター固有ファイルを優先する。

```text
cns/command.cmd・cns/state.cns・cns/observ.cns・cns/helper.cns > cns/common1.cns
```

重複するStateDefはフォーマッターによって`cns/common1.cns`側から削除される。現在はStateDef `100`、`105`、`106`、`191`がキャラクター固有の実装へ置き換えられている。

## 参照資料

- [Elecbyte CNS形式](https://www.elecbyte.com/mugendocs/cns.html)
- [WinMUGEN 2002.04.14 State Controllerリファレンス](https://bluesura.github.io/MUGEN/document/Official/2002.04.14/sctrls.html)
- `cns/command.cmd`
- `cns/state.cns`
- `cns/observ.cns`
- `cns/helper.cns`
- `cns/common1.cns`

## 常時監視ステートの機能塊コメント

`cns/observ.cns` のStateDef `-2`、`-3` では、機能塊の開始位置に `;;` コメントを置く。コメント名は `docs/state/observ.md` の対応する機能塊見出しと一致させ、どちらかを変更した場合はもう一方も同期して更新する。フォーマッターはこの `;;` コメントを削除または整形してはならない。
