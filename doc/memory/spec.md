# Mazelan 仕様書

最終更新: 2026-03-16 (STEP47 モデルロック+モバイルキーボード対応)

## プロジェクト概要
旅行特化AIチャットWebアプリ「Mazelan」。折りたたみ可能なQ&A UIが独自機能。
BYOK（Bring Your Own Key）方式で複数AIプロバイダーに対応。

- 本番: https://mazelan.ai
- ステージング: https://dev.mazelan.ai
- GCP: e2-small (bitpoint-bot, us-west1-b)

---

## 技術スタック

| レイヤー | 技術 |
|----------|------|
| Frontend | Next.js 14 (App Router) + React 18 + Tailwind CSS 3.4 + TypeScript 5 + next-intl (i18n) |
| Backend | FastAPI (Python) + Uvicorn + slowapi (レート制限) |
| DB | PostgreSQL + SQLAlchemy ORM + Alembic |
| 認証 | NextAuth.js v4 (Google OAuth + Email/Password) |
| AI | Anthropic Claude / OpenAI GPT / Google Gemini (マルチプロバイダー) |
| Markdown | react-markdown + react-syntax-highlighter + remark-gfm |
| デプロイ | GitHub Actions CI/CD + systemd + Nginx + certbot SSL |
| CI/CD | GitHub Actions + Workload Identity Federation (keyless) |
| i18n | next-intl (en/ja、ブラウザ言語自動検出、cookieオーバーライド) |

---

## APIエンドポイント一覧

### 認証 (`/auth`)
| Method | Path | レート制限 | 説明 |
|--------|------|-----------|------|
| POST | `/auth/upsert-user` | なし | Google OAuth時のユーザー作成/更新（X-Internal-API-Key必須） |
| POST | `/auth/login` | 5/min | メール/パスワード認証 |
| POST | `/auth/register` | 3/min | 新規ユーザー登録 |

### チャット (`/chat`)
| Method | Path | レート制限 | 説明 |
|--------|------|-----------|------|
| POST | `/chat/{session_id}` | 20/min | AIストリーミング応答（SSE）。ヘッダーでAPIキー送信。thinking対応 |

### セッション (`/sessions`)
| Method | Path | 説明 |
|--------|------|------|
| POST | `/sessions?title=...` | 新規セッション作成 |
| GET | `/sessions` | セッション一覧（is_starred DESC, updated_at DESC） |
| GET | `/sessions/{id}/messages` | メッセージ取得（created_at ASC） |
| DELETE | `/sessions/{id}` | セッション削除 |
| PUT | `/sessions/{id}` | セッションタイトル更新 |
| PUT | `/sessions/{id}/star` | スター切替 |
| GET | `/sessions/user/system-prompt` | グローバルシステムプロンプト取得 |
| PUT | `/sessions/user/system-prompt` | グローバルシステムプロンプト更新 |
| GET | `/sessions/{id}/system-prompt` | セッション別プロンプト取得 |
| PUT | `/sessions/{id}/system-prompt` | セッション別プロンプト更新 |

### コンテキストメモリ (`/contexts`)
| Method | Path | 説明 |
|--------|------|------|
| GET | `/contexts` | カテゴリ別コンテキスト一覧 |
| POST | `/contexts` | 手動コンテキスト作成 |
| PATCH | `/contexts/{id}` | コンテキスト編集 |
| DELETE | `/contexts/{id}` | コンテキスト削除 |
| PATCH | `/contexts/{id}/toggle` | アクティブ切替 |

### 議論モード (`/debate`)
| Method | Path | レート制限 | 説明 |
|--------|------|-----------|------|
| POST | `/debate/{session_id}` | 10/min | AI議論ストリーミング（5ステップ）。thinking対応 |

### その他
| Method | Path | 説明 |
|--------|------|------|
| GET | `/health` | ヘルスチェック |

---

## データベーススキーマ

### users
| カラム | 型 | 説明 |
|--------|------|------|
| id | UUID (PK) | |
| google_id | String (nullable, unique) | Google OAuth ID |
| email | String (unique) | |
| name | String (nullable) | |
| password_hash | String (nullable) | bcrypt |
| auth_provider | String | 'google' or 'email' |
| system_prompt | Text (nullable) | グローバルシステムプロンプト |
| created_at | DateTime (UTC) | |

