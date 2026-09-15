# Samples

## どれから開けばよいか

まず[採点付きレポート](crypto_inventory_scored.md)を開くと、実行しなくても結果の形が分かります。
英語の見出しは[結果の読み方](../docs/reading-results.md)と見比べてください。

| ファイル | 中身 |
|---|---|
| [project/crypto_example.py](project/crypto_example.py) | RSAとSHA-1を使う処理を書いた学習用のコード。棚卸し時には実行されない |
| [project/security.json](project/security.json) | AES-256、X25519、SHA-384を指定した学習用の設定 |
| [project/.pqc-agility.json](project/.pqc-agility.json) | 設計を文書化したことを申告する採点用設定 |
| [project/agility_design.txt](project/agility_design.txt) | その申告で参照する設計メモ。実装や本番試験の成功記録ではない |
| [directory.json](directory.json) | フォルダーを調べた結果。現在のサンプルは5件検出 |
| [score.json](score.json) | 25点の採点結果と各項目の理由 |
| [crypto_inventory_scored.md](crypto_inventory_scored.md) | 採点を含むレポート。最初に読む例としてはこちら |
| [crypto_inventory.md](crypto_inventory.md) | Phase 3時点の、採点機能を追加する前のレポート |
| [tls-github.json](tls-github.json) | GitHubへのTLS接続で観測した公開情報。日時・環境で値は変わる |

`project`以下は操作練習用に作成したサンプルです。実際の秘密情報は格納していません。
実行方法は[操作ガイド](../docs/getting-started.md)にあります。
