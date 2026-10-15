# 調査用参考文献候補：量子アニーリングとRSA整数分解

**状態：記事経由の参考文献候補。一次論文本文未読・書誌未確定・追試未実施。確認日：2026-10-15 UTC。**

[GIGAZINEの記事](https://gigazine.net/news/20241015-rsa-encryption-quantum-computer/)（2024-10-15）が紹介する「基于 D-Wave Advantage 的量子退火公钥密码攻击算法研究」を、今後の暗号解析・PQC調査用の候補として記録する。一次論文への導線は、記事に掲載された[学術誌サイトの公式PDF](http://cjc.ict.ac.cn/online/onlinepaper/wc-202458160402.pdf)。今回は取得できず、本文は読めていない。

記事が紹介する著者は上海大学のワン・チャオ氏ら、掲載先はChinese Journal of Computers。正式な著者一覧・刊行年・巻号・ページ・DOI・対象版は一次資料で確認できていないため、確定書誌として採録しない。

## 取り扱い

記事は量子アニーリングによる22ビット、古典計算との組合せによる50ビットの整数分解を紹介している。これは記事の報告範囲であり、本ラボで確認・再現した実験結果ではない。実用RSA-2048の解読実証、実用規模へのスケーリングや量子優位の証明として扱わない。Shor法によるゲート型量子計算の実証とも区別する。

この参考文献を追加しても、現在の[判定・採点](scoring.md)、移行優先度、CLI、暗号方式の対応範囲は変えない。記事の見出しから新しい危険度や期限を自動設定しない。[CAMM評価ノート](camm-practical-evaluation.ja.md)とは別の参考資料である。

## 次に確認すること（未実施）

- 公式本文の書誌情報と版を照合し、記事由来の説明と分けて記録する。
- 実験条件、古典前処理、比較対象、全処理時間、成功率、量子資源の数え方を確認する。
- 棚卸し結果と接続する場合も、暗号用途・データ保持期間・供給者の移行計画を別の根拠として確認する。論文の未確認情報で既存スコアを変えない。

## English

News-derived reference candidate; primary full text and formal bibliography remain unverified. No implementation, reproduction or scoring change. Small-instance factoring is not treated as practical RSA-2048 decryption or proof of quantum advantage.

[出典索引](references.md) | [日本語README](../README.ja.md)
