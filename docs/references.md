# References

確認日: 2026-09-15。公開ページで版と適用範囲を確認しました。
Phase 0では暗号アルゴリズムの評価はまだ実装していません。

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
