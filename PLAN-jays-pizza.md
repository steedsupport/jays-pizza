# JAY'S PIZZA — Cinematic Scrollytelling Website
**Location:** Cambridge/KW, Ontario · **Craft:** Wood-fired Neapolitan · **Menu:** Indian-Italian fusion
**Sections:** 4 · **Videos:** 4 × 10s (Veo 3.1, zero camera cuts) · **Build:** GSAP ScrollTrigger + Lenis + canvas frame-scrub

---

## SECTION 1 — The Concept & Architecture

**Narrative arc:** *One pizza, dawn to table.* The scroll IS the pizza-maker's day: S1 the dough blooms at dawn → S2 the fire takes it → S3 the two worlds (Naples × Masala) meet on the cut board → S4 the table, warm and ready. The user's thumb kneads, fires, garnishes, and serves the pizza.

**Vibe:** "Cinematic Trattoria Fusion" — Caravaggio firelight, Ontario small-town brick-and-warmth, faint saffron-and-char perfume in the grade. Dark ember backgrounds (#1A120B), warm cream type (#F5E9D7), brand red accents (#B33A2B – deeper, food-trust red), gold ember highlights.

**Architecture (the right technical choice for this brand):** ONE fixed full-viewport pinned canvas for the entire page (single <canvas>, no rebuilds between sections). Scroll position drives a timeline of 4 image-sequence playlists; crossing a section boundary triggers a stylized ember-flash / white-lift wipe while the next sequence preloads. UI (menu, CTA "Order Now") floats as glassmorphism chrome above the canvas. This gives one continuous cinematic feel — no page-feel, no seams, exactly the "movie" brief.

Sections:
1. **S1 — THE BLOOM** (dough, dawn light, hands) — slow push-in
2. **S2 — THE FIRE** (oven dome, flames, peel) — slow arc around the oven mouth
3. **S3 — THE FUSION** (top-down board, garnish landing) — overhead descend
4. **S4 — THE TABLE** (finished pie, trattoria glow, brand card) — slow pull-back + logo

---

## SECTION 2 — Image Prompts (Keyframes, 8K intent)

All: photoreal cinematic food-film stills, no text unless noted, no watermarks, no people's faces (hands only — keeps brand human but anonymous).

**K1 (anchor — feeds S2/S3/S4 continuity):**
> Cinematic 8K food-film still. Dawn in a small-town Ontario brick-walled pizzeria kitchen, Cambridge. Strong pizzaiolo hands stretching fresh Neapolitan dough on a dark oak counter, flour dust suspended in warm light beams from a sash window, a glass jar of slow-ferment dough, copper pans on hooks, a small brass bowl of saffron strands and a basil plant on the sill (subtle Indian-Italian cues). 85mm lens, f/1.8, shallow depth of field, backlit rim light, chiaroscuro warm amber + charcoal palette, steam-breath dawn atmosphere, Chef's Table / Kinfolk editorial grade. Landscape 16:9.

**K2 (from K1, same kitchen/counter):**
> Same kitchen as reference. The hand-built Neapolitan brick oven dome blazing, rolling flame inside, glowing embers; a long wooden peel sliding in an artisan margherita beginning to leopard-spot char; a second pie on the peel edge with a thin chili-honey glaze drizzle. 35mm lens, f/2, low three-quarter angle up from the hearth, volumetric smoke, sparks, Caravaggio firelight, deep shadows. Landscape 16:9, photoreal, no text.

**K3 (board shot — garnish moment):**
> Top-down flat-lay on a dark oak board in the same kitchen: a just-baked margherita with blistered leopard-spotted crust, steam rising; a hand placing fresh paneer cubes, cilantro sprigs and a saffron-tomato chutney drizzle beside torn basil; small copper cup of spiced tomato sauce, flour traces on the board. 40mm overhead, soft bright kitchen light, supreme food appetite appeal. Landscape 16:9, photoreal, no text.

**K4 (hero — brand card):**
> Cinematic hero shot: the finished fusion pizza on a rustic board, center of a reclaimed-wood table in a warm Cambridge Ontario trattoria — exposed brick, evening tungsten glow, candles and glassware soft behind, steam curling off the pie. Beside the board, a small menu card with bold red letterpress text exactly "JAY'S PIZZA" (short, clean, no other writing). 50mm, f/2, candlelight + tungsten, nostalgic Italian film still. Landscape 16:9.

---

## SECTION 3 — Video Prompts (Veo 3.1 · 10s each · ZERO CUTS)

Every prompt must carry: "Single continuous unbroken take, zero camera cuts, no jump cuts, no editing cuts; smooth constant-speed camera on a fixed physical path; consistent kitchen from first frame to last; native ambient sound."

**V1 (first frame = K1):** "Single continuous unbroken take, zero camera cuts. Steady tracking shot, slow push-in: hands stretching a fresh Neapolitan dough round on a dark oak counter in a warm dawn brick kitchen; flour dust drifting in light beams; dough widens and breathes as it turns. Ends on the dough resting, ready for the peel. Native audio: soft kitchen dawn ambience, faint dough slap on wood, distant oven murmur." (Camera path: steady track-in, 24fps feel, motion ramp at 60% for drama.)

**V2 (first frame = K2):** "Single continuous unbroken take, zero camera cuts. Slow lateral arc left-to-right around the mouth of a blazing wood-fired oven dome; the peel enters and slides the margherita onto the stone floor; flames fold over the crust, leopard char blooming; embers swirl. Native audio: fire crackle, stone hiss, peel scrape." (Camera path: slow orbital arc, ~15° per second, no cut.)

**V3 (first frame = K3):** "Single continuous unbroken take, zero camera cuts. Overhead locked axis, slow push-down and drift right: steam lifts off a just-baked margherita on the oak board; a hand places paneer cubes, cilantro sprigs, then a slow spiral drizzle of saffron-tomato chutney over torn basil; toppings settle into melting cheese. Native audio: crisp knife-through-crust tick, soft sizzle, chalkboard tap." (Camera path: vertical descend + lateral drift, single motion, no cut.)

**V4 (first frame = K4):** "Single continuous unbroken take, zero camera cuts. Slow pull-back reveal: steam curls off the finished fusion pizza on its board; the table, candles and brick trattoria glow come into focus; ends framed centered above the board with the 'JAY'S PIZZA' menu card legible, symmetric hero composition. Native audio: warm trattoria ambience, candle flicker, a contented distant laugh." (Camera path: pure dolly back, 8% speed feel, stabilizer-smooth, no cut.)

**Duration handling:** Gemini API Veo 3.1 generates 4/6/8s per call; we generate **8s then extend +2s (extend-from-last-frame API)** to hit 10s, or play 8s scrub-slid across the section. Choose at build: extend = true 10s files.

---

## SECTION 4 — The Antigravity Master Code Prompt (paste-ready)

```
Build a single-file ultra-premium cinematic scrollytelling website for "JAY'S PIZZA" (wood-fired
Neapolitan pizzeria with Indian-Italian fusion menu, Cambridge ON). Deliver index.html (all CSS/JS inline,
assets in /assets/). Tech stack: GSAP 3 + ScrollTrigger, Lenis smooth scroll, plain HTML5 canvas
(frame-sequence scrubbing, no three.js). Hard requirements:

1. STRUCTURE: body is exactly 5000vh tall on desktop. One fixed, full-viewport <canvas> pinned behind
   everything (position:fixed, inset:0, width/height 100%). A floating UI layer (pointer-events:none,
   children auto) above it with: fixed header (logo "JAY'S PIZZA", "Menu", "Reserve", "Order Now" button),
   a section progress rail (4 numbered ticks, labels: THE BLOOM / THE FIRE / THE FUSION / THE TABLE),
   per-section headline text blocks that fade/slide in-out at defined scroll windows (glassmorphism:
   rgba(26,18,11,0.45) bg, 1px rgba(245,233,215,0.18) border, backdrop-filter blur(14px),
   border-radius 20px), and an end-card (final section only) with "Order Now" CTA + address/phone line.

2. CANVAS SCRUB LOGIC: 4 sequences; two frame tiers ship per sequence — desktop tier at
   /assets/seq-[N]/seq[N]-[###].jpg (1600px wide, JPEG quality 90, hard cap 1MB per frame) and mobile
   tier at /assets/seq-[N]-m/seq[N]-[###].jpg (900px wide, JPEG quality 88, <=600KB), filenames 3-digit
   zero-padded; the page picks the tier once at load by viewport (window.innerWidth < 768 -> mobile tier)
   and never swaps mid-scroll. Each tier holds 240 frames per sequence (24fps extraction from a 10s
   master; scroll gap between frames = 1/24s ≈ 41.7ms of footage — the on-screen scroll distance for
   one frame step is maxScroll/960). Preload seq-1 fully before reveal (show a branded loader with %).
   Lazily preload seq 2,3,4 in background (priority order, sequential batches of 12 via fetch+Image;
   keep an LRU cap of 320 decoded Image objects, evict the previous sequence after transition).
   Scroll mapping: global progress p = scrollY / maxScroll in [0,1]. Section s = floor(p*4) clamped 0..3.
   Local t = (p*4 - s) in [0,1]; frame index = round(t * (framesInSeq - 1)) + 1. Draw current frame
   cover-fit (like background-size:cover) into canvas with devicePixelRatio cap 2. Use one rAF loop;
   only redraw when frame index or size changed. Crossfades: at section boundaries (local t<0.06 or >0.94)
   overlay a white-lift + ember-particle wipe (CSS opacity-driven overlay div; particles = 2D canvas noise),
   never crossfading two video streams.

3. UI STYLE (Cinematic Trattoria): background color #1A120B; type: display serif (Playfair Display) for
   headlines, Inter for UI/body; headline color #F5E9D7; accent red #B33A2B; gold ember #D9A441.
   Glassmorphism cards as specified; buttons: solid #B33A2B with cream text, radius 999px, hover lift
   + 1px cream glow. Section labels in letter-spaced small caps. Mobile: reduce headline scale,
   keep pinned canvas, swap to 0.5 resolution frames under 768px width.

4. BEHAVIOR: Lenis (lerp 0.09) + GSAP ScrollTrigger scrub:1 driving a single onUpdate(progress) ->
   sequencer.setProgress(p). Headline blocks: each fades/slides in-out at its own scroll window with
   y-translate + opacity tweens. End card: pin at 85-100% with scale 0.96->1 reveal. Sound toggle
   (top-right, off by default) plays per-section ambient loop. Reduced-motion prefers-reduced-motion:
   fall back to still keyframe per section + captions. No layout shift; LCP is the seq-1 first frame;
   preload it via <link rel=preload> as image. Add console-safe frame-miss guard: if an image index
   404s, hold the last decoded frame.

Return complete production-ready code, no placeholders, comment the scroll->frame math in English.
```

## VIDEO PROMPTS — FINAL CINEMATIC CUT (Veo 3.1 via VicSee MCP, 10s, zero cuts)

Universal prefix on every prompt: "Single continuous unbroken shot, zero camera cuts, no jump cuts,
no editing cuts of any kind; one smooth constant-speed camera move on a fixed physical path; the same
kitchen, same pizza, same lighting from first frame to last; photoreal cinematic food-film grade,
24fps motion feel; native synchronized ambient sound."

V1 THE BLOOM (first frame = K1): slow steady push-in from 85mm distance toward the hands as they
stretch the dough round on the dark oak counter; flour dust drifts through the dawn light beams; the
dough visibly widens and breathes with each press and turn; ends on the rested dough round glowing
in rim light, ready for the peel. Audio: quiet dawn kitchen, soft dough taps on wood, flour whisper.
Emotional target: tenderness, craft, anticipation.

V2 THE FIRE (first frame = K2): slow lateral arc left-to-right around the oven mouth at hearth level;
the long wooden peel glides in and lays the margherita onto the stone floor; flames fold over the
crust rim, leopard-spot char blooming in real time; embers swirl upward as the peel withdraws. Audio:
deep fire crackle, stone hiss, peel scrape on brick. Emotional target: primal hunger, heat, awe.

V3 THE FUSION (first frame = K3): overhead locked axis, slow descend and gentle rightward drift over
the oak board; steam lifts off the leopard-spotted margherita; a hand enters and places paneer cubes,
then cilantro sprigs beside torn basil; a slow spiral of saffron-tomato chutney drizzles across the
melted cheese, glistening. Audio: crisp crust tick under the knife, soft sizzle, copper cup set down.
Emotional target: fascination, appetite, the two-cultures moment.

V4 THE TABLE (first frame = K4): pure dolly pull-back from close on the finished pie; steam curls off
the paneer-basil fusion pizza; candles, glassware, brick glow resolve into the warm trattoria evening;
camera settles centered above the board, "JAY'S PIZZA" menu card legible, symmetric hero frame. Audio:
warm room ambience, candle flicker, one distant contented laugh. Emotional target: belonging, reward,
"order now" pull.

Duration note: generate 8s + extend-from-last-frame +2s = full 10s where the API allows; else ship 8s
and let the scrub stretch it (41.7ms/frame cadence preserved). 240 frames extracted per 10s master at
24fps (10s × 24fps = 240; the 420 figure was a slip — 420 would be 42fps) into both tiers (desktop q90
<=1MB, mobile <=600KB).

## BUILD PIPELINE (state machine)
1. ✅ Interview (answered: Cambridge KW, Indian-Italian fusion, Jay's Pizza, Neapolitan wood-fire craft)
2. ✅ Keyframes K1–K4 via connected Codex image engine (QC passed)
3. ⬜ Veo 3.1 videos ×4 (VicSee MCP, first frame = approved keyframes) → needs VICSEE_API_KEY
4. ⬜ Frame extraction (ffmpeg 24fps → 240/seq, PIL re-encode q90, desktop ≤1MB / mobile ≤600KB)
5. ⬜ Site build (Codex CLI executes the master prompt above) → QA (web-visual-qa) → launch