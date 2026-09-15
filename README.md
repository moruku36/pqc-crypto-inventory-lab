# PQC Crypto Inventory Lab

暗号資産の棚卸しとPQC移行評価を学ぶための、小規模なPython CLIです。

## 実装状況

Phase 0: CLI雛形・pytest・lint・型検査・CI設定を実装。
TLSスキャン以降の機能は、Phase 0のpush成功確認後に順次実装します。

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
