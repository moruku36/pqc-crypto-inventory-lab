# References

確認日: 2026-09-15。公開ページで版と適用範囲を確認しました。
以下は実装時に確認した資料の記録です。

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
