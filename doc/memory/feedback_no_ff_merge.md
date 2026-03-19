---
name: developマージは--no-ffで行う
description: feature→developマージ時に必ず--no-ffオプションを使い、マージコミットを残す
type: feedback
---

feature→developマージ時は `git merge --no-ff` を使うこと。

**Why:** fast-forwardマージだとdevelopの履歴上でマージコミットが残らず、直接コミットしたように見える。ユーザーから「直近5コミットが直接コミットされている」と指摘された（2026-03-15）。

**How to apply:** `git checkout develop && git merge --no-ff feature/xxx` の形で必ずマージコミットを作成する。