### chat_sessions
| カラム | 型 | 説明 |
|--------|------|------|
| id | UUID (PK) | |
| user_id | UUID (FK → users) | |
| title | String(60) | |
| system_prompt | Text (nullable) | セッション別プロンプト（優先） |
| is_starred | Boolean | スター付きフラグ |
| created_at | DateTime (UTC) | |
| updated_at | DateTime (UTC) | |

### messages
| カラム | 型 | 説明 |
|--------|------|------|
| id | UUID (PK) | |
| session_id | UUID (FK → chat_sessions) | |
| role | String | 'user' or 'assistant' |
| content | Text | |
| model | String (nullable) | 使用モデルID |
| images | JSON (nullable) | [{media_type, data(base64)}] |
| created_at | DateTime (UTC) | |

### contexts
| カラム | 型 | 説明 |
|--------|------|------|
| id | UUID (PK) | |
| user_id | UUID (FK → users) | |
| content | Text | コンテキスト内容 |
| category | String(50) | preferences/skills/projects/personal/general |
| source | String(10) | 'auto' or 'manual' |
| session_id | UUID (FK, nullable) | 自動抽出元セッション |
| is_active | Boolean | |
| created_at / updated_at | DateTime (UTC) | |

---

## フロントエンド構成

### ページ
| パス | ファイル | 説明 |
|------|----------|------|
| `/` | `app/page.tsx` | → /chat にリダイレクト |
| `/chat` | `app/chat/page.tsx` | メインチャットUI |
| `/login` | `app/login/page.tsx` | ログイン画面 |

### コンポーネント
| ファイル | 説明 |
|----------|------|
| `Sidebar.tsx` | セッション一覧、検索、タイトル編集、スター、設定モーダル、テーマ切替、モバイルアコーディオン |
| `ChatInput.tsx` | メッセージ入力（Cmd+Enter送信）、画像添付、モデル選択、議論モードトグル、思考モードトグル |
| `QAPairBlock.tsx` | Q&Aペア表示、折りたたみ、コピーボタン、ストリーミング表示、バウンスドットインジケーター |
| `UserBubble.tsx` | ユーザーメッセージ表示、長文5行クランプ+"...more"展開 |
| `MessageContent.tsx` | Markdown描画、シンタックスハイライト、コードコピーボタン |
| `ProviderIcon.tsx` | Claude/OpenAI/Gemini公式SVGアイコン |
| `ApiKeyModal.tsx` | 3プロバイダーAPIキー管理（localStorage） |
| `SystemPromptModal.tsx` | グローバル+セッション別システムプロンプト編集 |
| `ContextModal.tsx` | コンテキストメモリCRUD（カテゴリ別表示、楽観的トグル） |

### ユーティリティ (`lib/`)
| ファイル | 説明 |
|----------|------|
| `api.ts` | バックエンドAPI呼び出し（fetch + credentials） |
| `types.ts` | 型定義（Provider, ModelId, Session, Message, ModelGroup等） |
| `apiKeyStore.ts` | localStorage APIキー管理（取得/保存/バリデーション） |
| `themeContext.tsx` | テーマ状態管理（dark/sky-blue/cyan） |

---

## 対応AIモデル

### Anthropic Claude
| Model ID | ラベル | 画像 | Web検索 | 思考 |
|----------|--------|------|---------|------|
| claude-sonnet-4-6 | Claude Sonnet 4.6 | o | o | o |
| claude-opus-4-6 | Claude Opus 4.6 | o | o | o |
| claude-haiku-4-5-20251001 | Claude Haiku 4.5 | o | o | o |

### OpenAI GPT
| Model ID | ラベル | 画像 | 備考 |
|----------|--------|------|------|
| gpt-4o | GPT-4o | o | |
| gpt-4o-mini | GPT-4o mini | o | |
| o3-mini | o3-mini | x | max_completion_tokens使用 |

### Google Gemini
| Model ID | ラベル | 画像 | 思考 | 備考 |
|----------|--------|------|------|------|
| gemini-2.5-flash | Gemini 2.5 Flash | o | o | |
| gemini-2.5-pro | Gemini 2.5 Pro | o | o | |
| gemini-3.1-flash-lite | Gemini 3.1 Flash Lite | o | x | |

---

## 主要機能

### 折りたたみUI
- Q&Aペア単位で折りたたみ可能（独自機能）
- 最新のペアは展開、古いものは折りたたみ

