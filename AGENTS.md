# AGENTS.md

このリポジトリは、WinMUGEN用キャラクター「TENKIKAI」のキャラクターディレクトリです。

Codexの動作環境はmacOS上である。WinMUGENはWindows 11 on VMware上で動作するため、挙動の実機検証はユーザーに任せる。Codexによる技や移動などの動作検証は、定義、遷移条件、座標、速度、時間、ダメージなどに基づいて数学的に行うこと。

`docs/state/*.md` の動作定義とCNSファイルのステート定義に差異がある場合は、ユーザーへ報告すること。どちらをマスターとするかは定義されていない。Codexは差異のある記述とCNS定義をユーザーへ提示し、どちらを正として修正するかは場合ごとのユーザー指示に従うこと。

作業時は、次の文書に従ってください。

- [コーディング規約](docs/coding-rules.md)
- [フォーマッター](docs/formatter.md)
- [キャラクターデザイン](docs/DESIGN.md)
- [ステートドキュメント](docs/state/README.md)
- [設計判断記録](docs/ADR/)
