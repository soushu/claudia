---
name: Mazelan - 旅行特化AIツール
description: 旅行特化AIツール「Mazelan」。mazelan.ai稼働中、旅行API統合済み
type: project
---

Claudiaを旅行特化AIツールに発展させたプロジェクト。名前は **Mazelan**（Magellanにちなむ）。

**Why:** 旅行系APIを組み込んでAIチャットを差別化
**How to apply:** 今後の機能追加・API選定はMazelanとして進める

## 基本情報
- **名前**: Mazelan（Magellanにちなむ）
- **ドメイン**: mazelan.ai（Cloudflare Registrar、$80/年×2年、2026-03-15 取得済み）
- **DNS**: Cloudflare

## 実装済み旅行API
- **Google Maps検索リンク** — 場所を検知してリンク自動生成（base_prompt.py）
- **Amazon商品検索** — SerpAPI経由、BYOK不要、tool use全モデル対応
- **フライト検索** — Google Flights(SerpAPI) + Travelpayouts/Aviasales(728+航空会社)

### API選定経緯（フライト）
- Amadeus Self-Service: LCC含まれない → 不採用
- Kiwi.com Tequila: 50K MAU必要 → 登録不可
- Duffel: 日本法人の登録不可 → 断念
- **→ Travelpayouts/Aviasales に決定**（アフィリエイトモデル、API無料、728+航空会社）

## 今後の統合候補
- ホテル検索: SerpAPI Google Hotels / Travelpayouts
- 観光: Google Places API
- 天気: OpenWeatherMap
- 為替: Exchange Rate API

## ステータス
- [x] 名前決定・ドメイン取得 (2026-03-15)
- [x] ブランディング変更 (STEP 39)
- [x] ドメイン切り替え mazelan.ai (STEP 43)
- [x] 旅行API統合: Amazon + フライト検索 (STEP 48)
- [ ] GitHubリポジトリ リネーム (claudia → mazelan)
- [ ] soushu.biz Cloudflare移管（Pending Transfer、Xserver承認待ち）
- [ ] ホテル検索API統合
