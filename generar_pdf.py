#!/usr/bin/env python3
"""Genera HIGHTECH-lista-precios-mayorista.pdf"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph,
    Table, TableStyle, Spacer, KeepTogether, Image as RLImage
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT, TA_CENTER
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
    ("Poppins-Regular",  "Poppins-Regular.ttf"),
    ("Poppins-Bold",     "Poppins-Bold.ttf"),
    ("Poppins-SemiBold", "Poppins-SemiBold.ttf"),
    ("IBMPlexMono",      "IBMPlexMono-Regular.ttf"),
    ("IBMPlexMono-Bold", "IBMPlexMono-Bold.ttf"),
]:
    pdfmetrics.registerFont(TTFont(name, os.path.join(FONT_DIR, fname)))

# ── Rutas ─────────────────────────────────────────────────────
REPO    = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(REPO, "img")
OUTPUT  = os.path.join(REPO, "HIGHTECH-lista-precios-mayorista.pdf")

IMG_SIZE = 15 * mm  # thumbnail cuadrado

def img_cell(rel_path):
    """Devuelve un RLImage listo para insertar en tabla, o cadena vacía si falla."""
    if not rel_path:
        return ""
    full = os.path.join(REPO, rel_path.lstrip("./"))
    if not os.path.exists(full):
        return ""
    try:
        return RLImage(full, width=IMG_SIZE, height=IMG_SIZE, kind="proportional")
    except Exception:
        return ""

# ── Productos (con ruta de imagen) ───────────────────────────
PRODUCTOS = [
    # IPHONES SELLADOS
    {"cat":"iphones","nombre":"iPhone 17 256GB",         "caracteristicas":"White",                          "disp":"disponible","precio":990,  "img":"img/iphone17-white.jpg"},
    {"cat":"iphones","nombre":"iPhone 17 256GB",         "caracteristicas":"Black",                          "disp":"disponible","precio":990,  "img":"img/iphone17-black.png"},
    {"cat":"iphones","nombre":"iPhone 17 Pro 256GB",     "caracteristicas":"Cosmic Orange",                  "disp":"disponible","precio":1250, "img":"img/iphone17-pro-orange.jpg"},
    {"cat":"iphones","nombre":"iPhone 17 Pro 256GB",     "caracteristicas":"Silver",                         "disp":"disponible","precio":1250, "img":"img/iphone17-pro-silver.jpg"},
    {"cat":"iphones","nombre":"iPhone 17 Pro 256GB",     "caracteristicas":"Deep Blue",                      "disp":"disponible","precio":1250, "img":"img/iphone17-pro-blue.jpg"},
    {"cat":"iphones","nombre":"iPhone 17 Pro Max 256GB", "caracteristicas":"Silver",                         "disp":"disponible","precio":1350, "img":"img/iphone17-pm-silver.jpg"},
    {"cat":"iphones","nombre":"iPhone 17 Pro Max 256GB", "caracteristicas":"Blue Titanium",                  "disp":"disponible","precio":1350, "img":"img/iphone17-pm-blue.jpg"},
    # USADOS
    {"cat":"usados", "nombre":"iPhone 14 128GB",         "caracteristicas":"Celeste · Bateria 100%",         "disp":"disponible","precio":410,  "img":"img/iphone14-celeste.jpg"},
    {"cat":"usados", "nombre":"iPhone 15 128GB",         "caracteristicas":"Black · Bateria 83%",            "disp":"disponible","precio":490,  "img":"img/iphone15-black.jpg"},
    {"cat":"usados", "nombre":"iPhone 15 128GB",         "caracteristicas":"Pink · Bateria 80%",             "disp":"vendido",   "precio":490,  "img":"img/iphone15-pink.jpg"},
    {"cat":"usados", "nombre":"iPhone 15 Pro 128GB",     "caracteristicas":"Blue Titanium · Bateria 87%",    "disp":"disponible","precio":610,  "img":"img/iphone15-pro-blue.jpg"},
    {"cat":"usados", "nombre":"iPhone 15 Pro 128GB",     "caracteristicas":"Natural Titanium · Bateria 86%", "disp":"disponible","precio":610,  "img":"img/iphone15-pro-natural.jpg"},
    {"cat":"usados", "nombre":"iPhone 15 Pro Max 256GB", "caracteristicas":"Blue Titanium · Bateria 87%",    "disp":"disponible","precio":710,  "img":"img/iphone15-pro-blue.jpg"},
    {"cat":"usados", "nombre":"iPhone 16 128GB",         "caracteristicas":"Ultramarine · Bateria 100%",     "disp":"disponible","precio":650,  "img":"img/iphone16-ultramarine.jpg"},
    {"cat":"usados", "nombre":"iPhone 16 Pro 128GB",     "caracteristicas":"Desert · Bateria 93%",           "disp":"disponible","precio":830,  "img":"img/iphone16-pro-desert.jpg"},
    {"cat":"usados", "nombre":"iPhone 16 Pro 128GB",     "caracteristicas":"White Titanium · Bateria 91%",   "disp":"disponible","precio":810,  "img":"img/iphone16-pro-white.png"},
    # MACBOOK
    {"cat":"macbook","nombre":"MacBook Neo 256GB",       "caracteristicas":"Silver",                         "disp":"disponible","precio":850,  "img":"img/macbook-neo-silver.png"},
    {"cat":"macbook","nombre":'MacBook Air M5 13"',      "caracteristicas":"16GB RAM · 512GB · Midnight",    "disp":"disponible","precio":1450, "img":"img/macbook-air-m5-13.png"},
    # AIRPODS
    {"cat":"airpods","nombre":"AirPods Pro 3",           "caracteristicas":"USB-C",                          "disp":"disponible","precio":270,  "img":"img/airpods-pro-3.png"},
    {"cat":"airpods","nombre":"AirPods 4",               "caracteristicas":"Active Noise Cancellation",      "disp":"disponible","precio":210,  "img":"img/airpods-4-anc.png"},
    {"cat":"airpods","nombre":"AirPods Max (2nd Gen)",   "caracteristicas":"2026 · USB-C",                   "disp":"disponible","precio":600,  "img":"img/airpods-max-2.png"},
    # IPAD
    {"cat":"ipad",   "nombre":"iPad A16 128GB",          "caracteristicas":"Chip A16",                       "disp":"disponible","precio":500,  "img":"img/ipad-a16-128gb.png"},
    {"cat":"ipad",   "nombre":"iPad A16 256GB",          "caracteristicas":"Chip A16",                       "disp":"disponible","precio":610,  "img":"img/ipad-a16-256gb.png"},
    {"cat":"ipad",   "nombre":'iPad Air 11" M4 128GB',   "caracteristicas":"Chip M4 · 11 pulgadas",          "disp":"disponible","precio":850,  "img":"img/ipad-air11-m4-128gb.png"},
    {"cat":"ipad",   "nombre":'iPad Air 11" M4 256GB',   "caracteristicas":"Chip M4 · 11 pulgadas",          "disp":"disponible","precio":950,  "img":"img/ipad-air11-m4-256gb.png"},
    {"cat":"ipad",   "nombre":"iPad Pro M5 256GB",       "caracteristicas":"Chip M5 · OLED",                 "disp":"disponible","precio":1250, "img":"img/ipad-pro-m5-256gb.png"},
    # APPLE WATCH
    {"cat":"applewatch","nombre":"Apple Watch Series 11","caracteristicas":"42mm · Black",                   "disp":"disponible","precio":390,  "img":"img/apple-watch-s11-42mm.png"},
    {"cat":"applewatch","nombre":"Apple Watch Series 11","caracteristicas":"46mm · Black",                   "disp":"vendido",   "precio":430,  "img":"img/apple-watch-s11-46mm.png"},
    {"cat":"applewatch","nombre":"Apple Watch Ultra 3",  "caracteristicas":"49mm · Titanio · 2025",          "disp":"disponible","precio":820,  "img":"img/apple-watch-ultra-3-49mm.png"},
    # SAMSUNG
    {"cat":"samsung","nombre":"Samsung S25 Ultra",       "caracteristicas":"12GB RAM · 256GB · Black",       "disp":"disponible","precio":950,  "img":"img/samsung-s25-ultra-black.png"},
    {"cat":"samsung","nombre":"Samsung S26 Ultra",       "caracteristicas":"12GB RAM · 512GB · Black",       "disp":"disponible","precio":1250, "img":"img/samsung-s26-ultra-black.png"},
    # ACCESORIOS
    {"cat":"accesorios","nombre":"Apple Pencil Pro",     "caracteristicas":"2a Generacion",                  "disp":"vendido",   "precio":140,  "img":"img/apple-pencil-pro.png"},
    {"cat":"accesorios","nombre":"AirTag",               "caracteristicas":"x1",                             "disp":"disponible","precio":40,   "img":"img/airtag.png"},
    {"cat":"accesorios","nombre":"Cargador 20W",         "caracteristicas":"USB-C · Original Apple",         "disp":"disponible","precio":35,   "img":"img/cargador-20w.png"},
    {"cat":"accesorios","nombre":"Cable USB-C",          "caracteristicas":"Original Apple · 1m",            "disp":"disponible","precio":20,   "img":"img/cable-usbc.png"},
    {"cat":"accesorios","nombre":"Funda MagSafe",        "caracteristicas":"Compatible iPhone",              "disp":"disponible","precio":5,    "img":"img/funda-magsafe.png"},
    {"cat":"accesorios","nombre":"Templado",             "caracteristicas":"Vidrio templado · iPhone",       "disp":"disponible","precio":3,    "img":"img/templado.png"},
    {"cat":"accesorios","nombre":"Funda Silicon",        "caracteristicas":"Compatible iPhone",              "disp":"disponible","precio":5,    "img":"img/Fondo de FUNDA SILICON eliminado.png"},
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
    return [f"USD {base}"]

TODAY  = date.today().strftime("%d/%m/%Y")
PAGE_W, PAGE_H = A4
MARGIN = 20 * mm

# ── Estilos ───────────────────────────────────────────────────
def ps(name, font, size, color=BLACK, align=TA_LEFT, leading=None):
    return ParagraphStyle(name, fontName=font, fontSize=size,
        textColor=color, alignment=align,
        leading=leading or round(size * 1.35, 1))

sCatHead = ps("sCatH",  "Poppins-Bold",    9.5, WHITE, TA_LEFT,   13)
sColHdr  = ps("sColH",  "Poppins-Bold",    7.5, WHITE, TA_CENTER, 10)
sModel   = ps("sModel", "Poppins-SemiBold",8.5, BLACK, TA_LEFT,   12)
sSub     = ps("sSub",   "Poppins-Regular", 6.8, GRAY2, TA_LEFT,    9)
sPrice   = ps("sPrice", "IBMPlexMono-Bold",8.5, BLUE,  TA_CENTER, 11)
sPriceNA = ps("sNA",    "IBMPlexMono",     7.5, GRAY2, TA_CENTER, 10)
sCondB   = ps("sCond",  "Poppins-Regular", 8,   BLACK, TA_LEFT,   12)

# ── Header / Footer ───────────────────────────────────────────
def draw_page(canvas, doc):
    canvas.saveState()
    w, h = A4
    band = 17 * mm

    canvas.setFillColor(NAVY)
    canvas.rect(0, h - band, w, band, fill=1, stroke=0)
    canvas.setFillColor(BLUE)
    canvas.rect(0, h - band - 1.2*mm, w, 1.2*mm, fill=1, stroke=0)

    canvas.setFillColor(WHITE)
    canvas.setFont("Poppins-Bold", 13)
    canvas.drawString(MARGIN, h - 9.5*mm, "HIGHTECH ROSARIO")
    canvas.setFont("Poppins-Regular", 7)
    canvas.setFillColor(BLUEL)
    canvas.drawString(MARGIN, h - 13.5*mm, "LISTA DE PRECIOS MAYORISTA")

    canvas.setFont("Poppins-Regular", 7.5)
    canvas.setFillColor(BLUEL)
    canvas.drawRightString(w - MARGIN, h - 9*mm, TODAY)

    canvas.setStrokeColor(LGRAY)
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN, 13.5*mm, w - MARGIN, 13.5*mm)

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

    # Anchos de columna: [foto | modelo | precio]
    IC = 19 * mm                   # columna foto
    rest = col_w - IC
    cw = [IC, rest*0.72, rest*0.28]

    # ── Bloque de condiciones ──────────────────────────────────
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

    # ── Tablas por categoría ───────────────────────────────────
    by_cat = {}
    for p in PRODUCTOS:
        by_cat.setdefault(p["cat"], []).append(p)

    for cat in CAT_ORDER:
        prods = by_cat.get(cat, [])
        if not prods:
            continue

        # Encabezado de categoría (fila completa navy)
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

        # Cabecera de columnas
        hdr = [
            Paragraph("FOTO", sColHdr),
            Paragraph("MODELO / VARIANTE", sColHdr),
            Paragraph("x1", sColHdr),
            Paragraph("x3\n(-$10)", sColHdr),
            Paragraph("x5\n(-$20)", sColHdr),
            Paragraph("x10\n(-$25)", sColHdr),
        ]

        rows = [hdr]
        ts = [
            # cabecera
            ("BACKGROUND",    (0,0),(-1,0), NAVY2),
            ("TOPPADDING",    (0,0),(-1,0), 5),
            ("BOTTOMPADDING", (0,0),(-1,0), 5),
            ("ALIGN",         (0,0),(-1,0), "CENTER"),
            # toda la tabla
            ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
            ("LINEBELOW",     (0,0),(-1,-1), 0.25, LGRAY),
            ("BOX",           (0,0),(-1,-1), 0.5, LGRAY),
            # columna imagen: sin padding lateral, alineada al centro
            ("ALIGN",         (0,1),(0,-1), "CENTER"),
            ("TOPPADDING",    (0,1),(0,-1), 3),
            ("BOTTOMPADDING", (0,1),(0,-1), 3),
            ("LEFTPADDING",   (0,1),(0,-1), 2),
            ("RIGHTPADDING",  (0,1),(0,-1), 2),
        ]

        for i, p in enumerate(prods):
            ri = i + 1
            bg = WHITE if i % 2 == 0 else GRAY
            ts += [
                ("BACKGROUND",    (0,ri),(-1,ri), bg),
                ("TOPPADDING",    (1,ri),(-1,ri), 5),
                ("BOTTOMPADDING", (1,ri),(-1,ri), 5),
                ("LEFTPADDING",   (1,ri),(1,ri),  8),
            ]

            photo = img_cell(p["img"])
            model_cell = [Paragraph(p["nombre"], sModel),
                          Paragraph(p["caracteristicas"], sSub)]

            if p["disp"] == "vendido":
                price_cells = [Paragraph("VENDIDO", sPriceNA)] + [Paragraph("—", sPriceNA)]*3
            else:
                price_cells = [Paragraph(v, sPrice) for v in qty_prices(p["precio"])]

            rows.append([photo, model_cell] + price_cells)

        tbl = Table(rows, colWidths=cw, repeatRows=1)
        tbl.setStyle(TableStyle(ts))

        story.append(KeepTogether([cat_lbl, tbl]))
        story.append(Spacer(1, 4*mm))

    doc.build(story)
    print(f"PDF listo: {OUTPUT}")

build()
