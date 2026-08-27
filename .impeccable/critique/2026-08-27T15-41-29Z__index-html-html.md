---
target: index.html.html
total_score: 25
max_score: 40
na_heuristics: 
p0_count: 2
p1_count: 2
timestamp: 2026-08-27T15-41-29Z
slug: index-html-html
---
## Design Health Score

| # | Heuristic | Score | Key Issue |
|---|-----------|-------|-----------|
| 1 | Visibility of System Status | 3 | Toast y cart badge OK. Sin loading state en red lenta. |
| 2 | Match System / Real World | 3 | Voseo correcto, registro local. |
| 3 | User Control and Freedom | 3 | Modales cierran. Sin undo en borrado de carrito. |
| 4 | Consistency and Standards | 2 | 3 colores de precio distintos. Hero con 3 paletas. Radios inconsistentes. |
| 5 | Error Prevention | 3 | Validación inline correcta. Sin confirm al borrar ítem. |
| 6 | Recognition Rather Than Recall | 3 | Categorías visibles. "EN STOCK" en todos es ruido. |
| 7 | Flexibility and Efficiency | 2 | Sin atajos. Stepper requiere 3 taps. |
| 8 | Aesthetic and Minimalist Design | 1 | 37 emojis, 7 gradientes, 3 glassmorphism, 3 paletas en hero. |
| 9 | Error Recovery | 2 | Mensajes específicos OK. confirm() nativo rompe la superficie. |
| 10 | Help and Documentation | 3 | FAQ accesible. Botón FAQ sin label en mobile. |
| **Total** | | **25/40** | **Acceptable** |

## Design Specificity Verdict
Completamente intercambiable. 0/5 colores de marca coinciden. Inter en todo el sitio, Poppins e IBM Plex Mono no cargadas. 37 emojis, 7 gradientes, 3 backdrop-filter/blur. El detector encontró 19 findings: 18× overused-font, 1× single-font, 1× dark-glow.

## Overall Impression
El sitio funciona como catálogo pero visualmente es un kit genérico de "tienda Apple". La acumulación de emojis, gradientes y glassmorphism destruye cualquier señal de premium.

## What's Working
1. El flujo WhatsApp es correcto para el mercado.
2. El filtrado por categorías es genuinamente rápido.
3. El copy tiene el registro correcto con voseo consistente.

## Priority Issues

**[P0] Fuentes completamente equivocadas** — Inter en todo, Poppins e IBM Plex Mono sin cargar. Fix: reemplazar imports y aplicar sistema tipográfico del manual.

**[P0] Paleta de colores completamente fuera de marca** — 0/5 brand colors match. Fix: reescribir variables CSS con valores exactos del manual.

**[P1] 37 emojis en todo el sitio** — Fix: SVG inline con disc sólido según sistema de iconografía del manual.

**[P1] Hero con 3 mundos visuales incompatibles** — Descuento -20% factualmente incorrecto (es ~4.8%). Fix: colapsar a un hero único en paleta navy/azul.

**[P2] Precios inconsistentes y fuera de formato** — Fix: Poppins Bold 700, #0050ED, con span USD en gris.

## Persona Red Flags
- Casey: hero derecho desaparece en mobile, btn-faq 32px (bajo mínimo 44pt)
- Jordan: "Batería 87%" sin contexto, FAQ icon-only sin label, "Ya casi" genera ansiedad
- Riley: descuento -20% incorrecto, confirm() nativo bloqueado en algunos browsers

## Minor Observations
- backdrop-filter en hero-badge (glassmorphism)
- Footer invisible como anchor de confianza
- PDF usa font-family: sans-serif, pierde tipografía de marca
- Eyebrow tracked uppercase en 2 de 3 slides (patrón prohibido)
- CAT_EMOJI hardcoded en JS, necesita reemplazo SVG

## Questions to Consider
- El hero vende tres cosas distintas — elegir una sería más convincente
- Sin emojis ni gradientes, ¿qué queda de identidad visual?
- El -20% en el slide de oferta es factualmente incorrecto