### マルチプロバイダーAI
- `providers.py`でプロバイダー抽象化
- メッセージ形式をAnthropicスタイルから各プロバイダー形式に変換
- APIキーはフロントエンドのlocalStorageに保存、ヘッダーで送信

### ストリーミング応答
- SSE（Server-Sent Events）でリアルタイム表示
- StreamingResponse内でSessionLocal()直接生成（Depends(get_db)は使えない）
- タイピングインジケーター: 3つのバウンスドット（w-fit吹き出し）

### コンテキストメモリ
- Claude Haikuで会話から自動抽出（fire-and-forget、ユーザーの言語で保存）
- 重複検出（部分文字列マッチ）
- 手動CRUD + カテゴリ分類（ボタンで保存、Enter無効）
- アクティブなコンテキストはシステムプロンプトに`<context_memory>`として注入
- トグル: 楽観的UI更新（スクロールリセットなし）

### システムプロンプト
- グローバル（ユーザー単位）+ セッション別
- セッション別がグローバルを上書き
- 複数指示は改行区切りで登録可能
- コンテキストメモリと結合してプロバイダーに送信

### 画像添付
- base64マルチモーダル（DB永続化）
- ドラッグ&ドロップ / ペースト / ファイル選択
- 各プロバイダー形式に変換

### テーマ
- Dark / Sky Blue / Cyan の3テーマ
- CSS変数 + Tailwindカスタムカラー
- localStorageで永続化

### 認証
- Google OAuth + メール/パスワード（NextAuth.js v4）
- JWTトークン（secure HTTP-only cookie、SameSite=Lax）
- バックエンド側でfastapi-nextauth-jwtで検証

### エラーハンドリング
- `⚠️`アイコン付き日本語エラーメッセージ
- 4種類に分類: 認証エラー / レート制限(429) / 月額上限(400) / その他
- providers.py: ProviderAuthError / ProviderRateLimitError / ProviderSpendLimitError / ProviderError
- main.py: グローバル例外ハンドラー（ValidationError→汎用メッセージ、未処理例外→ログ+500）

### 送信方法
- Cmd+Enter (Mac) / Ctrl+Enter (Win) で送信
- 送信ボタンクリック
- Enterは改行

### AI議論モード
- 2つのモデルで5ステップ議論（回答A→回答B→批評A→批評B→統合回答）
- ChatInputの黄色「🔀 議論」トグルで有効化
- 両モデルのAPIキーが必要
- DB保存形式: `<!--DEBATE:modelA:modelB-->` + `<!--STEP:...-->` マーカー

### 思考モード (Extended Thinking)
- ChatInputの紫「🧠 思考」トグルで有効化（対応モデルのみ表示）
- Anthropic: `thinking={"type":"enabled","budget_tokens":10000}`, max_tokens=16000
- Gemini 2.5: `ThinkingConfig(thinking_budget=10000)`

### セッションタイトル編集
- サイドバーで3点メニュー → Rename でインライン編集

### お気に入り(スター)機能
- サイドバーで3点メニュー → Star/Unstar切替
- スター付きセッションはリスト上部にピン表示
- 黄色星アイコンでスター状態を表示

### ウェルカム画面
- 新規セッション時にGemini風サジェストカード4枚表示
- カードクリックでテキストエリアに質問をセット

### トークン使用量・コスト表示 (STEP 35)
- メッセージごとにトークン数・コストをホバーツールチップで表示

### チャットエクスポート (STEP 37)
- テキスト / PDF形式でエクスポート可能

### 利用規約・プライバシーポリシー (STEP 38)
- フッターからアクセス可能

### ベースシステムプロンプト (STEP 41)
- `backend/base_prompt.py` — Mazelanの旅行AI identity + Google Mapsリンク生成指示
- 全チャットに自動適用

### Geminiフリーキープール (STEP 42)
- `GEMINI_FREE_KEYS` env var（5プロジェクト: mazelan-free-1〜5）
- ラウンドロビンで分散
- キーチェーン: ユーザーキー → フリープール → 有料フォールバック
- デフォルトモデル: Gemini 2.5 Flash Lite

### コスト倍率表示 (STEP 45)
- 全モデルにプロバイダー内コスト倍率 `(Free x1)` / `(Free x2)` / `(Free x10)` 表示（キー未設定時のみ）

