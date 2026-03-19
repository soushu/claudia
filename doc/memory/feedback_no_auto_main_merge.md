---
name: mainマージは必ずユーザー指示を待つ
description: develop→mainマージは自動でやらない。必ずユーザーの明示的な指示を待つ
type: feedback
---

develop → main へのマージは、ユーザーが「mainにマージして」と明示的に指示するまで絶対に行わない。

**Why:** CLAUDE.mdのルール3に記載済みだが、作業の流れで勝手にmainマージしてしまうことがあった。developへのマージ+pushまでは自律的にやってOKだが、mainマージは必ず止まって確認する。

**How to apply:** developマージ後に「mainにもマージしますか？」と聞くのはOK。ただし返答なしにマージしない。
