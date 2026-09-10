# The AI + Real Sports Media strategy

Chuck's research, 9 Sep 2026. **Read this at the start of every session and
before building any content.** He asked for it to be read 2-3 times a day
because I drifted from it inside a single afternoon.

The one-line version: **Claude is the editor-in-chief, not the media source.**
The bottleneck is a rights-cleared sports media supply chain, not a better
image generator. Do not solve a media problem by making another graphic.

---


Inside the Number — AI + Real Sports Media Content System
A practical stack for producing professional Instagram Reels, Instagram posts, and X content with current real sports photos/video — not generic AI graphics.
Bottom lineDo not replace Claude. Reposition it. Claude should be the editor-in-chief, analyst, copywriter, and workflow orchestrator. It should NOT be responsible for sourcing the actual sports footage. The missing layer is a rights-cleared sports media feed plus a real video editor.
1. The recommendation in one picture
Tool
Role
Verdict
Claude
Brain / editor-in-chief
Analyzes games, writes hooks/scripts/captions, chooses stories, creates asset briefs, maintains brand voice.
Minute Media Content Suite
Best candidate for licensed sports video + images
Rights-cleared highlight library across major US leagues; built for publishers; monetization attached to assets.
Imagn / Reuters Connect
Current real sports photography
Large sports wire; real game/action photos; commercial and social licensing available; individual examples show low-cost single-property licensing.
SportFeeds
Real-time sports social/video API
Pulls clips from verified sports accounts, tags players/leagues, supports engagement scoring and region-aware filtering; useful as a technical discovery/ingestion layer.
Canva
Brand/design layer
Connected directly to Claude; creates and edits reusable branded social templates.
CapCut
Reels assembly
Turns real clips into vertical Reels quickly; auto-cut, captions, reframing, audio and export.
ChatGPT
Second opinion / research QA
Web search is available even on Free; useful for verifying breaking stories and challenging weak ideas; also connects to Canva.
Grok
X trend radar only
Best use is monitoring what is exploding on X in real time. Not the core content-production engine.
Gemini
Optional Google-side helper
Useful for Google ecosystem/Canva-connected workflows and research; not necessary to add if the existing Claude workflow is strong.
2. Why Claude feels like a dead end
Claude is not fundamentally failing at writing or strategy. The bottleneck is that “generate a good social post” and “obtain current, usable, rights-cleared sports media” are two different jobs. Claude can now work with creative software and Canva, but Canva and AI image generators do not turn current NFL/NBA/MLB game moments into licensed broadcast highlights.
Claude + Canva can create polished designs, resize assets, search Canva content, and export finished designs. That solves the design layer — not the live sports-media rights layer.
Claude can connect to Adobe creative tools, including Photoshop, Premiere, Express, Lightroom and Stock, and can orchestrate multi-step creative workflows. That makes Claude a better production manager, but it still does not create the rights to NFL/NBA/MLB broadcast footage.
The real-world “big sports account” look comes from a combination of immediate real footage/photo selection, tight editorial timing, strong captions, and consistent motion branding.
3. The most important new discovery: Minute Media
For Inside the Number, this is the first company I would contact. Minute Media’s Content Suite advertises premium, licensed video highlights and images, with official highlight rights covering NFL, MLB, NBA, PGA TOUR, NHL, MLS and F1, plus monetization infrastructure. It is aimed at publishers rather than casual creators.
Ask specifically for a small-publisher / independent sports-media package for InsideTheNumber.com and the associated Instagram/X accounts.
Ask whether the license covers: website, organic Instagram, Instagram Reels, X, Facebook, paid promotion, and commercial subscription marketing.
Ask whether assets can be delivered via API/feed or only through a portal. API delivery is much more valuable for a passive-income workflow.
Ask about geographic restrictions, attribution requirements, retention windows, and whether betting/sportsbook-related content is permitted.
Why this mattersIf Minute Media will onboard a small publisher on reasonable terms, it can eliminate the hardest problem in your business: getting the actual clip of the thing that just happened instead of producing a graphic about it.
4. Real photographs: Imagn / Reuters Connect
Imagn is particularly relevant for US sports. It operates one of the largest sports-photo networks and states that its content can be licensed for editorial and commercial projects including websites, social media and advertising. Reuters now manages the licensing/sales side through Reuters Connect.
Use this when the post needs a striking real player/coach/game photo but does not need video.
A current Reuters Connect example for an NFL Titans-Bears image displayed a single-property digital/social license at $50 for worldwide, one-year, single-use terms up to 50,000 monthly unique visitors. Exact prices vary by asset and license, but the example demonstrates that individual social-ready sports photos can be acquired without buying a huge enterprise package.
For a betting publisher, confirm the exact commercial/promotional rights before using any image in an ad, sponsor creative, or subscription promotion.
5. SportFeeds: very interesting for automation, but confirm rights
SportFeeds is a compelling technical layer. Its current product says it ingests sports highlights and breaking social content from verified team, league, athlete and media accounts on roughly a one-minute cycle, tags clips to sport/league/team/player, scores engagement, and applies region-aware content-rights filtering.
This could be the “radar” that tells your system a specific Jalen Hurts / Luka Doncic / Shohei Ohtani clip exists right now.
It can reduce the manual work of hunting through hundreds of accounts.
Do not assume that a clip being visible or delivered by an API automatically gives Inside the Number permission to re-upload it commercially. Get written confirmation of redistribution rights for Instagram/X and your website before building the workflow around it.
6. What each AI should actually do
Claude: the boss
Claude should decide what is worth posting. Give it your sports-data feeds, story rules, brand voice, templates and asset rules. It should output a production brief, not immediately invent a graphic.
ChatGPT: the challenger
Use ChatGPT when you want a second opinion: verify the news, challenge a claim, compare competing angles, search for the freshest reporting, or critique a proposed caption. ChatGPT web search is available on the Free plan.
Grok: the X radar
Use Grok specifically for “what is blowing up on X right now?” because Grok can search public X posts in real time. It is especially useful for finding conversation, reactions and emerging narratives.
Gemini: optional
Keep Gemini available because you already pay for it, but do not make it the center of the stack unless its Google/Canva workflow proves materially better for a specific job. It is not the missing answer to the real-footage problem.
Canva: design system
Build 8–12 reusable Inside the Number templates: breaking news, line movement, injury, player trend, best bet, worst bet, postgame, carousel, quote card, and “the number was right” recap.
CapCut: video factory
Once the real clip exists, CapCut should handle the repetitive edit work: 9:16 crop, cutting dead time, subtitles, sound, text overlays, and export.
7. The content formula that will look like a real sports-media account
The goal is not to make every post a giant graphic. Make the sports moment the hero and put Inside the Number’s analytics around it.
Format
Structure
REAL CLIP + NUMBER
5–15 sec highlight of the actual play → one powerful statistic → one betting/analytics implication → CTA.
REAL PHOTO + NUMBER
Real player/coach/game photo → 2–3 lines of data → “Here is what the market is missing.”
CAROUSEL
Slide 1 real image; Slides 2–5 data story; final slide subscription CTA.
POSTGAME REEL
Three real moments from the game + three numbers the model liked/disliked.
LIVE/MOVE POST
Real current image or official clip + line movement + timestamp + concise explanation.
OPINION/REACTION
Use real reaction image/video from the current story, but make the analysis uniquely yours.
8. The workflow I would build
1. Monitor: Claude/Grok/SportFeeds detect games, injuries, line moves, postgame moments and viral stories.
2. Decide: Claude scores each story for urgency, audience interest, statistical edge, subscription value and visual potential.
3. Source the real media: Minute Media for licensed highlights; Imagn/Reuters Connect for current photos; SportFeeds for discovery/automation if rights are confirmed.
4. Produce: Claude writes hook, script, caption, CTA and on-screen copy. Canva builds static/carousel assets. CapCut builds Reels from the real footage.
5. QA: ChatGPT or a human checks facts, line/time, player, score and any claims before publishing.
6. Publish: Use Adobe Express Content Scheduler or another scheduler for approved Instagram/X publishing. Adobe Express currently supports scheduling to Instagram Business/Creator and X.
7. Learn: Feed performance metrics back into Claude weekly so it stops producing formats that get no reach and doubles down on winners.
9. The exact instructions to give Claude
Paste the following into the Inside the Number project instructions/system prompt. The most important change is the distinction between “content idea” and “media asset.”
You are the Editor-in-Chief and Content Director for Inside the Number, a professional sports analytics and betting-media brand.PRIMARY OBJECTIVEProduce content that looks and feels like a legitimate modern sports-media publisher, not an AI content farm. Real sports moments, current reporting and strong editorial timing must lead. Graphics are supporting elements, not the default visual.NON-NEGOTIABLE MEDIA RULES1. Never default to an AI-generated image of a real athlete when a current real photo or licensed real video is available.2. Never fabricate a sports highlight, player reaction, injury, quote, score, line movement or game moment.3. Do not assume that a photo/video found on X, Instagram, YouTube, TikTok or a website is licensed for commercial re-use. Treat public visibility as different from publishing rights.4. Prefer rights-cleared/licensed sources. Use Minute Media for licensed sports video/highlights when available; use Imagn/Reuters Connect for licensed current sports photography; use other verified/authorized sources only after confirming the allowed use.5. When rights are unclear, label the asset STATUS = RIGHTS UNKNOWN and do not recommend downloading/re-uploading it.EVERY CONTENT IDEA MUST PRODUCE TWO OUTPUTSA. EDITORIAL BRIEF- Story- Why people care now- Key statistic/number- Hook- Caption- CTA- Target platform- Ideal lengthB. MEDIA BRIEF- Asset type: real video / real photo / official social post / graphic- Exact subject- Suggested source- Rights status: LICENSED / OFFICIAL-USE / RIGHTS UNKNOWN- Recommended crop: 9:16 / 4:5 / 1:1 / 16:9- Suggested clip length- What exact moment should be shownCONTENT PRIORITYScore every idea 1-10 on: urgency, visual power, statistical novelty, betting relevance, shareability, subscription value.CREATIVE RULEDo not make a graphic merely because you can. First ask: “What real image or video would make this impossible to scroll past?” Only then add the Inside the Number data layer.REEL STRUCTURE0-2 sec: strongest real moment + hook2-7 sec: what happened7-12 sec: the number that matters12-18 sec: betting/analytics implication18-22 sec: CTA to InsideTheNumber.comBRAND VOICEConfident, sharp, analytical, slightly provocative, never cheesy. No generic “Here’s why this matters” filler. Use specific numbers, timestamps and consequences.OPERATING PRINCIPLEYou are responsible for deciding WHAT should be published and HOW it should be framed. You are not responsible for inventing the real sports media. Source or request the real asset first, then build the story around it.
10. A practical first-phase budget strategy
Because the goal is passive income, avoid building an expensive enterprise media stack on day one. The first milestone is proving that real sports visuals materially improve reach and subscriber conversion.
Keep Claude as the main brain.
Keep Canva as the design system.
Add CapCut for video assembly if you do not already have a preferred editor.
Contact Minute Media first about a small-publisher package.
Use Imagn/Reuters Connect selectively for the highest-value photo posts rather than licensing dozens of photos before you know what converts.
Use SportFeeds as a test/integration layer if the API economics and redistribution rights make sense.
Do not add another general-purpose AI subscription just because it can generate prettier graphics. The missing ingredient is current real media, not another image generator.
11. What I would not do
I would not tell Claude to scrape and repost random sports highlights from X, YouTube or TikTok.
I would not build the brand around AI-generated fake player imagery.
I would not make every post a static “stat card.” Sports feeds win because something happened and the audience gets to see it.
I would not automate publishing without a fast fact/rights check. One wrong player, score, line or clip can damage the brand.
12. Final recommendation
The cleanest architecture is:
CLAUDE → SPORTS MEDIA FEED / LICENSED ASSETS → CANVA + CAPCUT → SCHEDULER → INSTAGRAM / X
Claude stays. Gemini stays optional. Grok becomes a real-time X radar. ChatGPT becomes a second-opinion/research tool. The critical investment is the sports-media layer: licensed current video and real photography. That is the difference between an AI-generated sports page and a professional sports-media brand.
Sources checked
Anthropic — Claude for Creative Work — https://www.anthropic.com/news/claude-for-creative-work
Anthropic — Claude connectors directory — https://www.anthropic.com/news/connectors-directory
Canva — AI Connector for ChatGPT / Claude / Gemini — https://www.canva.com/help/mcp-agent-setup/
Minute Media — Content Suite — https://beta.minutemedia.com/platform/content
SportFeeds — Sports Highlights API — https://sportfeeds.com/products/highlights-api
Imagn — Services — https://www.imagn.com/services/
Imagn — Licensing and Reprints — https://imagn.com/licensing-reprints/
Reuters Connect — current NFL sports photo license example — https://www.reutersconnect.com/item/nfl-chicago-bears-at-tennessee-titans/dGFnOnJldXRlcnMuY29tLDIwMjY6bmV3c21sX01UMVVTQVRPREFZMjk2OTQzNjM%3D
Reuters — Reuters Connect now sole platform for licensing visual content — https://www.reuters.com/media-center/reuters-connect-now-single-destination-license-visual-content-2026-07-28/
CapCut — AI video editor / auto video editor — https://www.capcut.com/tools/ai-video-editor
Adobe Express — scheduling/publishing social posts — https://helpx.adobe.com/express/web/publish-and-share/share-to-social-media/schedule-publish-social-posts.html
OpenAI — ChatGPT web search — https://help.openai.com/en/articles/9237897
X Help — About Grok — https://help.x.com/en/using-x/about-grok
