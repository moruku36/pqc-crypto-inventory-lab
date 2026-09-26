# 運用確認票

スキャナーの検出結果から、人が調べる項目をCSVに書き出します。

```sh
pqc-scan review ./samples/mini-service --output reports/mini-service-review.csv
```

CSVには検出ID、場所、方式、スキャナーの分類と、空欄の`owner`、`purpose`、`runtime_state`、`data_retention_years`、`exposure`、`verification_source`、`next_action`が入ります。既存ファイルは上書きしません。読取エラーや件数制限で棚卸しが不完全な場合は出力せず、まず調査対象を確認します。

確認欄はスキャナーの判断ではありません。担当者の回答や設定・運用記録で埋め、`verification_source`に根拠を記します。検出されなかった資産や保存データはCSVに自動で載らないため、行を手動で追加してください。[模擬システムの正解表](../samples/mini-service-ground-truth.json)には、その例も記載しています。

[記入例](../samples/mini-service-review-example.csv)には、検出6行と手動で追加した2行を載せています。`declared`と書いた情報は演習上の申告であり、実運用を確認した結果ではありません。同じ設定ファイルのAES-256が2件出ても、どちらが保存データに対応するかは検出結果だけでは決められません。

結果のCSVにはファイル名や内部運用情報が含まれる場合があります。共有前に確認し、既定の`reports/`内で保管してください。表計算ソフトで開く場合も、検出元の名前を数式として実行しないよう、先頭の危険文字はエクスポート時に無害化します。
