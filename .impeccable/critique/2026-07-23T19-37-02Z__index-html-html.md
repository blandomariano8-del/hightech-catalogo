---
target: index.html.html
total_score: 23
max_score: 40
na_heuristics: 
p0_count: 2
p1_count: 2
timestamp: 2026-07-23T19-37-02Z
slug: index-html-html
---
Method: dual-agent (A: design-review sub-agent · B: detector-scan sub-agent)

## Design Health Score

| # | Heuristic | Score | Key Issue |
|---|-----------|-------|-----------|
| 1 | Visibility of System Status | 3/4 | Shipping row permanently shows a literal "—" placeholder that never resolves |
| 2 | Match System / Real World | 3/4 | Payment/pricing conventions fit the Argentine resale market; emoji stand in for real product photos |
| 3 | User Control and Freedom | 2/4 | No Escape-key handling on any modal; closing the success modal silently wipes the cart |
| 4 | Consistency and Standards | 3/4 | Two adjacent controls (qty "+" and the added checkmark) do the identical action on every card |
| 5 | Error Prevention | 1/4 | "¡Pedido confirmado!" is shown before anything reaches the seller; closing it destroys the order with zero confirmation |
| 6 | Recognition Rather Than Recall | 3/4 | Category-count feature is fully coded but wired to DOM ids that don't exist — always a no-op |
| 7 | Flexibility and Efficiency | 2/4 | No saved contact info / localStorage — every repeat order re-types everything from zero |
| 8 | Aesthetic and Minimalist Design | 2/4 | Clean type scale, but emoji-as-icon used everywhere; detector independently flags Inter as the sole font with no pairing for hierarchy |
| 9 | Error Recovery | 2/4 | No fallback if the WhatsApp popup is blocked on mobile — silent failure at the highest-stakes step |
| 10 | Help and Documentation | 2/4 | FAQ content is genuinely good, but its only entry point (`.btn-faq`) is hidden at ≤600px — exactly the dominant device class |
| **Total** | | **23/40** | **Acceptable — significant improvements needed** |

## Design Specificity Verdict

**LLM assessment:** Hybrid. The business logic — WhatsApp-based checkout, Argentina-specific payment methods (pesos/USD/transferencia/crypto), and FAQ content addressing real used-phone/warranty anxieties — is genuinely authored for this vendor. The visual system is not: navy hero + blue radial "signature arc," rounded-card tokens, Inter, badge pills — this is interchangeable 2023 SaaS-template styling that could be reskinned for any category with a find-and-replace. The biggest miss: a store whose entire value proposition is "we sell Apple products" shows zero product photography, using stock emoji (📱🎧📲) instead — nothing here visually says "Apple reseller," and nothing shows this is a real Rosario storefront (no address, photo, or owner presence anywhere).

**Deterministic scan:** `detect.mjs --json` on `index.html.html` returned exit code 2 (findings present), 19 total hits across 2 rules:
- `overused-font` × 18 — every selector re-declaring `font-family: 'Inter', sans-serif` instead of inheriting from `body` (line 34); Inter is flagged as one of the handful of faces every AI-generated UI converges on.
- `single-font` × 1 — no second face exists anywhere to carry hierarchy.

Both rules trace to the same root fact (Inter is the only font, restated by inheritance-avoidance across ~17 selectors), so treat this as **one design decision, not 18 independent problems** — the count is inflated by CSS-authoring redundancy, not severity. No color/contrast/structural/accessibility rules fired in this detector's ruleset. This is a case of the detector catching something the design review didn't explicitly name: font monotony as a distinct, independently-fixable issue from the emoji/photography problem.

**Visual overlays:** Not available. No browser automation tool (Playwright/Puppeteer/MCP browser) exists in this session, so live-server injection and in-browser overlays were skipped per protocol — this critique is based on static source reading only, not a rendered/visual pass.

## Overall Impression

The commerce mechanics are well-built for a no-backend, WhatsApp-first small business — but the page currently tells the customer their order is confirmed before it actually is, and destroys that order on a stray tap. That's the single biggest risk: not a polish issue, a lost-sale issue. The visual shell around it is competent but generic, and doesn't yet look like it belongs to an Apple reseller specifically.

## What's Working

1. **The WhatsApp message construction** (`enviarWhatsapp()`) — bold labels, emoji anchors, itemized subtotal, running total, all pre-filled so the customer never types a manual order. This directly removes friction from the one channel that actually closes sales here.
2. **The printable PDF order summary** (`verPedidoPDF()`) — a smart low-tech receipt substitute for a system with no backend or accounts, auto-triggering print in a clean branded window.
3. **Defensive image fallback** — broken/missing image URLs degrade to an emoji instead of a broken-image icon (line 858), a correctly engineered small detail.

## Priority Issues

**[P0] Hero cards are hardcoded and desynced from the real catalog; WhatsApp number looks like an unreplaced placeholder**
- **Why it matters:** The hero shows "iPhone 15 128GB — USD $560" while the real catalog (`PRODUCTOS`) prices the same item at $600, and lists an "iPhone 16" that doesn't exist in the catalog at all. For an unfamiliar small vendor selling $1000+ phones, a shopper catching a price mismatch two seconds apart reads as bait-and-switch. Separately, `wa.me/5493415000000` is a suspiciously round number matching the same placeholder pattern as the form's example phone — if it's not the real business line, every order vanishes silently.
- **Fix:** Generate hero cards from `PRODUCTOS` at render time instead of hand-typing them; extract the WhatsApp number into one named constant and verify it's the real number before launch.
- **Suggested command:** `/impeccable harden`

