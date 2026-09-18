# コーディング規約

## 対象

この規約は、WinMUGEN用キャラクター「TENKIKAI」の定義ファイルに適用する。

キャラクターの動作を変えずに、改行コード、コメント、書式、ファイル構成を統一し、可読性を高めることを目的とする。

自動整形の実行方法は、[フォーマッター](scripts/formatter.md)を参照する。

## 改行コード

テキストファイルの改行コードは、Windows版MUGENと現行macOSの双方で扱えるLFに統一する。

Gitによるチェックアウトやコミットで改行コードが変化しないよう、`.gitattributes` でLFを指定する。

```gitattributes
* text=auto eol=lf
*.sff binary
*.snd binary
*.act binary
```

`binary/sprite.sff`、`binary/sound.snd`、`binary/pal1.act` はバイナリファイルとして扱い、改行コード変換の対象にしない。

## コメント

定義ファイルから、`;;`で始まる機能塊コメントと罫線コメントを除く、セミコロンで始まる行コメントと行末コメントを削除する。

`;;`で始まる単独行は機能塊コメントとして保持する。StateDef `-2`、`-3` では、浮遊移動、状態同期、表示、ヘルパー生成などの機能塊ごとに`;;`コメントを置く。`cns/observ.cns`の`;;`コメント内容は`docs/state/observ.md`のStateDef `-2`、`-3`の機能塊見出しと同期させ、どちらかを変更した場合はもう一方も更新する。フォーマッターは`;;`コメントの内容を削除・整形しない。

行コメントは、行頭の空白を除いた最初の文字が `;` である行を指す。

```text
; この行は削除する
  ; この行も削除する
```

行末コメントは、設定値や式の後ろにある `;` 以降を指す。セミコロンより前の有効な定義は残し、コメントだけを削除する。

```text
stcommon = common1.cns ;Common states
type = ChangeState ;説明
```

上記は、次のようにする。

```text
stcommon = common1.cns
type = ChangeState
```

ただし、セクションを区切るための罫線コメントは削除せず、次の書式に統一する。

```text
;-------------------------------------------------
```

罫線コメントは、`;` 1文字の後ろに `-` を49文字並べた、合計50文字の行だけを使用する。

ハイフンの数が異なる罫線、`=` などハイフン以外の記号を使った罫線、その他の書式の罫線コメントは、すべて上記の書式に置き換える。罫線の前後には文字や空白を追加しない。

コメント削除によって連続した不要な空行が生じた場合は、後述のブロック間の規則に合わせて整理する。

## StatedefとStateの書式

すべてのStatedefセクションとStateコントローラーを、次の書式に統一する。

```text
[statedef 105]
type=s
ctrl=0
anim=105
velset=0,0

[state ]
type=posadd
trigger1=animtime=0
x=-100
```

次の規則を適用する。

- `[Statedef 番号]` は `[statedef 番号]` にする。
- `[State 番号, 名前]` などのState見出しは、すべて `[state ]` にする。
- State見出しにある番号と説明名は削除する。
- Statedef番号は変更しない。
- セクション内の定義は行頭にそろえ、インデントしない。
- `=` の前後の空白を削除する。
- `&&`、`||`、比較演算子、算術演算子など、演算子の前後にあるASCII半角スペースを削除する。
- `type=` の値は、`type=assertspecial` のようにすべて小文字にする。
- 各Statedefブロックおよび各Stateブロックの間には、空行を1行置く。
- トリガー、式、値、Stateコントローラーの順序は変更しない。
- `[Data]`、`[Size]`、`[Command]`、`[Files]` など、StatedefとState以外のセクション名は、この書式統一による変更対象にしない。

書式変更のみを目的とし、キャラクターの挙動は変更しない。

## 定数とInfoの半角スペース

`cns/constants.cns` は、セクション見出しを含むファイル全体からASCII半角スペースを除去する。

`tenkikai.def` は、`[Info]` セクション内からASCII半角スペースを除去する。

`cns/command.cmd` は、コマンド定義部分からASCII半角スペースを除去する。`[statedef -1]` 以下では、`p2bodydist X` などMUGEN構文上必要な区切りの空白を維持する。

```ini
[Info]
name="TENKIKAI"
versiondate=03,14,2026
```

全角スペースや、他のDEFセクションに対する追加の空白除去は、この規則の対象外とする。

## ファイル構成

キャラクター定数、コマンド、通常ステート、常時監視ステート、ヘルパー用ステートをファイル単位で分離する。

| ファイル | 内容 |
| --- | --- |
| `cns/constants.cns` | `[Data]`、`[Size]`、`[Velocity]`、`[Movement]` などのキャラクター定数 |
| `cns/command.cmd` | コマンド定義と `[statedef -1]` |
| `cns/state.cns` | 0以上9999以下のStatedef |
| `cns/observ.cns` | `[statedef -2]` と `[statedef -3]` |
| `cns/helper.cns` | 10000以上のStatedef |
| `cns/common1.cns` | WinMUGENの `common1.cns` をキャラクター側で管理する共有ステート |
| `cns/anim.air` | Action定義 |
| `binary/sprite.sff` | スプライト |
| `binary/sound.snd` | サウンド |
| `binary/pal1.act` | パレット |

現在の共通ルーター`[statedef 99000]`と、常駐Helperごとの専用StateDefは、`cns/helper.cns`に配置する。

`cns/common1.cns` と他のステートファイルに同じStateDef番号が存在する場合は、他のステートファイルを優先する。重複するStateDefブロックは、`cns/common1.cns` 側から削除する。

`tenkikai.def` の `[Files]` では、分割したファイルを次のように参照する。

```ini
[Files]
cmd=cns/command.cmd
cns=cns/constants.cns
st=cns/state.cns
st1=cns/observ.cns
st2=cns/helper.cns
stcommon=cns/common1.cns
sprite=binary/sprite.sff
anim=cns/anim.air
sound=binary/sound.snd
pal1=binary/pal1.act
```


## 変更後の確認

整形と分割を行った後は、次を確認する。

- 全テキストファイルがLFになっていること。
- バイナリファイルが変更されていないこと。
- 罫線コメントがすべて、`;` 1文字と `-` 49文字からなる合計50文字の行になっていること。
- 罫線コメント以外の行コメントと行末コメントが残っていないこと。
- 全Statedef番号が分割前後で一致すること。
- `cns/common1.cns` と他のステートファイルに重複するStateDef番号がないこと。
- Stateコントローラーの数と順序が分割前後で一致すること。
- `tenkikai.def` からすべての分割ファイルを参照できること。
- `cns/constants.cns` と `[Info]` にASCII半角スペースが残っていないこと。
- `cns/command.cmd` のコマンド定義部分にASCII半角スペースが残っていないこと。
- StatedefとStateブロックの `type=` の値に大文字が残っていないこと。
- StatedefとStateブロックの演算子前後にASCII半角スペースが残っていないこと。
- 定義内容に意図しない変更がないこと。
