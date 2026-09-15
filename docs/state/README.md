# ステートドキュメント

## 目的

この文書群は、CNSとCMDから削除したコメントに代わり、TENKIKAIの各StateDefが担当する挙動を日本語で説明する。上流の方針は[キャラクターデザイン](../DESIGN.md)を参照する。

CNS/CMDの実装と挙動文書のどちらをマスターとするかは定めない。両者に差異が生じた場合は差異をユーザーへ提示し、どちらを正として修正するかはユーザーの指示に従う。

## 文書一覧

- [デフォルトステート](state-default.md): TENKIKAI固有の移動、登場、勝利、入力遷移
- [アタックステート](state-attack.md): 通常技、通常投げ、必殺技
- [超必殺技ステート](state-superattack.md): 超必殺技
- [ヘルパーステート](state-helper.md): 常時監視と頭部ヘルパー
- [stcommon共有ステート](state-stcommon.md): `cns/common1.cns` にあるWinMUGEN共有ステート
- [ヘルパー一覧](helper-list.md): `Helper` コントローラーが生成するヘルパー
- [Explod一覧](explod-list.md): `Explod` コントローラーが生成する演出物
- [Projectile一覧](projectile-list.md): `Projectile` コントローラーが生成する飛び道具
- [変数一覧](var-list.md): CNSで使用する通常変数とシステム変数

## 記述規則

すべての挙動で、H2見出しを挙動名、H3見出しを `StateDef NUM: 機能名` の形式にする。挙動とStateDefが1対1の場合も、1対多の場合も、このH2・H3構造を省略しない。

```markdown
## 挙動名

### StateDef NUM: 機能名
```

技については、入力、消費パワー、移動、攻撃判定、相手への効果、遷移先をコードから確認できる範囲で記載する。

## StateDefの優先順位

キャラクター固有ファイルと `cns/common1.cns` に同じStateDef番号がある場合は、キャラクター固有ファイルを優先する。

```text
cns/command.cmd・cns/state.cns・cns/observ.cns・cns/helper.cns > cns/common1.cns
```

重複するStateDefはフォーマッターによって `cns/common1.cns` 側から削除される。現在はStateDef `100`、`105`、`106`、`191` がキャラクター固有の実装へ置き換えられている。

## 参照資料

- [Elecbyte CNS形式](https://www.elecbyte.com/mugendocs/cns.html)
- [WinMUGEN 2002.04.14 State Controllerリファレンス](https://bluesura.github.io/MUGEN/document/Official/2002.04.14/sctrls.html)
- `cns/command.cmd`
- `cns/state.cns`
- `cns/observ.cns`
- `cns/helper.cns`
- `cns/common1.cns`
