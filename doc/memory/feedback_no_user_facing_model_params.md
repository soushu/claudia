---
name: No user-facing model parameters
description: Temperature等のモデルパラメータはユーザーに触らせず、バックエンドで自動判断すべき
type: feedback
---

Temperature、Top P等のモデルパラメータをUIに出してユーザーに調整させるべきではない。

**Why:** ユーザーが関与すべきことではなく、用途に応じてAI/バックエンド側で最適値を自動選択すべき。UXとして悪い。

**How to apply:** モデルパラメータ調整UIの実装は行わない。将来的に必要なら、プロンプト内容やモード（コード生成/ブレスト等）に応じてバックエンドで自動設定する方式にする。
