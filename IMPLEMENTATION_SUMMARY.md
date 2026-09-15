# Implementation Summary

## この文書の読み方

この文書は「何を作り、どこまで動作確認したか」の記録です。
初めて使う場合は[操作ガイド](docs/getting-started.md)、結果の意味は[結果の読み方](docs/reading-results.md)から確認できます。

短くまとめると、暗号を見つける機能、見直し候補をまとめる機能、変更の準備状況を採点する機能を作りました。
テスト成功は、確認対象の処理が期待どおり動いたという意味です。あらゆる暗号利用を漏れなく検出する保証ではありません。
以下のPhaseは開発を分けた段階で、利用者がこの順に実装し直す必要はありません。

2026-09-16追記：READMEと各文書に、初回操作・出力項目・採点内訳・処理の流れ・用語の説明を追加しました。
以下の実装時の検証結果とGit履歴は、2026-09-15の記録として残しています。

検証日: 2026-09-15。Repository: https://github.com/moruku36/pqc-crypto-inventory-lab
Private / main。ユーザー承認によりCodespaces内でテスト・commit・pushを実施しました。
Windowsからのgit pushは実施していません。

## Implemented Features

- `tls`: 証明書検証付きの通常TLSハンドシェイク1回。TLS・スイート・証明書署名・公開鍵・鍵長・期限・取得可能な鍵交換を出力。
- `directory`: 指定ルートのPython AST、設定キー、PEM/DER証明書、PEM/SSH公開鍵を解析。
- `report`: 必須9章のMarkdown。用途別PQC候補、優先度、限界、参照資料を記載。
- `score`: 10項目×10点。理由・証拠・改善案、UNKNOWNと静的根拠と運用申告を区別。
- 支援士学習ノート: 16テーマに試験ポイント・実装・実務・注意点を記載。

## Repository Structure

```text
src/pqc_inventory/
  cli.py                 CLIと構造化エラー
  classification.py      保守的な量子リスク分類
  tls_scanner.py          TLS/X.509情報取得
  directory_scanner.py    読取境界・制限・静的解析
  scoring.py             明示的な採点規則
  report.py              Markdown生成と出力保護
tests/                   オフライン単体・回帰テスト
docs/                    設計・一次資料・採点基準・学習ノート
samples/                 公開TLS出力・合成ソース・JSON/Markdown例
reports/                 利用者の出力先（Git対象外）
.github/workflows/ci.yml  Python 3.11/3.13のCI
```

## Test Results

Codespaces Python 3.14.2で実行。全37テスト成功、Ruff成功、mypyは12ファイルで問題なし。

| 検証 | 結果 |
|---|---|
| CLI help/version | 成功、0.1.0 |
| 公開TLS: github.com:443 | 成功、TLSv1.3 / TLS_AES_128_GCM_SHA256 |
| TLS 1.3鍵交換 | UNKNOWN（Python sslの公開情報から取得不可） |
| samples/project棚卸し | 5 findings、truncated=false |
| サンプル採点 | 25/100、評価6/10項目、申告3項目 |
| 採点付きレポート生成 | 成功、全9章 |
| 秘密本文の非出力・範囲制限・上書き防止・エラー無害化 | 回帰テスト成功 |

確認環境: cryptography 48.0.1 / pytest 9.1.1 / Ruff 0.16.7 / mypy 1.20.2。
依存はpyproject.tomlで範囲指定しており、完全なビット単位再現や依存固定は保証しません。
ライブTLS結果は取得時点の観測で、全対応方式や将来の状態を示しません。

## CI Results

各runはPython 3.11と3.13でpytest・Ruff・mypy・CLIを実行します。

