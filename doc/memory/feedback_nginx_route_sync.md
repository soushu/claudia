---
name: Nginxルート追加時は3箇所すべて同期必須
description: バックエンドAPIパス追加時にNginx設定のリポジトリ・sites-available・sites-enabledの3箇所を必ず同期する
type: feedback
---

バックエンドに新しいAPIパス（例: `/debate/`, `/contexts/`）を追加する際は、以下の3箇所すべてを同期すること:

1. `deploy/nginx/claudia.conf` / `claudia-staging.conf`（リポジトリ）
2. `/etc/nginx/sites-available/`（サーバー）
3. `/etc/nginx/sites-enabled/`（サーバー）

**Why:** 2026-03-15に議論モード(`/debate/`)がNginxに登録されておらず本番でエラーになった。原因は、手動で`sites-enabled`に追加していたルートが、`sites-available`→`sites-enabled`へのコピー時に上書きされて消えたため。リポジトリのNginx設定にも`/debate/`が含まれていなかった。

**How to apply:**
- 新しいバックエンドAPIパスを追加する際は、コードと同時にリポジトリのNginx設定も更新する
- SSEストリーミングを使うエンドポイント（`/chat/`, `/debate/`）は `proxy_buffering off`, `proxy_cache off`, `chunked_transfer_encoding off`, `proxy_read_timeout 600s` を設定する
- サーバーで手動変更した場合は `sites-available` にもコピーしておく（`sites-enabled`はシンボリックリンクではなくコピーなので）
