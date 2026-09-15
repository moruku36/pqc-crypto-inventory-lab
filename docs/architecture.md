# Architecture

## Phase 0

`src/pqc_inventory/cli.py`がargparseによるCLI入口です。
Phase 1からX.509解析にcryptographyを使用します。pytest、Ruff、mypyは開発用途です。
CIはPython 3.11および3.13で同じ検査を実行します。

## 後続Phaseの設計方針

TLS取得、ローカル解析、レポート、採点を独立したモジュールに分けます。
ネットワーク取得と判定を分離し、オフラインの単体テストを可能にします。
判定は観測値と理由を保持し、プロトコル名だけから鍵交換方式を推測しません。
ローカル解析は指定ルートに限定し、リンク追跡と生の内容出力を避けます。
採点は観測不足と低評価を区別し、基準・証拠・限界を公開します。

## TLS

`tls_scanner.py`: 標準ssl/socketで接続し、cryptographyでleaf証明書を解析。
公開鍵のEC符号化だけでは署名と鍵共有を区別できないため、表示はECCとします。
`classification.py`: アルゴリズム評価と判定理由。通信・出力から独立。
TLS 1.2のECDHE/DHEはスイートが示すファミリーのみ、グループは取得しません。
TLS 1.3のスイートは鍵交換を表さないためUNKNOWNです。
