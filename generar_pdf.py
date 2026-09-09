#!/usr/bin/env python3
"""Genera HIGHTECH-lista-precios-mayorista.pdf"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph,
    Table, TableStyle, Spacer, KeepTogether
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from datetime import date
import os

# ── Colores de marca ──────────────────────────────────────────
NAVY  = colors.HexColor("#000E23")
BLUE  = colors.HexColor("#0050ED")
NAVY2 = colors.HexColor("#0A2060")
GRAY  = colors.HexColor("#F4F4F5")
LGRAY = colors.HexColor("#E5E7EB")
GRAY2 = colors.HexColor("#6B7280")
BLUEL = colors.HexColor("#8BA3D4")
CONDBG= colors.HexColor("#EEF3FF")
WHITE = colors.white
BLACK = colors.HexColor("#111111")

# ── Fuentes ───────────────────────────────────────────────────
FONT_DIR = "/private/tmp/claude-501/-Users-macbook-Documents-GitHub-hightech-catalogo/fd657560-bb6d-406b-887f-2b0ccf45b267/scratchpad/fonts"

for name, fname in [
    ("Poppins-Regular",    "Poppins-Regular.ttf"),
    ("Poppins-Bold",       "Poppins-Bold.ttf"),
    ("Poppins-SemiBold",   "Poppins-SemiBold.ttf"),
    ("IBMPlexMono",        "IBMPlexMono-Regular.ttf"),
    ("IBMPlexMono-Bold",   "IBMPlexMono-Bold.ttf"),
]:
    pdfmetrics.registerFont(TTFont(name, os.path.join(FONT_DIR, fname)))

# ── Datos ─────────────────────────────────────────────────────
PRODUCTOS = [
    # IPHONES SELLADOS
    {"cat":"iphones","nombre":"iPhone 17 256GB",         "caracteristicas":"White",                          "disponibilidad":"disponible","precioStock":990},
    {"cat":"iphones","nombre":"iPhone 17 256GB",         "caracteristicas":"Black",                          "disponibilidad":"disponible","precioStock":990},
    {"cat":"iphones","nombre":"iPhone 17 Pro 256GB",     "caracteristicas":"Cosmic Orange",                  "disponibilidad":"disponible","precioStock":1190},
    {"cat":"iphones","nombre":"iPhone 17 Pro 256GB",     "caracteristicas":"Silver",                         "disponibilidad":"disponible","precioStock":1250},
    {"cat":"iphones","nombre":"iPhone 17 Pro 256GB",     "caracteristicas":"Deep Blue",                      "disponibilidad":"disponible","precioStock":1250},
    {"cat":"iphones","nombre":"iPhone 17 Pro Max 256GB", "caracteristicas":"Silver",                         "disponibilidad":"disponible","precioStock":1350},
    {"cat":"iphones","nombre":"iPhone 17 Pro Max 256GB", "caracteristicas":"Blue Titanium",                  "disponibilidad":"disponible","precioStock":1350},
    # USADOS
    {"cat":"usados", "nombre":"iPhone 14 128GB",         "caracteristicas":"Celeste · Bateria 100%",         "disponibilidad":"disponible","precioStock":410},
    {"cat":"usados", "nombre":"iPhone 15 128GB",         "caracteristicas":"Black · Bateria 83%",            "disponibilidad":"disponible","precioStock":490},
    {"cat":"usados", "nombre":"iPhone 15 128GB",         "caracteristicas":"Pink · Bateria 80%",             "disponibilidad":"vendido",   "precioStock":490},
    {"cat":"usados", "nombre":"iPhone 15 Pro 128GB",     "caracteristicas":"Blue Titanium · Bateria 87%",    "disponibilidad":"disponible","precioStock":610},
    {"cat":"usados", "nombre":"iPhone 15 Pro 128GB",     "caracteristicas":"Natural Titanium · Bateria 86%", "disponibilidad":"disponible","precioStock":610},
    {"cat":"usados", "nombre":"iPhone 15 Pro Max 256GB", "caracteristicas":"Blue Titanium · Bateria 87%",    "disponibilidad":"disponible","precioStock":710},
    {"cat":"usados", "nombre":"iPhone 16 128GB",         "caracteristicas":"Ultramarine · Bateria 100%",     "disponibilidad":"disponible","precioStock":650},
    {"cat":"usados", "nombre":"iPhone 16 Pro 128GB",     "caracteristicas":"Desert · Bateria 93%",           "disponibilidad":"disponible","precioStock":830},
    {"cat":"usados", "nombre":"iPhone 16 Pro 128GB",     "caracteristicas":"White Titanium · Bateria 91%",   "disponibilidad":"disponible","precioStock":810},
    # MACBOOK
    {"cat":"macbook","nombre":"MacBook Neo 256GB",       "caracteristicas":"Silver",                         "disponibilidad":"disponible","precioStock":850},
    {"cat":"macbook","nombre":'MacBook Air M5 13"',      "caracteristicas":"16GB RAM · 512GB · Midnight",    "disponibilidad":"disponible","precioStock":1450},
    # AIRPODS
    {"cat":"airpods","nombre":"AirPods Pro 3",           "caracteristicas":"USB-C",                          "disponibilidad":"disponible","precioStock":270},
    {"cat":"airpods","nombre":"AirPods 4",               "caracteristicas":"Active Noise Cancellation",      "disponibilidad":"disponible","precioStock":210},
    {"cat":"airpods","nombre":"AirPods Max (2nd Gen)",   "caracteristicas":"2026 · USB-C",                   "disponibilidad":"disponible","precioStock":600},
    # IPAD
    {"cat":"ipad",   "nombre":"iPad A16 128GB",          "caracteristicas":"Chip A16",                       "disponibilidad":"disponible","precioStock":500},
    {"cat":"ipad",   "nombre":"iPad A16 256GB",          "caracteristicas":"Chip A16",                       "disponibilidad":"disponible","precioStock":610},
    {"cat":"ipad",   "nombre":'iPad Air 11" M4 128GB',   "caracteristicas":"Chip M4 · 11 pulgadas",          "disponibilidad":"disponible","precioStock":850},
    {"cat":"ipad",   "nombre":'iPad Air 11" M4 256GB',   "caracteristicas":"Chip M4 · 11 pulgadas",          "disponibilidad":"disponible","precioStock":950},
    {"cat":"ipad",   "nombre":"iPad Pro M5 256GB",       "caracteristicas":"Chip M5 · OLED",                 "disponibilidad":"disponible","precioStock":1250},
    # APPLE WATCH
    {"cat":"applewatch","nombre":"Apple Watch Series 11","caracteristicas":"42mm · Black",                   "disponibilidad":"disponible","precioStock":390},
    {"cat":"applewatch","nombre":"Apple Watch Series 11","caracteristicas":"46mm · Black",                   "disponibilidad":"vendido",   "precioStock":430},
    {"cat":"applewatch","nombre":"Apple Watch Ultra 3",  "caracteristicas":"49mm · Titanio · 2025",          "disponibilidad":"disponible","precioStock":820},
    # SAMSUNG
    {"cat":"samsung","nombre":"Samsung S25 Ultra",       "caracteristicas":"12GB RAM · 256GB · Black",       "disponibilidad":"disponible","precioStock":950},
    {"cat":"samsung","nombre":"Samsung S26 Ultra",       "caracteristicas":"12GB RAM · 512GB · Black",       "disponibilidad":"disponible","precioStock":1250},
    # ACCESORIOS
    {"cat":"accesorios","nombre":"Apple Pencil Pro",     "caracteristicas":"2a Generacion",                  "disponibilidad":"vendido",   "precioStock":140},
    {"cat":"accesorios","nombre":"AirTag",               "caracteristicas":"x1",                             "disponibilidad":"disponible","precioStock":40},
    {"cat":"accesorios","nombre":"Cargador 20W",         "caracteristicas":"USB-C · Original Apple",         "disponibilidad":"disponible","precioStock":50},
    {"cat":"accesorios","nombre":"Cable USB-C",          "caracteristicas":"Original Apple · 1m",            "disponibilidad":"disponible","precioStock":20},
    {"cat":"accesorios","nombre":"Funda MagSafe",        "caracteristicas":"Compatible iPhone",              "disponibilidad":"disponible","precioStock":5},
    {"cat":"accesorios","nombre":"Templado",             "caracteristicas":"Vidrio templado · iPhone",       "disponibilidad":"disponible","precioStock":3},
    {"cat":"accesorios","nombre":"Funda Silicon",        "caracteristicas":"Compatible iPhone",              "disponibilidad":"disponible","precioStock":5},
]

CAT_ORDER = ["iphones","usados","macbook","airpods","ipad","applewatch","samsung","accesorios"]
CAT_LABELS = {
    "iphones":    "iPhones Sellados · Nuevos",
    "usados":     "iPhones Usados Verificados",
    "macbook":    "MacBooks",
    "airpods":    "AirPods",
    "ipad":       "iPads",
    "applewatch": "Apple Watch",
    "samsung":    "Samsung",
    "accesorios": "Accesorios",
}

def qty_prices(base):
    return [f"USD {base}", f"USD {base-10}", f"USD {base-20}", f"USD {base-25}"]

TODAY  = date.today().strftime("%d/%m/%Y")
OUTPUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "HIGHTECH-lista-precios-mayorista.pdf")
PAGE_W, PAGE_H = A4
MARGIN = 20 * mm

# ── Estilos ───────────────────────────────────────────────────
def ps(name, font, size, color=BLACK, align=TA_LEFT, leading=None):
    return ParagraphStyle(name, fontName=font, fontSize=size,
        textColor=color, alignment=align,
        leading=leading or round(size * 1.35, 1))

sCatHead = ps("sCatH",  "Poppins-Bold",    9.5, WHITE, TA_LEFT, 13)
sColHdr  = ps("sColH",  "Poppins-Bold",    7.5, WHITE, TA_CENTER, 10)
sModel   = ps("sModel", "Poppins-SemiBold",8.5, BLACK, TA_LEFT, 12)
sSub     = ps("sSub",   "Poppins-Regular", 6.8, GRAY2, TA_LEFT,  9)
sPrice   = ps("sPrice", "IBMPlexMono-Bold",8.5, BLUE,  TA_CENTER,11)
sPriceNA = ps("sNA",    "IBMPlexMono",     7.5, GRAY2, TA_CENTER,10)
sCondB   = ps("sCond",  "Poppins-Regular", 8,   BLACK, TA_LEFT,  12)

# ── Header / Footer ───────────────────────────────────────────
def draw_page(canvas, doc):
    canvas.saveState()
    w, h = A4
    band = 17 * mm

    # header band
    canvas.setFillColor(NAVY)
    canvas.rect(0, h - band, w, band, fill=1, stroke=0)

    # accent stripe
    canvas.setFillColor(BLUE)
    canvas.rect(0, h - band - 1.2*mm, w, 1.2*mm, fill=1, stroke=0)

    # brand name
    canvas.setFillColor(WHITE)
    canvas.setFont("Poppins-Bold", 13)
    canvas.drawString(MARGIN, h - 9.5*mm, "HIGHTECH ROSARIO")
    canvas.setFont("Poppins-Regular", 7)
    canvas.setFillColor(BLUEL)
    canvas.drawString(MARGIN, h - 13.5*mm, "LISTA DE PRECIOS MAYORISTA")

    # date
    canvas.setFont("Poppins-Regular", 7.5)
    canvas.setFillColor(BLUEL)
    canvas.drawRightString(w - MARGIN, h - 9*mm, TODAY)

    # footer line
    canvas.setStrokeColor(LGRAY)
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN, 13.5*mm, w - MARGIN, 13.5*mm)

    # footer text
    canvas.setFont("Poppins-Regular", 6.8)
    canvas.setFillColor(GRAY2)
    canvas.drawCentredString(
        w / 2, 9*mm,
        f"HIGHTECH ROSARIO  ·  Puerto Norte, Rosario  ·  @hightech.rosario  ·  pag. {doc.page}"
    )
    canvas.restoreState()

# ── Documento ─────────────────────────────────────────────────
def build():
    doc = BaseDocTemplate(
        OUTPUT, pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=24*mm, bottomMargin=19*mm,
    )
    frame = Frame(MARGIN, 19*mm, PAGE_W - 2*MARGIN, PAGE_H - 43*mm, id="main")
    doc.addPageTemplates([PageTemplate(id="p", frames=[frame], onPage=draw_page)])

    story = []
    col_w = PAGE_W - 2*MARGIN
    # Widths: modelo 44%, 4x precio 14% cada uno
    cw = [col_w*0.44, col_w*0.14, col_w*0.14, col_w*0.14, col_w*0.14]

    # ── Bloque de condiciones ──
    cond_para = Paragraph(
        "<b>Metodos de pago:</b> USDT / USDC &nbsp;·&nbsp; Transferencia en pesos (+3%) &nbsp;·&nbsp; "
        "Efectivo (pesos o dolares).<br/>"
        "Los equipos se pueden <b>MIXEAR</b> &nbsp;·&nbsp; precios por cantidad &nbsp;·&nbsp; "
        "precios sujetos a cambio sin previo aviso.", sCondB)
    cond_tbl = Table([[cond_para]], colWidths=[col_w])
    cond_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), CONDBG),
        ("BOX",           (0,0),(-1,-1), 0.8, BLUE),
        ("LEFTPADDING",   (0,0),(-1,-1), 10),
        ("RIGHTPADDING",  (0,0),(-1,-1), 10),
        ("TOPPADDING",    (0,0),(-1,-1), 7),
        ("BOTTOMPADDING", (0,0),(-1,-1), 7),
    ]))
    story.append(cond_tbl)
    story.append(Spacer(1, 5*mm))

    # ── Tablas por categoría ──
    by_cat = {}
    for p in PRODUCTOS:
        by_cat.setdefault(p["cat"], []).append(p)

    for cat in CAT_ORDER:
        prods = by_cat.get(cat, [])
        if not prods:
            continue

        # Encabezado de categoría (fila ancha navy)
        cat_lbl = Table(
            [[Paragraph(CAT_LABELS[cat].upper(), sCatHead)]],
            colWidths=[col_w],
        )
        cat_lbl.setStyle(TableStyle([
            ("BACKGROUND",    (0,0),(-1,-1), NAVY),
            ("LEFTPADDING",   (0,0),(-1,-1), 10),
            ("TOPPADDING",    (0,0),(-1,-1), 5),
            ("BOTTOMPADDING", (0,0),(-1,-1), 5),
        ]))

        # Fila de cabeceras de columna
        hdr = [
            Paragraph("MODELO / VARIANTE", sColHdr),
            Paragraph("x1", sColHdr),
            Paragraph("x3  (-10)", sColHdr),
            Paragraph("x5  (-20)", sColHdr),
            Paragraph("x10 (-25)", sColHdr),
        ]

        rows = [hdr]
        ts = [
            ("BACKGROUND",    (0,0),(-1,0), NAVY2),
            ("TOPPADDING",    (0,0),(-1,0), 5),
            ("BOTTOMPADDING", (0,0),(-1,0), 5),
            ("LEFTPADDING",   (0,0),(0,0),  10),
            ("VALIGN",        (0,0),(-1,-1),"MIDDLE"),
            ("LINEBELOW",     (0,0),(-1,-1), 0.25, LGRAY),
            ("BOX",           (0,0),(-1,-1), 0.5, LGRAY),
        ]

        for i, p in enumerate(prods):
            ri = i + 1
            bg = WHITE if i % 2 == 0 else GRAY
            ts.append(("BACKGROUND", (0,ri),(-1,ri), bg))
            ts.append(("TOPPADDING",    (0,ri),(-1,ri), 5))
            ts.append(("BOTTOMPADDING", (0,ri),(-1,ri), 5))
            ts.append(("LEFTPADDING",   (0,ri),(0,ri),  10))

            model_cell = [Paragraph(p["nombre"], sModel),
                          Paragraph(p["caracteristicas"], sSub)]

            if p["disponibilidad"] == "vendido":
                price_cells = [Paragraph("VENDIDO", sPriceNA)] + [Paragraph("—", sPriceNA)]*3
            else:
                price_cells = [Paragraph(v, sPrice) for v in qty_prices(p["precioStock"])]

            rows.append([model_cell] + price_cells)

        tbl = Table(rows, colWidths=cw, repeatRows=1)
        tbl.setStyle(TableStyle(ts))

        story.append(KeepTogether([cat_lbl, tbl]))
        story.append(Spacer(1, 4*mm))

    doc.build(story)
    print(f"PDF listo: {OUTPUT}")

build()
