# animation-gif-spritter方針

## 目的

`assets/gif/`に配置したアニメーションGIFを、SFF登録や個別編集に利用できるフレーム単位のPNGへ分割する。

## 入出力

入力は`assets/gif/*.gif`とする。出力はGIFごとに専用ディレクトリを作成し、次の形式で保存する。

```text
assets/gif/example.gif
  ↓ animation-gif-spritter
assets/sprites/example/0000.png
assets/sprites/example/0001.png
assets/sprites/example/0002.png
```

フレーム番号は0から始め、GIF内の順序を維持する。既存のPNGを無断で上書きせず、出力先が存在する場合はエラーにするか、明示的な上書き指定を要求する。

## フレーム変換

GIFの各フレームを、表示結果どおりに合成してからPNGへ書き出す。単一フレームの差分だけを抽出せず、GIFのdisposal methodと前フレームの状態を考慮する。

透明部分はアルファチャンネルとして保持する。フレームのサイズ、透明領域、フレーム順を変換によって変更しない。

フレーム遅延時間は素材分割では記録しない。遅延時間は、分割後のPNGを使って`animation.air`を作成する段階で定義する。

## CLIの確定形式

単一GIFの分割は次の形式で実行する。

```console
animation-gif-spritter \
  --input assets/gif/example.gif \
  --output-png assets/sprites/example/
```

CLI本体は`scripts/animation-gif-spritter/`へ配置する。SFFとスプライト番号を扱う`scripts/sprite-editor/`とは責務を分離し、Pythonの実行と依存関係はscripts共通規約に従ってuvで管理する。

## 検証

- 出力PNGの枚数がGIFのフレーム数と一致すること。
- フレーム番号が連続し、入力順を維持すること。
- 合成後の各フレームが元GIFの表示結果と一致すること。
- 透明部分が保持されること。
- 既存PNGを意図せず上書きしないこと。
