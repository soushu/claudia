---
name: セキュリティ監査結果 2026-03-15
description: 包括的セキュリティ監査の全結果。完了済み4項目+追加推奨10項目（Critical/High/Medium/Low）
type: project
---

# セキュリティ監査結果 (2026-03-15)

## 完了済み

| # | 項目 | 重要度 | 対応内容 |
|---|------|--------|----------|
| 1 | CSRF保護 | Medium | NextAuth cookieにSameSite=Lax, httpOnly, Secure(本番)を明示設定 |
| 2 | レートリミット | High | slowapi導入: login(5/min), register(3/min), chat(20/min), debate(10/min) |
| 3 | 依存バージョン固定 | Low | requirements.txt全パッケージを本番pip freezeで正確に固定 |
| 4 | エラーハンドリング | Medium | main.pyグローバル例外ハンドラー(ValidationError→汎用, 未処理→ログ+500) |
| 5 | upsert-user認証 | High | X-Internal-API-Key必須（以前に対応済み） |
| 6 | chat.pyエラー汎用化 | Medium | 内部詳細を返さないように修正（以前に対応済み） |

## 未対応 — 追加推奨

### 🔴 Critical
| # | 項目 | リスク | 対応方法 |
|---|------|--------|----------|
| C1 | HTTPセキュリティヘッダー未設定 | クリックジャッキング、XSS、MIMEスニッフィング | Nginxに以下を追加: `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, `Strict-Transport-Security: max-age=31536000`, `Content-Security-Policy: default-src 'self'...`, `Referrer-Policy: strict-origin-when-cross-origin` |
| C2 | 画像base64サイズ制限なし | 巨大画像でメモリ枯渇→OOM→DoS | バックエンドでbase64データサイズを検証（例: 10MB上限）。chat.py, debate.pyの両方 |

### 🟠 High
| # | 項目 | リスク | 対応方法 |
|---|------|--------|----------|
| H1 | APIキーをlocalStorageに保存 | XSS脆弱性があれば即漏洩 | 理想はサーバーサイド暗号化保存+httpOnly cookie。ただしBYOKの性質上、完全な解決は難しい。CSPヘッダー(C1)で緩和が現実的 |
| H2 | upsert-userにレート制限なし | ブルートフォース可能 | slowapiで `@limiter.limit("5/minute")` 追加 |
| H3 | INTERNAL_API_KEYの強度未検証 | 弱いキーだと推測可能 | 本番で十分な長さ(32文字以上)のランダム文字列を使用しているか確認 |

### 🟡 Medium
| # | 項目 | リスク | 対応方法 |
|---|------|--------|----------|
| M1 | ストリーミングタイムアウトなし | 接続が永遠にハング→リソース枯渇 | stream_chat/stream_debateにタイムアウト設定（例: 5分） |
| M2 | リクエストボディサイズ制限なし | 大きなペイロードでメモリ問題 | Nginx `client_max_body_size 20m;` 設定 |
| M3 | base64画像がDBに直接保存 | DB肥大化、バックアップ遅延 | 長期的にはS3/GCS等のオブジェクトストレージ移行を検討 |
| M4 | deploy/setup.shにDBパスワード | ソースコードにシークレット | プレースホルダー化 `DB_PASSWORD=changeme` |

### 🟢 Low
| # | 項目 | リスク | 対応方法 |
|---|------|--------|----------|
| L1 | deployスクリプトに個人情報 | ユーザー名等がソースに | プレースホルダー化 |
| L2 | CORS設定の確認 | 不適切なオリジン許可 | 本番で許可オリジンが正しいか定期確認 |
| L3 | セッションID列挙 | UUIDだが理論上推測可能 | 既に認可チェック(user_id一致)があるため実害は低い |

## 対応順序（inside-outアプローチ）

OWASP・Acunetix等の共通見解: アプリ本体の脆弱性を先に潰し、Nginxヘッダーは防御の追加レイヤーとして後からバッチ適用。
**Why:** Nginxヘッダーはブラウザ挙動の制御(defense-in-depth)でありアプリ本体の脆弱性は防げない。CSPは設定ミスでフロントが壊れるリスクがあり安定後に設定すべき。Nginx変更はまとめて1回のreloadで適用する方が効率的。

| 順 | タスク | 種別 | 状態 |
|----|--------|------|------|
| 1 | **C2** 画像base64サイズ制限 | コード変更 | ✅ 完了 |
| 2 | **H2** upsert-userレート制限 | コード変更 | ✅ 完了 |
| 3 | **M1** ストリーミングタイムアウト | コード変更 | ✅ 完了 |
| 4 | **M4** setup.shプレースホルダー化 | コード変更 | ✅ 完了 |
| 5 | **C1+M2** HTTPヘッダー+ボディサイズ制限 | Nginx適用済み | ✅ 完了（本番・ステージング両方適用確認済み） |

## 備考
- GitHubリポジトリ公開自体は問題なし（.envはgitignore済み、git履歴にもシークレットなし）
- H1(localStorage APIキー)は、BYOK方式の性質上完全な解決は難しい。CSPヘッダーでXSSリスクを下げるのが現実的
- 本監査はコードレビューベース。ペネトレーションテストは別途実施推奨
