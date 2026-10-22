# PQC Crypto Inventory Lab

[English](README.md) | 日本語

指定したローカルファイルと、許可を得た TLS 接続先の暗号利用について手掛かりを集める学習用ツールです。耐量子暗号（PQC）への移行で何を追加調査するかを整理します。システムの「量子安全」を認定するものではありません。

![明示した入力から静的検出とレポートまでのデータフロー](docs/images/architecture-overview.svg)

## 付属サンプルを試す

Python 3.11 以上が必要です。リポジトリのルートで実行します。

```sh
python -m venv .venv
# 利用するシェルの手順で .venv を有効にします。
python -m pip install -e ".[dev]"
pqc-scan directory ./samples/project
pqc-scan score ./samples/project
pqc-scan report ./samples/project --output reports/first-review.md
```

最初のコマンドは JSON を表示します。`path` と `line` は根拠の場所、`kind` は検出方法、`value`・`status`・`confidence`・`reason` は限定的な方式の評価です。サンプルは 5 件を検出し、スコアは 25/100 点です。安全性の割合ではありません。レポートは新規ファイルに保存し、上書きしません。[結果の読み方](docs/reading-results.md)と[採点基準](docs/scoring.md)を参照してください。

## 現在できること

| コマンド | 入力 | 出力と範囲 |
|---|---|---|
| `directory PATH` | 明示したローカルディレクトリ | Python の一部の暗号 API、既知の設定キー、公開鍵、X.509 証明書、秘密鍵の存在の静的な手掛かりを JSON に出力 |
| `score PATH` | 同じディレクトリと任意の `.pqc-agility.json` | 10 項目の根拠・申告の点数。申告内容は独立検証しません |
| `report PATH --output FILE` | 同じディレクトリ | 棚卸しと調査の問いを Markdown に保存。新規ファイルのみ |
| `review PATH --output FILE` | 完全なディレクトリ棚卸し | 人が確認するための空欄付き CSV。不完全な結果では出力を拒否 |
| `compare BEFORE AFTER` | 2 つのディレクトリ | 静的な根拠の差分。配備の確認ではありません |
| `tls HOST` | 明示的に許可された TLS ホスト | 証明書を検証する 1 回の接続と JSON 観測結果。広域探索はしません |

オプションは `pqc-scan --help` を参照してください。[操作ガイド](docs/getting-started.md)、[構成とデータフロー](docs/architecture.md)、[合成サンプル](samples/README.md)から詳細へ進めます。

## 結果と安全な範囲

`QUANTUM_VULNERABLE` は追加調査が必要な古典的公開鍵方式です。`SAFE` は限定的な方式レベルのラベルであり、パラメータ・実装・プロトコル・鍵管理・配備の安全性を保証しません。`UNKNOWN` は根拠不足です。検出ゼロも暗号不使用の証明ではありません。P1～P3 とアジリティ採点は本プロジェクト独自の目安で、NIST の評価や期限ではありません。

ディレクトリは利用者が明示指定した範囲だけを、サイズと件数の制限付きで読みます。サンプルコードの実行や秘密鍵のデコードはしませんが、秘密鍵ヘッダーを識別するためファイルのバイト列を読む場合があります。許可なく実際の秘密情報を含む場所へ向けないでください。相対パス名自体が機微情報になり得ます。生成する `reports/` は Git 追跡対象外ですが、共有前に内容を確認してください。学習には `samples/project` または `samples/mini-service` を使えます。`tls` は対象の許可を得てから使用してください。証明書ストアの収集、広域ネットワーク走査、本番移行は対象外です。

## 計画と資料

[実装状況と今後の計画](docs/roadmap.md)で、実装済み・今回の変更・判断待ちを分けています。[オフライン確認演習](docs/offline-review-exercise.md)と[性能証拠台帳](docs/performance-evidence.md)は合成・不明の値を用い、実環境の測定結果ではありません。[PQC discovery](docs/pqc-discovery-governance.ja.md)、[CAMM](docs/camm-practical-evaluation.ja.md)、[Google の PQC Notebook](docs/gemini-pqc-notebook-readiness.ja.md)などの研究ノートは[出典索引](docs/references.md)から読めます。過去の各 Phase と検証記録は[実装サマリー](IMPLEMENTATION_SUMMARY.md)に残しています。

NIST の確定した規格は [FIPS 203（ML-KEM）](https://csrc.nist.gov/pubs/fips/203/final)、[FIPS 204（ML-DSA）](https://csrc.nist.gov/pubs/fips/204/final)、[FIPS 205（SLH-DSA）](https://csrc.nist.gov/pubs/fips/205/final)です。本ツールは一部の名称を認識するだけで、これらの暗号方式の実装・検証はしません。[セキュリティ方針](SECURITY.md)と[貢献ガイド](CONTRIBUTING.md)も参照してください。
