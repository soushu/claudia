---
name: npm ciデプロイ失敗時の対処
description: package-lock.jsonの不整合でnpm ciが失敗する問題。新パッケージ追加後に発生しやすい
type: feedback
---

新しいnpmパッケージを追加した後、`package-lock.json`がサーバーのNode.jsバージョンと同期しないと`npm ci`が失敗する。

**Why:** デプロイスクリプトは`npm ci`を使用しており、package.jsonとpackage-lock.jsonが完全一致していないとエラーになる。ローカルのNode.jsバージョンとサーバーのバージョンが異なると、lock fileの依存解決が変わることがある。

**How to apply:**
1. 新パッケージ追加後は`npm install`でlock fileを再生成してからコミット
2. デプロイスクリプトで`if ! npm ci; then npm install; fi`フォールバック対応済み（`||`は`set -euo pipefail`と干渉するため`if/then`方式を使用）
3. ローカルとサーバーのNode.jsバージョンを揃えるのが理想
4. 実例: `next-intl`追加時に`@swc/helpers`の依存が不整合でデプロイ失敗（2026-03-16）
