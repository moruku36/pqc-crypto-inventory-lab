# 移行前後の比較演習

[模擬システム](../samples/mini-service/README.md)を変更前、`samples/migration-after`を変更案として比べます。変更案は設定と説明用コードの例で、PQCの実装・配備・相互接続を検証したものではありません。

```sh
pqc-scan compare ./samples/mini-service ./samples/migration-after
pqc-scan review ./samples/migration-after --output reports/after-review.csv
```

`compare`は同じ相対パス・検出種別・方式・分類の件数を比較します。`removed_evidence`は根拠が消えたこと、`added_evidence`は新しい根拠が現れたことを示します。稼働中の暗号が変更された証明ではありません。途中で読めなかったファイルがある場合は`issues`と`truncated`を先に確認してください。
同じ方式のまま内容だけが変わった場合、この比較には現れません。

| 変更 | 比較結果の読み方 | 残る確認事項 |
|---|---|---|
| 設定のX25519→ML-KEM | X25519の設定根拠が消え、ML-KEMの設定根拠が追加される | 通信相手、TLS実装、フォールバック、鍵交換の互換性 |
| 署名コードのRSA呼び出し→ML-DSA設定 | RSAのAPI呼び出しが消え、ML-DSA設定が追加される | 署名形式、鍵管理、検証側、署名サイズの対応 |
| 証明書はRSAのまま | RSA公開鍵の根拠が残る | PKIと証明書の更新計画。設定だけでは解決しない |
| 旧コードはSHA-1のまま | SHA-1の根拠が残る | 未使用という申告の確認、削除可否、既存の衝突リスク |
| 保存データの設定はAES-256のまま | AES-256の設定根拠が残る | データとの対応、実際の暗号化、保持期間 |

架空の[接続先対応表](../samples/migration-compatibility.json)では、`legacy-client`がML-KEMとML-DSAに対応せず、`pilot-client`は両方に対応する設定です。変更案を全利用者へ一斉に適用できるとは判断できません。これは演習用の仮定で、実製品の対応状況ではありません。

演習では[運用確認票](review-workflow.md)に責任者、用途、稼働状況、データ保持期間、公開範囲、確認資料を記入します。移行案の検出件数や`SAFE`という表示だけで完了と判断しないでください。
