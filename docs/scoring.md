# Crypto Agility scoring rubric

これは独自の「確認できた静的根拠＋運用側が申告した成熟度」の点数です。
実測の安全性、PQC準拠、NISTの公式スコアではありません。

## 計算

10項目×最大10点。合計は各項目の単純和で0〜100点です。
UNKNOWNの0点は根拠不足であり、「能力がない」という判定ではありません。
合計と一緒にassessed_items/10・declared_items・partial_inventoryを確認します。
同じ対象範囲・根拠の質でなければ、他プロジェクトと単純比較できません。

| 根拠 | 点 | 出力 |
|---|---:|---|
| 根拠なし、またはunknown申告 | 0 | UNKNOWN |
| absent申告 | 0 | DECLARED（運用側の申告） |
| documented申告＋読取対象内の証拠ファイル | 5 | DECLARED |
| tested申告＋読取対象内の証拠ファイル | 10 | DECLARED。テスト内容は本ツールでは実行・検証しない |
| 設定の暗号選択またはPython暗号API利用を検出 | 該当項目に5 | STATIC_EVIDENCE。稼働状態・保守性は未検証 |
| 明示的なPython暗号API呼び出しを検出 | hard_coded_algorithmsを0 | STATIC_EVIDENCE。肯定的申告より優先。ラッパー内部の呼出しの可能性は人が確認 |

自動評価はhard_coded_algorithms、cryptographic_library_dependency、
configuration_driven_selectionだけです。他の項目をキーワード一致で推定しません。

## 10項目

| 識別子 | 確認したい能力 |
|---|---|
| hard_coded_algorithms | 呼出し元が固定アルゴリズムに依存せず切替可能か |
| algorithm_abstraction | 暗号プロバイダ/APIの抽象化 |
| centralized_key_management | KMS/HSM、鍵の所有・アクセス管理 |
| certificate_automation | 証明書の発行・配布の自動化 |
| key_rotation | 鍵更新、重複期間、廃止と復旧 |
| cryptographic_library_dependency | 暗号ライブラリ依存と保守計画 |
| protocol_negotiation | 認証された交渉、ダウングレード耐性 |
| configuration_driven_selection | ポリシー検証付きの設定選択 |
| certificate_lifecycle_automation | 更新、期限監視、失効の運用 |
| upgradeability | 互換性試験とロールバックを伴う移行 |

## 任意の運用根拠ファイル

対象ルート直下に`.pqc-agility.json`を置けます。省略すると自動評価のみです。

```json
{
  "version": 1,
  "criteria": {
    "key_rotation": {
      "level": "documented",
      "evidence": ["rotation-plan.txt"]
    }
  }
}
```

levelはunknown/absent/documented/tested。未対応の項目・スキーマはエラーにします。
documented/testedには1〜20個の根拠パスが必要です。スキャンで正常に読み取った
相対パスのみを許可し、対象外・秘密鍵ファイル・manifest自身は拒否します。
ファイルの存在を確認するだけで、その記述の真実性は保証しません。
根拠として扱う運用文書は対応する.txt/.json等で用意してください。
合成サンプルは「設計の記載」の申告であり、本番運用や試験成功を主張しません。

設計上の背景: [NIST CSWP 39upd1](https://csrc.nist.gov/pubs/cswp/39/upd1/considerations-for-achieving-crypto-agility/final)。
