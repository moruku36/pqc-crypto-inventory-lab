# References

確認日: 2026-09-15。公開ページで版と適用範囲を確認しました。
以下は実装時に確認した資料の記録です。

## 追加の研究ノート（2026-10-12確認）

| 資料 | 保存した読書ノート | このプロジェクトとの関係 |
|---|---|---|
| [Post-Quantum Discovery as a Governance Capability](https://arxiv.org/abs/2605.16549v1)、v1、2026-05-15提出、[全文](https://arxiv.org/pdf/2605.16549v1) | [日本語](pqc-discovery-governance.ja.md) / [English](pqc-discovery-governance.md) | 棚卸しから証拠・責任・時間上のリスク・供給者制約の管理へ。匿名ケーススタディの報告値と限界、現ラボとの対応、未実施の最小検証案を整理 |

論文の式・Wave区分を本ラボの採点へ採用したわけではありません。原文全文は版固定リンクで参照し、公開リポジトリには独自の要約・レビューを保存します。以下の規格確認日は従来の記録のままです。

## Google Cloud記事とGemini Notebook（2026-10-18確認）

| 資料 | 保存したノート | このプロジェクトとの関係 |
|---|---|---|
| [Cloud CISO Perspectives: New Gemini Notebook can help CISOs and policymakers prepare for PQC](https://cloud.google.com/blog/products/identity-security/cloud-ciso-perspectives-new-gemini-notebook-can-help-cisos-policymakers-prepare-for-pqc)、Stephanie Kiel、2026-10-14公開 | [日本語](gemini-pqc-notebook-readiness.ja.md) / [English](gemini-pqc-notebook-readiness.md) | 記事の事実（ノートブックの説明、CISO向け4手順、Googleの2029年目標）と、棚卸し・優先度付け・説明資料への未実装の提案を分離。ノートブック本体は未確認 |

関連して確認した一次資料：[Googleの移行タイムライン](https://blog.google/innovation-and-ai/technology/safety-security/cryptography-migration-timeline/)（2026-03-25）、[RSA-2048の見積り](https://arxiv.org/abs/2505.15917)（概要のみ、arXiv v1）、[ECDLP-256の見積り](https://arxiv.org/abs/2603.28846)（概要のみ、arXiv v2）、[2025年のCISO向け記事](https://cloud.google.com/blog/products/identity-security/cloud-ciso-perspectives-prepare-early-for-PQC-resilient-cryptographic-threats)（2025-02-28）。2029年はGoogle自身の計画で、規格上の期限ではありません。

## CAMM評価研究（2026-10-15確認）

[Practical Evaluation of the Crypto-Agility Maturity Model](https://arxiv.org/abs/2604.12428v1)、v1、2026-04-14提出、[PDF](https://arxiv.org/pdf/2604.12428v1)。[ラボの改善案](camm-practical-evaluation.ja.md)と[論文サーベイ](https://github.com/moruku36/independent-cs-research-2026/blob/main/surveys/collection-v2/2026-camm-practical-evaluation.md)を参照。既存の独自スコアをCAMM成熟度へ変換せず、新機能・追試は未実施として扱います。

## 暗号解析の参考文献候補（2026-10-15記録、一次本文未確認）

[量子アニーリングとRSA整数分解の参考ノート](dwave-annealing-rsa-reference.ja.md)。[GIGAZINE記事](https://gigazine.net/news/20241015-rsa-encryption-quantum-computer/)が示す[公式PDF](http://cjc.ict.ac.cn/online/onlinepaper/wc-202458160402.pdf)は今回取得できず、本文・正式書誌・DOIは未確認。実用RSA-2048解読や量子優位の実証としては扱わず、実装・採点へ採用していません。

## 原文を読む前に

初めから規格全文を読む必要はありません。まず[用語の早見表](glossary.md)と
[学習ノート](security-specialist-notes.md)で、このツールに登場する用途を確認できます。

| 知りたいこと | 参照する資料 | このプロジェクトとの関係 |
|---|---|---|
| 共有秘密を作るPQCの方式は何か | FIPS 203 / SP 800-227 | ML-KEMを鍵確立の候補として紹介する背景 |
| 署名に使えるPQCの方式は何か | FIPS 204 / FIPS 205 | ML-DSA、SLH-DSAを署名の候補として紹介する背景 |
| 移行で何を考えるのか | IR 8547 | 既存方式と移行を整理するための資料。下記の確認版は草案 |
| 暗号を変更しやすくするには | CSWP 39upd1 | 設計・運用を含む変更能力を考える背景 |

FIPSは規格の文書、SPは指針等を扱う刊行物、IRは報告書、CSWPはホワイトペーパーの系列名です。
`Final`は確定版、`Initial Public Draft`は最初の公開草案です。
資料を参照したことと、本ツールが規格の認証を受けたことは異なります。

## 確認した版とリンク

| 資料 | 確認した版 | 適用 |
|---|---|---|
| [FIPS 203](https://csrc.nist.gov/pubs/fips/203/final) | 2024-08-13 Final | ML-KEMによる共有秘密の確立 |
| [FIPS 204](https://csrc.nist.gov/pubs/fips/204/final) | 2024-08-13 Final | ML-DSA署名 |
| [FIPS 205](https://csrc.nist.gov/pubs/fips/205/final) | 2024-08-13 Final | SLH-DSA署名 |
| [SP 800-227](https://csrc.nist.gov/pubs/sp/800/227/final) | 2025-09-18 Final | KEMの利用・実装上の考慮 |
| [IR 8547](https://csrc.nist.gov/pubs/ir/8547/ipd) | 2024-11-12 Initial Public Draft | PQC移行の検討。確定した義務・期限として扱わない |
| [CSWP 39upd1](https://csrc.nist.gov/pubs/cswp/39/upd1/considerations-for-achieving-crypto-agility/final) | 2026-06-29更新 Final | 暗号移行能力の設計。独自スコアはNIST認証ではない |

FIPS 203/204の公開ページにはerrata案の案内があります。実装導入時には最新版を再確認します。
本プロジェクトはPQCプリミティブを自作せず、用途に応じた移行候補を提示します。
