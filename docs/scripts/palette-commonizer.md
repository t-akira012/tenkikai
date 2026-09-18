# palette-commonizer仕様

## 目的

複数のPNG素材を既存のACTパレットへ変換し、SFFへ登録したときの色調を共通化する。画像の編集やGIFの分割、パレット自体の生成は行わない。

## 責務

`palette-commonizer`は、指定されたACTファイルを読み込み、各入力画像をそのパレットへ変換する。

- 入力画像のフレーム順、画像サイズ、ディレクトリ構造を維持する。
- PNGの左上1pxの色を透明色として扱い、SFFで使用する透明インデックスへ割り当てる。
- 元のPNGは変更せず、指定した出力先へ変換結果を書き出す。
- SFFのグループ番号・画像番号や`animation.air`の表示時間は扱わない。

GIFの分割は`animation-gif-spritter`、SFFのJSON変換と生成は`sprite-editor`が担当する。

## 入出力

入力は`assets/sprites/*.png`とし、共通パレットには`binary/pal1.act`を使用する。変換結果は`dist/pallet-commonizer/`へ出力し、入力側のファイル名と順序を維持する。`assets/sprites/`は変更しない。

```text
binary/pal1.act
assets/sprites/*.png
        ↓ palette-commonizer
dist/pallet-commonizer/*.png
```

既存の出力PNGは、`make pal-commonizer`の再生成時に更新する。CLIを直接実行する場合は`--overwrite`を明示したときだけ既存ファイルを更新する。

## CLIの確定形式

```console
palette-commonizer \
  --palette binary/pal1.act \
  --input assets/sprites/ \
  --output dist/pallet-commonizer/ \
  --overwrite
```

Makefileからは次のコマンドで実行する。

```console
make pal-commonizer
```

実行状況は、対象ディレクトリ、現在の画像、完了、失敗を端末へ表示する。Pythonの実行と依存関係はscripts共通規約に従ってuvで管理する。

## パレット変換

ACTは256色分のRGBを格納する768バイトのファイルとして読み込む。ACTにはアルファ情報がないため、入力PNGのアルファ透明画素はSFFで使用する透明インデックスへ割り当てる。さらに、透過PNGでない場合も含め、各PNGの左上1pxのRGBを透明色として扱い、同じRGBの画素を透明インデックスへ割り当てる。これはWinMUGENで一般的な透明色指定方式である。透明色以外のRGBがACT内に完全一致しない場合は、同じ最近似色規則でACTの色へ変換する。

変換結果はACTのパレットを埋め込んだインデックスPNGとして保存する。元画像のRGBA表現は入力素材として保持し、共通化済み画像をSFF生成の入力に使用する。既定のACTは`binary/pal1.act`とし、別のACTを使う場合は明示的に指定する。

## 検証

- 入力画像の枚数と出力画像の枚数が一致すること。
- 入力側の相対パスとフレーム順が維持されること。
- 全出力画像が指定ACTと同じパレットを使用すること。
- アルファ透明画素と左上1px由来の透明色が保持されること。
- 元のPNGが変更されていないこと。
- `--overwrite`なしでは既存出力を上書きしないこと。