### i18n 多言語対応 (STEP 46)
- next-intl使用。`frontend/messages/en.json` / `ja.json`（約130キー）
- ブラウザ言語自動検出、cookieでオーバーライド可

### モデルロック (STEP 47)
- APIキー未設定モデルに🔒表示
- 選択 → 該当プロバイダーのAPI Key設定画面表示
- 送信時もキーチェック → 未設定ならモーダル表示（入力テキスト保持）

### モバイルキーボード対応 (STEP 47)
- visualViewport APIで入力欄を予測変換バーの上に押し上げ

### セキュリティ
- CSRF: SameSite=Lax cookie + httpOnly + Secure(本番)
- レート制限: slowapi (IP-based) — login/register/chat/debate/upsert-user
- 依存パッケージ: 全バージョン固定
- エラー: グローバル例外ハンドラーで内部情報漏洩防止
- HTTPヘッダー: X-Frame-Options, HSTS, nosniff, CSP, Referrer-Policy, Permissions-Policy (Nginx)
- 画像base64: 10MB/枚, 5枚/リクエスト, media_typeホワイトリスト (schemas.py)
- ストリーミングタイムアウト: 5分/チャンク (providers.py)
- リクエストボディサイズ: Nginx client_max_body_size 20m
- メール列挙防止: 登録/ログインで同一メッセージ返却

### サイドバー
- モバイル: メール+シェブロンで設定エリアをアコーディオン折りたたみ
- PC: 従来通り全表示
- アクティブセッション: 左ボーダー(border-l-2) + font-medium

### セッション維持
- activeIdをlocalStorageに保存
- リロード時に復元 + メッセージ再取得 + 最後の質問にスクロール

---

## ファイル構成（主要）

```
claudia/
├── backend/
│   ├── main.py              # FastAPIアプリ (CORS, ルーター, グローバル例外ハンドラー, レート制限)
│   ├── models.py            # SQLAlchemy ORM (User, ChatSession, Message, Context)
│   ├── database.py          # DB接続 & セッション管理
│   ├── dependencies.py      # NextAuth JWT認証DI
│   ├── providers.py         # マルチプロバイダー抽象化 (Claude/GPT/Gemini)
│   ├── context_extractor.py # Claude Haikuでコンテキスト自動抽出（ユーザー言語対応）
│   └── routers/
│       ├── auth.py          # 認証 (upsert-user, login, register) + レート制限
│       ├── chat.py          # チャットストリーミング (thinking対応) + レート制限
│       ├── debate.py        # AI議論モード (5ステップ議論) + レート制限
│       ├── sessions.py      # セッション管理 + タイトル編集 + スター + システムプロンプト
│       └── contexts.py      # コンテキストメモリCRUD
├── frontend/
│   ├── app/                 # Next.js App Router (chat, login, auth API)
│   ├── components/          # React コンポーネント
│   ├── lib/                 # API呼び出し、型定義、状態管理
│   └── tailwind.config.ts   # テーマ設定
├── alembic/                 # DBマイグレーション
├── deploy/                  # systemd, nginx, デプロイスクリプト
├── .github/workflows/
│   ├── deploy.yml           # main push → 本番自動デプロイ
│   └── deploy-staging.yml   # develop push → ステージング自動デプロイ
└── requirements.txt         # Python依存（全バージョン固定）
```

---

## CI/CD構成

### 環境
| 環境 | ブランチ | ドメイン | Backend | Frontend | DB |
|------|----------|----------|---------|----------|-----|
| 本番 | main | mazelan.ai | :8000 | :3000 | claudia |
| ステージング | develop | dev.mazelan.ai | :8002 | :3002 | claudia_staging |

### 認証
- Workload Identity Federation（JSON鍵なし）
- SA: `claudia-deploy@bitpoint-bot.iam.gserviceaccount.com`
- IAP SSH → yutookiguchi@bitpoint-bot

### デプロイフロー
1. push → GitHub Actions トリガー
2. WIF認証 → gcloud compute ssh (IAP tunnel)
3. git fetch + reset → pip install → alembic → サービスstop → npm ci + build → サービスstart
4. SSH経由ヘルスチェック

### 制約・OOM対策
- concurrency group `deploy-gce` で本番/ステージング同時ビルド防止
- ビルド前にサービスstop（メモリ解放）
- `NODE_OPTIONS="--max_old_space_size=384"`
- ヘルスチェック120秒タイムアウト（起動が遅い）
