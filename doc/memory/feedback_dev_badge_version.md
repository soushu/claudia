---
name: DEV badge version numbering
description: Increment version number on the staging DEV badge with every deploy to develop
type: feedback
---

DEV バッジにバージョン番号を付ける（例: `DEV v42.61`）。develop にマージするたびにインクリメントする。

**Why:** ステージング環境が更新されたかブラウザで一目でわかるようにするため。

**How to apply:**
- **整数インクリメント**（42→43）: 大きい変更（新機能追加等）
- **小数インクリメント**（42.61→42.62）: 小さい修正・調整
- 小数は2桁まで使用（例: 42.01, 42.10, 42.99）
- `frontend/app/chat/page.tsx` の DEV バッジを更新
