---
name: 現在の作業状態
description: 現在の進捗と次のタスク。再起動後にすぐ再開するための状態メモ
type: project
---

## 現在のブランチ: `develop` (DEV v42.62)
## 最終更新: 2026-03-19

## 2026-03-18〜19 完了分

### mainマージ済み
- [x] 議論モード批評プロンプト改善（当たり前のことを褒めない）
- [x] ツール使用制限（明示的リクエスト時のみ）
- [x] SerpAPIキャッシュ導入（serpapi_cache.py: フライト3h, Amazon 1h）
- [x] ツール実行ステータス表示（「🔍 フライト検索中...」「🧠 考え中...」）
- [x] SerpAPIエラー時の適切なエラーハンドリング
- [x] 入力欄オートフォーカス
- [x] Slack通知名を Mazelan に変更

### developのみ（mainへの未マージあり）
- [x] Gemini Google Search Grounding追加（Web検索機能）
- [x] Gemini動的ツール切り替え（function_calling → google_search、同時併用不可のため）
- [x] SerpAPI枠切れ時のWeb検索フォールバック（エラー→google_searchで代替）
- [x] Web検索フォールバック時の注意書き（参考情報であることを明記）
- [x] 長URL防御（500文字超カット: フロント+バックエンド）
- [x] URLハンドリングプロンプト（URLの中身は読めない→Web検索で確認）
- [x] Google Mapsリンク精度改善（正式名称+支店名+都市+国名）
- [x] 議論モードペーシング中ステータス表示

## 現在の状況・注意点

### SerpAPI
- **無料枠250回/月を使い切り（2026-03-18時点で0回残）**
- 4月1日にリセットされるまでflight_search/amazon_searchは使えない
- Web検索フォールバックで代替中（ただし価格情報は不正確になる場合あり）
- 有料化時はSearchApi.io（$40/月・10,000回）に移行予定

### Gemini API制約
- google_searchとfunction_callingは同一リクエストで併用不可
- 動的切り替えで対応済み: function_calling実行後にgoogle_searchに切替
- ツールエラー検知時は即座にgoogle_searchに切替

### Web検索フォールバックの既知の問題
- LLMが具体的な価格を提示するが不正確な場合がある（Web検索の限界）
- プロンプトで注意書き（⚠️参考情報）を必須にして対応済み
- SerpAPI復旧後は構造化データに戻るので解消

## 残タスク
- developの変更をmainにマージ（ユーザー指示待ち）
- GCPプロジェクトクォータ解放後にフリープールキー追加
- soushu.biz移管完了（承認メール待ち）
- テストローンチ
- セキュリティ追加対応（ローンチ後）→ memory/project_security_todo.md
- ユーザー単位の無料枠制御（ローンチ後）→ memory/project_user_quota.md
