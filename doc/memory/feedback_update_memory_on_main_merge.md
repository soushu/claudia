---
name: mainマージ時にメモリ更新
description: develop→mainマージ時にMEMORY.mdの進捗状況（STEP一覧、ロードマップ、DEVバージョン等）を必ず更新する
type: feedback
---

mainにマージする際は、MEMORY.mdの進捗状況を必ず更新すること。

**Why:** ユーザーから明示的に指示があった。メモリが古いまま放置されると次回の会話で状況把握が遅れる。

**How to apply:** develop→mainマージを実行した直後に以下を確認・更新する:
1. 完了STEP一覧に新しいSTEPを追加
2. ロードマップの該当項目に✅完了マークを付ける
3. DEVバッジバージョンを現在の値に更新
4. 必要に応じてspec.md、implementation.md、roadmap.mdも更新
