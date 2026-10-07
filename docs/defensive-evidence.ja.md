# 防御的インベントリ検証の証拠台帳

教育用インベントリとして扱います。既存の防御動作を回帰テストで確認し、scanner本体は変更していません。実行時使用、検出の網羅性、相互運用性、システム全体の耐量子安全性を保証しません。

| 主張 | テストまたは原本 | コマンド | 実測結果 | 限界 |
| --- | --- | --- | --- | --- |
| 合成canaryがJSON、Markdown、CSV、標準出力と標準エラーに出ない | `tests/test_defensive_boundaries.py::test_cli_content_canary_absent_from_all_exports` | `PYTHONPATH=src python -m pytest -q tests/test_defensive_boundaries.py` | 最終59件のsuiteに含めて成功 | JSON/Pythonの秘密値に似た内容と合成PEM本文。ファイル名は出力されるため秘密を含めない |
| JSON/Python/UTF-8不正、サイズ超過、打切りを部分結果として扱う | `test_partial_inventory_is_visible_and_csv_is_not_published`の5ケース | 同上 | JSONにissueまたはtruncation、MarkdownにPartial result YES。CSVはexit 1、新規出力なし、既存出力保持 | directory/reportのexit 0は完全性や安全性の証明ではない |
| MAX_BYTES境界とstat後の増加を制限 | exact maxとgrowth回帰テスト | 同上 | 1048576 bytesは受理、超過とstat後増加を拒否 | サイズ境界の確認であり全競合条件の証明ではない |
| ファイル識別子の変更を拒否 | fstat identityとreal replacement回帰テスト | 同上 | device/inode不一致の模擬試験と実際の一時ファイル置換を拒否 | 限定した介入点。同じinodeへの書込みに対するsnapshot整合性は未証明 |
| CSV数式接頭辞を文字列化し、手動評価欄を空欄にする | formula prefixとexport canary回帰テスト | 同上 | = + - @のパスがCSV再読込後も先頭apostrophe付き。空白付き接頭辞も関数で確認。手動欄は空 | 表計算ソフト上での実行試験ではない |
| 既存と新規テスト、静的検査を確認 | `evidence/defensive-local-verification.json` | 英語版の全テスト、ruff、mypyコマンド | 59 passed、lint exit 0、mypyは17 source filesでexit 0 | WSLローカル検証。Windows CI未実施 |

fixtureはすべて合成した一時ファイルです。追加モジュールはsocket.create_connectionを禁止し、既存TLSテストは不正引数またはmockを使用します。外部対象へのprobeは行っていません。追加回帰ケースは15件です。canary検査は選んだ内容経路に限り、任意の秘密、名前、あらゆるencodingの非漏洩を保証しません。静的なalgorithmラベルや空欄のreviewから配備状態を認定しません。

## 再現とリビジョン

基点commitは`b5f3b71c2ea528e68341e9cd595abc0794cb1660`、実装とテスト証拠のcommitは`51a8563fa102847fa2a129f183cf2a3672c78eca`です。いずれもこの変更はローカル限定で、続くcommitに文書を含めています。追加変更のCIは未実行で、以前のgreen CIを新しいテストの証拠にしていません。pushもmergeもしていません。

宣言された依存関係を隔離したWSL Ubuntu 24.04のPython 3.12環境で、各リポジトリのルートから実行しました。[実測記録](../evidence/defensive-local-verification.json)に正確なコマンド、出力、UTC日時、検証対象PythonファイルのSHA-256があります。`git log -2 --oneline`でローカル2commitを確認できます。実行モデルとeffortの設定は独立確認できず、Astra mediumで実行したとは主張しません。