| 対象 | 結果 | Run |
|---|---|---|
| Phase 0 | success | [34969798389](https://github.com/moruku36/pqc-crypto-inventory-lab/actions/runs/34969798389) |
| Phase 1 | success | [34970187041](https://github.com/moruku36/pqc-crypto-inventory-lab/actions/runs/34970187041) |
| Phase 2 | success | [34970723824](https://github.com/moruku36/pqc-crypto-inventory-lab/actions/runs/34970723824) |
| Phase 3 | success | [34971124815](https://github.com/moruku36/pqc-crypto-inventory-lab/actions/runs/34971124815) |
| Phase 4 | success | [34971637946](https://github.com/moruku36/pqc-crypto-inventory-lab/actions/runs/34971637946) |
| Phase 5 | success | [34971927648](https://github.com/moruku36/pqc-crypto-inventory-lab/actions/runs/34971927648) |
| Final code review | success | [34972259588](https://github.com/moruku36/pqc-crypto-inventory-lab/actions/runs/34972259588) |

このサマリーを含む最終commitのCIはpush後に確認し、完了報告で結果を示します。

## Example Commands

```sh
python -m pip install -e '.[dev]'
python -m pytest -q
python -m ruff check .
python -m mypy
pqc-scan tls github.com
pqc-scan directory ./samples/project
pqc-scan score ./samples/project
pqc-scan report ./samples/project --output reports/crypto_inventory.md
```

既存レポートは上書きしません。再実行時は別の出力名を指定してください。

## Security Considerations

通常TLS情報の取得と明示指定ルートの静的解析だけを実施します。
秘密鍵の本文・トークン・ソース断片を出力せず、秘密鍵の解析/復号はしません。
相対パスは出力に含まれるため共有前に確認してください。
ファイルサイズ・件数制限、リンク/特殊ファイル除外、構造化した固定エラーを実装。
証明書検証や管理端末の制限を無効化せず、許可されたクラウドで作業しました。

## Known Limitations

- 静的検出は実稼働・用途・全資産の存在/不在を証明しない。Python以外のコードと依存定義の網羅解析は未対応。
- 動的呼出し・alias再代入は未追跡。秘密鍵は存在のみ、未対応の証明書署名OIDはUNKNOWN。
- TLSはleaf中心。全チェーン棚卸し、CRL/OCSP、全スイート探索、TLS 1.3交渉グループ取得は未対応。
- DNSの待ち時間はsocket timeoutの外。敵対的な同時ディレクトリ差替えは対象外。
- SAFEは限定的な方式評価。スコアのDECLAREDは申告であり、証拠内容や運用試験を自動検証しない。
- 証明書自動化等の運用能力は自動推測しない。NIST準拠・認証の判定ツールではない。

## Problems Encountered

1. WindowsでPython配布元へのTLS接続失敗。利用者がローカルpush制限を申告し、Codespaces利用を承認。
2. CLIのCodespaces権限不足は利用者のOAuth承認で解消。
3. 空ブランチではCodespacesを作れないため、READMEのみのbootstrap commitをGitHub上で先行作成。
4. SSHの非ログインシェルでは標準認証環境がなくpush失敗。ログインシェルで解消し、次Phaseへ進む前にpushを確認。
5. 実装中の行長・型検査指摘を各Phase内で修正。最終レビューでTLS未知方式と既知の方式表示を補強。
6. RFC 8446の後継案内は確認したが、後継本文は取得制限で未確認。最新TLS規格への完全準拠は主張しない。

## Future Improvements

依存ロック・SBOM、言語別解析、用途/所有者/保存期間のモデル化、認可された運用証拠の検証、
TLSグループ取得API、証明書チェーン/失効評価、対象環境でのPQC互換性試験を検討。

## NIST PQC Mapping

FIPS 203 → ML-KEM（鍵確立）、FIPS 204 → ML-DSA（署名）、FIPS 205 → SLH-DSA（署名）。
SP 800-227 → KEMの安全な利用、IR 8547 → 移行検討（確認版は草案）、
CSWP 39upd1 → 暗号変更能力の設計背景。規格の実装や暗号モジュール認証は行っていません。
版・直接リンクは[references.md](docs/references.md)、独自採点は[scoring.md](docs/scoring.md)。

## Security Specialist Exam Mapping

TLS証明書解析でPKI/署名/鍵共有の違い、棚卸しで暗号用途・SHA-1の既存リスク、
レポートで段階移行・保管期間、採点で鍵管理・証明書運用・切戻しを学習できます。
[全16テーマのノート](docs/security-specialist-notes.md)は単なる用語集でなく実装との対応を示します。

## Git History

| 区分 | Commit |
|---|---|
| Cloud bootstrap | `7c30eee08587219fbbc6b6252898139d2a921b78` |
| Phase 0 | `757e6c60172ba7023bbb37cd842c4c4e009912bd` |
| Phase 1 | `3460ea3cf08257ba439a9277a738a5dc1f6e03b9` |
| Phase 2 | `93e004efae78cf38512c941bdfcdf20f4336a08e` |
| Phase 3 | `5a4e60b08a77b831b50230b0bd2acd1f4d4633be` |
| Phase 4 | `71d8f5daac770cfe402014b40fed48a45caa39ce` |
| Phase 5 | `8299c46f4210b9a49b856ab0b65d588d542aed41` |
| Final code review | `8207da10696a62627e86a6dd02f961557fb9d0f8` |

各Phaseを個別commit/pushし、その都度origin、main、HEAD、clean状態、remote SHA一致を確認。
最終文書commitのSHAは自己参照を避けて本文に埋め込まず、Git履歴と完了報告で示します。
