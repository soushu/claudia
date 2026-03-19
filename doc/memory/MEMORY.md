# Mazelan プロジェクト メモリ

## 概要
旅行特化AIチャットWebアプリ「Mazelan」。折りたたみUI + BYOK + マルチプロバイダー + tool use（商品検索・フライト検索）+ Web検索。
- 本番: https://mazelan.ai / ステージング: https://dev.mazelan.ai
- GCP: e2-small (bitpoint-bot, us-west1-b)
- ブランチ戦略・コーディングルール・デプロイ・環境構成 → `/CLAUDE.md`（厳守）

## 技術スタック
Frontend: Next.js 14 + Tailwind CSS 3.4 + next-intl / Backend: FastAPI + PostgreSQL + Alembic / 認証: NextAuth.js v4 / AI: Claude + GPT + Gemini / デプロイ: GitHub Actions + systemd + Nginx

## 仕様・実装
- [仕様書](spec.md) — API・DB・コンポーネント・機能一覧
- [実装詳細](implementation.md) — マルチモデル・Context Memory・テーマ・tool use等
- [ロードマップ](roadmap.md) — 完了STEP一覧・残タスク

## インフラ・デプロイ
- CI/CD認証: Workload Identity Federation（SA: `claudia-deploy@bitpoint-bot.iam.gserviceaccount.com`）
- Slack通知: Mazelan ステージング / Mazelan 本番（deploy.yml, deploy-staging.yml）
- デプロイスクリプト npm ci: `set +e` → 終了コードキャプチャ → `set -e` 方式

## セキュリティ
- [セキュリティ監査結果 2026-03-15](security_audit_2026_03_15.md) — 完了6項目+未対応10項目
- [セキュリティ追加対応（ローンチ後）](project_security_todo.md) — High3/Medium4/Low1

## フィードバック
- [DEV badge version numbering](feedback_dev_badge_version.md) — 整数=大きい変更、小数2桁=小さい修正
- [mainマージ時にメモリ更新](feedback_update_memory_on_main_merge.md)
- [developマージは--no-ff](feedback_no_ff_merge.md)
- [モデルパラメータはユーザーに触らせない](feedback_no_user_facing_model_params.md)
- [Nginxルート追加時は3箇所同期](feedback_nginx_route_sync.md)
- [mainマージは必ずユーザー指示を待つ](feedback_no_auto_main_merge.md)
- [npm ciデプロイ失敗時の対処](feedback_npm_lock_sync.md)
- [ツール使用は明示的リクエスト時のみ](feedback_explicit_tool_use.md)

## 企画
- [Mazelan - 旅行特化AIツール](project_travel_pivot.md) — mazelan.ai稼働中
- [現在の作業状態](project_current_task.md) — 最新の進捗と残タスク（次回開始時はここから）

## 検討中
- [ユーザー単位の無料枠使用量制御](project_user_quota.md) — ローンチ後にユーザー数を見て判断

## 既知の注意点（CLAUDE.md に記載のないもの）

### 認証・セッション
- cookie名: `__Secure-next-auth.session-token` を明示指定必要
- NEXT_PUBLIC_BACKEND_URL: ドメイン変更時はリビルド必要（ビルド時埋め込み）

### Nginx
- /chat/ はフロントと衝突 → バックエンドAPIは正規表現 `/chat/{uuid}` でマッチ
- sites-enabledはコピー → sites-available変更時はコピー必要

### 依存関係
- passlib/bcrypt互換性: bcrypt<4.1にダウングレード必要

### Gemini
- フリーキープール: `GEMINI_FREE_KEYS` env var。現在pool-4,5の2キー運用
- キーチェーン: ユーザーキー → フリープール → 有料フォールバック
- 503 UNAVAILABLE: リトライ対象に追加済み
- **google_searchとfunction_callingは同一リクエストで併用不可** → 動的切り替えで対応（providers.py）

### SerpAPI / Tool Use
- Amazon検索・フライト検索: SerpAPI経由。`SERPAPI_KEY` env var
- **無料枠: 250回/月（2026-03-18時点で使い切り、4月1日リセット）**
- 有料化時はSearchApi.io（$40/月・10,000回）に移行予定
- **キャッシュ**: serpapi_cache.py でインメモリTTLキャッシュ（フライト3h、Amazon 1h）
- **Web検索フォールバック**: SerpAPIエラー時にgoogle_searchで代替（不正確な場合あり→注意書き付き）
- 議論モードでは `disable_tools=True` で無効化

### Web検索
- **Claude**: built-in web_search（全モデル有効、SerpAPIツールと併用可能）
- **Gemini**: Google Search Grounding（function_callingとは同時不可→動的切替）
- **GPT**: Web検索機能なし（API版には未提供）

### フライト検索アーキテクチャ
- ツール1回呼び出しで完結（departure_month + day range + trip_weeks）
- SerpAPI消費: ~11回/検索（キャッシュヒット時は0回）
- 各フライトに3リンク: 航空会社公式サイト(70+社)、Google Flights確認、Aviasales価格比較

### UI
- ツール実行ステータス表示: 「🔍 フライト検索中...」「🧠 考え中...」「次のステップを準備中...」
- 長URL防御: 500文字超は[リンク省略]に置換（フロント+バックエンド両方）
- 入力欄オートフォーカス: セッション切替時

### 外部サービス
- Travelpayouts: サイト認証Active。アフィリエイトID: 508503
- SerpAPI: 無料枠250回/月。キャッシュ+Web検索フォールバック導入済み
