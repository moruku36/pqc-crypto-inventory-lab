# PQC Crypto Inventory Lab

暗号資産の棚卸しとPQC移行評価を学ぶための、小規模なPython CLIです。

## 実装状況

Phase 0–5: CLI・CI・TLS・棚卸し・移行レポート・採点・支援士学習ノートを実装。

### 現在の検証状況（2026-09-15）

- 専用Privateリポジトリ: https://github.com/moruku36/pqc-crypto-inventory-lab
- Codespaces内でpytest 3件、Ruff、mypy、CLI起動が成功。
- Windowsからの依存取得はTLSエラー。利用者の許可により検証・commit・pushを
  Codespacesへ移行。ここでいうローカルテストはクラウド開発環境内のテストです。
- 起動に空でないブランチが必要なため、READMEのみのbootstrap commitを先行。
- CI結果と各Phaseのcommitは最終IMPLEMENTATION_SUMMARY.mdに記録します。

## 開発環境

Python 3.11以上。

```sh
python -m venv .venv
# Windows: .venv\Scripts\activate
# POSIX: source .venv/bin/activate
python -m pip install -e ".[dev]"
pqc-scan --help
pqc-scan --version
python -m pytest -q
python -m ruff check .
python -m mypy
```

## 実装手順

各Phaseは実装、ローカルテスト、差分レビュー、文書更新、commit、push、
remote・branch・commit・working tree・反映確認、完了報告の順で進めます。

0. 初期構成
1. 公開TLSハンドシェイク情報の取得
2. 明示指定ディレクトリの暗号棚卸し
3. Markdown移行レポート
4. 根拠を示すCrypto Agility採点
5. 情報処理安全確保支援士の学習ノート

## 安全性

学習用であり、包括的な暗号監査や安全性の証明ではありません。
将来のスキャナーは取得できない情報をUNKNOWNとし、秘密鍵本文・トークン・
認証情報を出力しません。TLS取得は通常の公開ハンドシェイクに限定します。
ローカルレポートは機微なパスを含み得るため、reports/はGit対象外です。

[設計](docs/architecture.md) · [参照資料](docs/references.md)

## TLSスキャン（Phase 1）

```sh
pqc-scan tls github.com --timeout 5
pqc-scan tls example.com --port 443
```

JSONでTLSバージョン、暗号スイート、証明書の署名・公開鍵・鍵長・有効期限、
取得可能な鍵交換ファミリーと理由を返します。TLS 1.3の鍵交換グループは
Python sslが公開しないためUNKNOWNです。接続は証明書の名前・信頼・期限を検証します。
失敗時は標準エラーに構造化JSONを出して終了コード1、引数エラーは2です。
DNS解決にはOS側の待ち時間があり、`--timeout`は全処理の厳密な上限ではありません。

SAFEは限定的なアルゴリズム評価で、システム全体の安全性を示しません。
SHA-1の古典的な弱点と量子脆弱性は区別します。CRL/OCSP検証は行いません。
実行例は`samples/tls-github.json`。ライブ値は実行日時・経路で変化します。
Phase 1検証: pytest 16件、Ruff、mypy成功。

## ディレクトリ棚卸し（Phase 2）

```sh
pqc-scan directory ./samples/project
pqc-scan directory ./project --max-files 5000
```

Pythonの暗号ライブラリAPI呼び出しをASTで解析し、設定のalgorithm/cipher/hash等の
既知キー、PEM・DER証明書、PEM/SSH公開鍵を解析します。RSA、ECDSA、ECDH、
Ed25519、X25519、SHA-1/256/384/512、AESを対象とします。
文字列・コメントにアルゴリズム名があるだけでは検出しません。
秘密鍵はヘッダーの存在のみを記録し、鍵のデコードや本文出力は行いません。

最大1 MiB/ファイル、最大10,000ファイル。シンボリックリンク・.git・仮想環境・
node_modules・reportsを除外します。.env等も除外し、読み取れないファイルはissuesに
固定理由を記録します。件数制限ではtruncated=trueを返します。
ファイル更新を止めた静的ディレクトリで実行してください。

相対パス自体は出力されます。共有前に機微なファイル名がないか確認してください。
検出ゼロは暗号不使用の証明ではありません。依存設定やPython以外のソースを含む
全言語・全形式の解析は未対応です。例: `samples/directory.json`。
Phase 2検証: pytest 21件、Ruff、mypy成功。

## 移行レポート（Phase 3）

```sh
pqc-scan report ./samples/project
pqc-scan report ./project --output reports/project-review.md
```

必須9章を含むMarkdownを生成します。既存ファイルは上書きしません。
`reports/`の既定出力はGit対象外。共有用の合成例は`samples/crypto_inventory.md`です。
P1はSHA-1用途・鍵保管の確認、P2は量子脆弱な公開鍵方式の用途・保持期間の調査、
P3はパラメータ等の確認という独自のトリアージです。NISTの義務・期限ではありません。
PQC候補は用途別の検討案で、ライブラリ・PKI・プロトコル対応の検証が必要です。
Phase 3検証: pytest 26件、Ruff、mypy成功。Phase 0–2のGitHub Actionsも成功確認済み。

## Crypto Agility Score（Phase 4）

```sh
pqc-scan score ./samples/project
```

10項目の点数・理由・根拠・改善案をJSONで出力し、reportにも組み込みます。
[採点基準とmanifest仕様](docs/scoring.md)を参照してください。
UNKNOWNは未評価、DECLAREDは運用側の申告で、実行検証済みという意味ではありません。
サンプルは25/100（静的根拠10点＋設計の申告15点）で、本番の成熟度評価ではありません。
出力例は`samples/score.json`と`samples/crypto_inventory_scored.md`。
Phase 4検証: pytest 35件、Ruff、mypy成功。

## 支援士学習ノート（Phase 5）

[セキュリティ技術と実装の対応](docs/security-specialist-notes.md)に、公開鍵・共通鍵・
ハイブリッド暗号、RSA/ECC、PKI/X.509、TLS、署名・ハッシュ・鍵交換・証明書、
CRL/OCSP、暗号移行、Crypto Agility、PQCを整理しました。
各項目に試験ポイント・実装箇所・実務用途・間違えやすい点を記載しています。
