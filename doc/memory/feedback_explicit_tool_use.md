---
name: ツール使用は明示的リクエスト時のみ
description: flight_search・amazon_product_searchはユーザーが明示的に検索を依頼した時のみ使用。API無駄遣い防止
type: feedback
---

外部APIツール（flight_search, amazon_product_search）は、ユーザーが明示的に依頼した時のみ使用する。

- **flight_search**: 「航空券を調べて」「安い便は？」など明示的な検索依頼時のみ。運航再開の有無など一般的な質問では呼ばない
- **amazon_product_search**: 「Amazonで調べてリンク教えて」など商品リンクを明示的に求めた時のみ。「おすすめは？」程度では呼ばない

**Why:** SerpAPI無料枠250回/月。フライト検索1回で~11回消費するため、不要な呼び出しは致命的。

**How to apply:**
- base_prompt.py のツール使用指針に反映済み
- ツールのdescription自体にも「ONLY use when explicitly asked」を記載済み（二重ガード）
- SerpAPIエラー時はWeb検索（google_search）でフォールバック（providers.pyで動的切替）
- Web検索フォールバック時は注意書き「⚠️参考情報」を必ず付与
- 新しいツールを追加する際も同じ原則を適用する
