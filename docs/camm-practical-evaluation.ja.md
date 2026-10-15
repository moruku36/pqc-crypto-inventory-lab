# CAMM評価論文から考える、根拠付きの暗号移行評価

**状態：文書による改善提案。採点・CLI・スキーマの変更、追試は未実施。確認日：2026-10-15 UTC。**

[Practical Evaluation of the Crypto-Agility Maturity Model](https://arxiv.org/abs/2604.12428v1)（Wolfほか、v1、2026-04-14）の書誌・評価条件・限界は[論文サーベイ](https://github.com/moruku36/independent-cs-research-2026/blob/main/surveys/collection-v2/2026-camm-practical-evaluation.md)に記録した。[原文PDF](https://arxiv.org/pdf/2604.12428v1)の§3–5は、成熟度を判定する範囲と証拠を明確にする必要性を示している。ラボへの採用案は以下の独自提案であり、論文による本ラボの検証ではない。

## 現在のラボで確認できること

[採点仕様](scoring.md)は10項目の独自ヒューリスティックで、CAMMのレベル判定ではない。合計点をCAMM 0–4に換算しない。

| 現在の仕組み | 読み取り上の限界 |
|---|---|
| 静的解析の `STATIC_EVIDENCE` | ファイル上の手掛かり。稼働環境の完全な棚卸しや移行成功は証明しない |
| 運用申告の `DECLARED` | `tested`でも試験自体をツールが独立検証したわけではない |
| `UNKNOWN`、`partial_inventory` | 根拠不足や対象範囲の制約。能力欠如や安全性を断定しない |
| [人の確認票](review-workflow.md)と[変更前後の比較](migration-exercise.md) | 人による確認や静的根拠の比較を支える。CAMM認証や本番移行試験を代替しない |

## 今後の改善案と受入条件（すべて未実施）

| 順序 | 提案 | 完了と判断するための条件 |
|---|---|---|
| 1 | 既存CSVと別の手作業評価票を作る | 対象commit・ファイル範囲・除外範囲・評価者・日付を記載する。既存CSVやmanifestの対応外フィールドとして投入しない |
| 2 | 要件ごとに証拠と判断を分ける | 要件ID、確認手順、期待結果、証拠参照、観測／申告の別、適用性と理由、判断を記載する。未確認と対象外を区別し、対象外を自動加点しない |
| 3 | 評価者間の解釈差を調べる | 公開合成サンプルを2人以上が独立判断し、合議前の記録と不一致理由を残す。都合のよい合意結果だけを保存しない |
| 4 | 移行の運用根拠を別途確認する | 切替・互換性・切戻し・最低セキュリティ条件の試験計画と、実行結果を区別する。未実行なら未実行と記載する |
| 5 | 自動評価の追加可否を判断する | 再現可能な判定基準と人のレビューで有用性を確認してから、別変更としてスキーマとテストを設計する。今回の提案で既存点数を変更しない |

最初の成果物は、[正解つき模擬システム](../samples/mini-service/README.md)を対象にした手作業評価票1件を想定する。ここではその評価票の作成・実行・一致率測定まで完了したとは主張しない。外部TLSへの追加アクセスや本物の鍵の取得は演習に含めない。

## 他の改善計画との関係

[PQC discoveryの読書ノート](pqc-discovery-governance.ja.md)で扱う責任者・供給者の制約と合わせて使う。性能に関する将来計画は[README](../README.md)を参照し、測定していない性能値を成熟度や安全性の根拠にしない。

## English

This documentation-only proposal keeps the existing heuristic score separate from CAMM maturity levels. The next step is a manual, scoped evidence worksheet and independent reviewer exercise. No new assessment engine, schema or migration test has been implemented.

[日本語README](../README.ja.md) | [出典索引](references.md) | [採点仕様](scoring.md)
