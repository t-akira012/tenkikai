# Sprite Editor

SFFと`assets/sprite.json`、`assets/sprites/`を相互変換するCLIツールを配置する。

確定したCLI形式は次のとおり。

```console
sff-to-json --input binary/sprite.sff --output-json dist/sprite.json --output-png dist/sprites/
json-to-sff --input-json assets/sprite.json --input-png assets/sprites/ --output binary/sprite.sff
```
