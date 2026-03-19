# 実装詳細メモ

## 本番障害: STEP22デプロイ後バックエンド停止 (2026-03-12)
- **症状**: 履歴表示不可 + 返信不可（全API 502）
- **原因**: `pip install` がシステムpipで実行され、venvに `openai`/`google-genai` が入らず `ModuleNotFoundError` でuvicornが起動失敗。さらに再起動時に `google` 名前空間パッケージ競合で `ImportError: cannot import name 'genai' from 'google'` 発生（再度restartで解消）
- **修正**: `venv/bin/pip install openai google-genai` → `sudo systemctl restart claudia-backend` で復旧
- **再発防止**: デプロイコマンドを `venv/bin/pip install -r requirements.txt` に修正済み

## STEP22 マルチモデル対応 (2026-03-12)
### アーキテクチャ
- `backend/providers.py`: MODEL_REGISTRY + stream_anthropic/openai/google + stream_provider ディスパッチ
- APIキー: プロバイダー別にlocalStorage保存（`claudia_{provider}_api_key`）
- ヘッダー: `X-API-Key`（選択モデルのキー）+ `X-Anthropic-Key`（Context抽出用）
- メッセージ形式変換: Anthropic形式を基本とし、各プロバイダーに変換
  - OpenAI: image→image_url(data URI), system→messages先頭
  - Gemini: Content/Part型、user/model交互ルール（同一ロールマージ）
- Context抽出: 常にClaude Haiku、Anthropicキー未設定時はスキップ
- Web searchツール: Claude専用

### 注意点
- o3-mini: 画像非対応（自動ストリップ）、`max_completion_tokens`使用
- Gemini: 連続同一ロールメッセージは自動マージ必須
- google-genai v1.66+を使用（google-generativeaiは非推奨で警告が出る）

## STEP21 Context Memory
- DB: `contexts`テーブル — migration: `c3d4e5f6a7b8`
- 抽出: `backend/context_extractor.py` — Claude Haiku で fire-and-forget、ユーザー言語で保存
- カテゴリ: preferences, skills, projects, personal, general
- 重複排除: 双方向サブストリングマッチ
- 注入: `chat.py` で `<context_memory>` タグとしてシステムプロンプトに追記
- UI: `ContextModal.tsx` — カテゴリ別グループ、楽観的トグル更新、ボタンで保存（Enter無効）

## STEP20 システムプロンプト
- DB: `users.system_prompt`(Text) + `chat_sessions.system_prompt`(Text) — migration: `b2c3d4e5f6a7`
- API: `sessions/user/system-prompt` (GET/PUT) + `sessions/{id}/system-prompt` (GET/PUT)
- 優先順位: セッション別 > ユーザーグローバル > なし
- UI: `SystemPromptModal.tsx` — Global/Sessionタブ切替、複数指示の説明付き

## STEP15 テーマシステム
- CSS変数: `:root`(dark) / `.light-blue`(Sky Blue) / `.light-cyan`(Cyan)
- ThemeContext: `frontend/lib/themeContext.tsx` — 3テーマ cycle
- localStorage: `claudia-theme` キー
- Tailwindカラー: `bg-theme-*`, `text-t-*`, `border-border-*` セマンティックトークン
- コードブロック: dark=oneDark, light=coldarkCold

## STEP34 セキュリティ強化 (2026-03-15)
→ 詳細は [security_audit_2026_03_15.md](security_audit_2026_03_15.md) 参照

## STEP48 旅行API統合: Tool Use (2026-03-17)
### アーキテクチャ
- `backend/amazon_search.py`: SerpAPI → Amazon.co.jp商品検索
- `backend/flight_search.py`: Google Flights(SerpAPI) + Travelpayouts/Aviasales
- `backend/providers.py`: 各プロバイダーのストリーム関数にtool useループ内蔵
  - Claude: `tool_use` ブロック検出 → `tool_result` 返却（max 3 rounds）
  - OpenAI: `function calling` チャンク蓄積 → `tool` メッセージ返却
  - Gemini: `FunctionDeclaration` → `function_call`/`function_response` Parts
- `backend/base_prompt.py`: ツール使用指示をシステムプロンプトに含む
- `disable_tools` パラメータ: 議論モードでtool useを無効化

### 環境変数
- `SERPAPI_KEY`: Amazon検索 + Google Flights
- `TRAVELPAYOUTS_TOKEN`: Aviasalesフライト検索（アフィリエイト）
- 未設定時はツール自動無効化（既存機能に影響なし）

### 注意点
- 議論モードでtool useを有効にするとdebateフローが壊れる → `disable_tools=True`
- Gemini 503 UNAVAILABLEはリトライ対象（429と同じバックオフ）
- SerpAPIのフリー枠: 250回/月