**[P0] "Pedido confirmado" misstates state, and closing it destroys the cart with no confirmation**
- **Why it matters:** `confirmarPedido()` only validates the form and stores state locally — nothing has reached the seller yet — but the modal is titled "¡Pedido confirmado!". `cerrarSuccess()`, triggered by the close button *or* a backdrop tap, unconditionally clears `cart` with no gate on whether WhatsApp send ever happened. A stray tap (likely on mobile, where the pattern of backdrop-tap-to-close is already trained by the cart panel) permanently loses the order while the customer believes, from the screen's own title, that it already succeeded.
- **Fix:** Retitle the screen to reflect real state until WhatsApp send is confirmed (e.g. "Casi listo — confirmá por WhatsApp"); gate cart-clearing on the WhatsApp tap actually firing; require explicit confirmation before clearing on close.
- **Suggested command:** `/impeccable harden`

**[P1] FAQ access disappears on mobile, and category filtering has no mobile equivalent**
- **Why it matters:** `.btn-faq { display: none }` at ≤600px removes the only FAQ entry point on phones; `.navbar-cats { display: none }` at ≤768px removes all category quick-filters with nothing replacing them. This audience is overwhelmingly mobile (WhatsApp-first commerce), and the FAQ is exactly where warranty/used-phone-reliability anxiety gets addressed — cutting it off removes reassurance at the point of highest need, on the dominant device.
- **Fix:** Replace the hidden FAQ button with a persistent icon next to the cart icon; surface category chips on mobile using the already-styled-but-unused `.filters-bar`/`.filter-btn` classes.
- **Suggested command:** `/impeccable adapt`

**[P1] Redundant add-to-cart control, plus dead category-count code**
- **Why it matters:** Once an item is added, the qty-control's own "+" and the adjacent added-checkmark button both call the identical `changeQty(id,1)` side by side on every card — on the single most frequent interaction on the page, reading as broken. Separately, `updateCounts()` and the fully-styled `.filter-count` CSS reference `count-${c}` DOM ids that don't exist anywhere in the HTML — this "feature" has always been a no-op, and is a maintenance trap for whoever edits the file next.
- **Fix:** Collapse the added-item row to one qty stepper; either wire the count/filter-bar feature to real DOM output or delete the unused CSS/JS.
- **Suggested command:** `/impeccable clarify`

**[P2] No real product photography; emoji fallback undercuts a premium, high-trust purchase**
- **Why it matters:** 4 of 5 catalog entries have empty or unverified local image paths, falling back to a single large emoji on a flat gray gradient — the same pattern repeats in hero cards and cart items. Buyers are asked to hand over $600–$1300 in cash/crypto to an unfamiliar small vendor; stock emoji directly undercuts the "Garantía escrita / Equipos verificados" trust claims stated three lines above it.
- **Fix:** Require real photos before launch (the `driveUrl()` Drive-link helper is already built for this and currently unused); until photos exist, use a branded "Foto próximamente" placeholder instead of an emoji.
- **Suggested command:** `/impeccable polish`

## Persona Red Flags

**Jordan (first-timer):** Sees iPhone 15 usado at $560 in the hero, then $600 in the catalog seconds later — reads as bait-and-switch from a vendor they have no prior relationship with. Fills the full checkout form, taps "Confirmar pedido," and is told the order is confirmed with no indication a second manual step (tap WhatsApp, then hit Send) is still required — likely closes the tab believing the purchase is done. No address, hours, or social proof anywhere before the form asks for name and phone.

**Sam (accessibility-dependent):** Category buttons and badges rely on bare emoji with no `aria-label`. None of the three modals have `role="dialog"`, `aria-modal`, or a focus trap, and there is no Escape-key handler anywhere. Form validation toggles a `.show` class with no `aria-live` region and no `aria-invalid`/`aria-describedby` — a screen-reader user gets no spoken feedback that a field just failed validation. Invalid state is signaled by red border-color alone, no icon or non-color indicator.

**Casey (mobile-user):** FAQ access and category filters both disappear at mobile breakpoints with nothing replacing them. The cart panel goes full-width (100vw) on mobile with backdrop-tap-to-close trained behavior, making an accidental thumb tap far more likely to trigger the cart-wipe bug than on desktop. The (mismatched) hero product cards are hidden on mobile too — meaning the pricing-drift bug currently only shows on desktop, but stays live underneath.

## Minor Observations

- No `prefers-reduced-motion` guard on the smooth-scroll, pulse, or float animations.
- `IMAGES_BASE_URL` is declared but never referenced anywhere in the script — dead config.
- Image paths like `iphone17-pro-orange.jpg.png` have a double extension — worth confirming these actually resolve.
- The shipping row always renders a literal "—" that never resolves to a number.
- Three near-duplicate iPhone 17 Pro Max entries (differing only by color) each consume a full grid slot — no color-swatch/variant pattern; won't scale as more colors/tiers are added.
- `driveUrl()` is a well-built Drive-link-to-direct-image utility, but zero catalog entries currently use it.
- Font monotony (detector-confirmed): Inter is redeclared in ~17 separate selectors instead of inheriting from `body` — one design decision multiplied into 18 mechanical findings; fixing the font choice once addresses all of them.

## Questions to Consider

1. If the WhatsApp send is the actual order, why does the site perform an in-browser "confirmation" step before that send happens — would collapsing these into one single moment remove the exact trust gap that's likely costing completed sales?
2. Hero content, catalog data, and the WhatsApp number are currently maintained in three disconnected places by hand — what would it take to make `PRODUCTOS` plus one named constant the single source of truth all three derive from?
3. This page positions itself as the trustworthy alternative to buying a $1300 phone from a stranger — so why is every element that could prove "this is a real, professional Rosario store" (storefront photo, owner's face, unboxing shot) replaced by system emoji?
