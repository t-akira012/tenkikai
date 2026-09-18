# Sprite Editor方針

## 目的

`assets/`に置いたPNG画像を、macOSのCLIだけでWinMUGEN用の`binary/sprite.sff`へ追加できるようにする。既存のSFFを破壊せず、追加した画像をAIR定義から利用できる状態にする。

## 正規ソースと生成物

スプライトの正規ソースは、次のテキスト・画像ファイルとする。

```text
assets/sprite.json
assets/sprites/*.png
```

`assets/sprite.json`には、各画像のグループ番号、画像番号、原点、パレット、透明色などのSFF定義を記録する。画像本体は`assets/sprites/`へ個別のPNGとして保存する。番号定義はバイナリSFFを直接編集せず、JSONの変更として行う。

`binary/sprite.sff`は生成物とし、正規ソースから毎回再生成する。生成物を直接編集してはならない。

既存SFFの展開は次の形式で行う。

```text
binary/sprite.sff
  ↓ sff-to-json
assets/sprite.json
assets/sprites/*.png
```

再構築は次の形式で行う。

```text
assets/sprite.json + assets/sprites/*.png
  ↓ json-to-sff
binary/sprite.sff
```

同じJSONと画像から同じスプライト構成を再生成できることを目標とする。SFFのバイナリ配列や内部オフセットの一致ではなく、画像、番号、原点、パレット、透明色などの意味的な一致を保証する。

## 試作の範囲

試作では、次の処理だけを対象にする。

1. 既存SFFを`assets/sprite.json`と`assets/sprites/`へ展開する。
2. `assets/sprites/`内のPNGの透明部分を判定し、SFFで扱えるインデックス画像へ変換する。
3. JSONで指定した番号・原点・パレットに従ってSFFを再構築する。
4. 既存スプライトを保持したまま、新規スプライトを追加する。
5. 再構築後のSFFを検査し、JSONと画像の定義が反映されていることを確認する。

試作段階では、元の`binary/sprite.sff`を直接上書きしない。作業用のコピーへ出力し、形式検査と画像数・画像番号・サイズの確認が完了した後に置換可能とする。既存SFFを正規ソースへ展開した後は、SFFではなくJSONとPNGを編集する。

## SFFの扱い

初回の`binary/sprite.sff`を入力として使用し、SFFのバージョン、スプライト一覧、パレット、画像データの格納方式を読み取って正規ソースへ展開する。以後は`assets/sprite.json`と`assets/sprites/`を入力として使用する。

新規画像は既存SFFの形式に合わせて追加する。PNGのアルファチャンネルはそのまま格納せず、SFFの透明色およびパレットインデックスへ変換する。既存画像のグループ番号・画像番号・原点は変更しない。

## CLIツールの責務

ツールは、次の確定済みオプション形式で入出力を指定する。SFFからの展開結果は`dist/`へ出力し、編集用の`assets/`を上書きしない。

```console
sff-to-json \
  --input binary/sprite.sff \
  --output-json dist/sprite.json \
  --output-png dist/sprites/

json-to-sff \
  --input-json assets/sprite.json \
  --input-png assets/sprites/ \
  --output binary/sprite.sff
```

入力画像の順序と割り当て結果を端末へ表示し、処理対象・現在の画像・完了・失敗を隠さない。

画像変換とSFF入出力を分離し、PNGの透明化だけを再実行しても既存SFFへ影響しない構成にする。既存SFFのバックアップはツール内で削除せず、出力先を分けて保持する。

## 検証

試作ツールは次を検証する。

- 入力PNGが存在し、読み込み可能であること。
- 透明部分が検出され、透明色として一貫して変換されること。
- 画像サイズがSFFへ格納可能であること。
- 既存SFFのヘッダーと既存スプライト数が追記前後で維持されること。
- 新規画像のグループ番号・画像番号・原点が指定値と一致すること。
- 出力SFFがWinMUGENから読み込める形式であること。

macOS上ではバイナリ構造と画像データの検査まで行い、実際の描画とAIRからの参照はWindows上のWinMUGENで確認する。

## 復旧

試作出力に問題があった場合は、commit済みの`binary/sprite.sff`へ戻せるようにする。元ファイルを直接編集せず、検証済み出力だけを明示的に置換する。
