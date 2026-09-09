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
from reportlab.platypus.flowables import HRFlowable
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from datetime import date
import os, urllib.request, tempfile

# ── Colores de marca ──────────────────────────────────────────
NAVY   = colors.HexColor("#000E23")
BLUE   = colors.HexColor("#0050ED")
GRAY   = colors.HexColor("#F4F4F5")
WHITE  = colors.white
BLACK  = colors.HexColor("#111111")
GRAY2  = colors.HexColor("#6B7280")
BGALT  = colors.HexColor("#EEF1F8")   # azul muy suave para alternado

# ── Fuentes: Poppins + IBM Plex Mono via Google Fonts CDN ────
FONT_DIR = tempfile.mkdtemp()

def dl(url, dest):
    if not os.path.exists(dest):
        urllib.request.urlretrieve(url, dest)

BASE = "https://github.com/google/fonts/raw/main/ofl/"
fonts = {
    "Poppins-Regular":   BASE + "poppins/Poppins-Regular.ttf",
    "Poppins-Bold":      BASE + "poppins/Poppins-Bold.ttf",
    "Poppins-SemiBold":  BASE + "poppins/Poppins-SemiBold.ttf",
    "IBMPlexMono-Regular": BASE + "ibmplexmono/IBMPlexMono-Regular.ttf",
    "IBMPlexMono-Bold":    BASE + "ibmplexmono/IBMPlexMono-Bold.ttf",
}
print("Descargando fuentes…")
for name, url in fonts.items():
    dest = os.path.join(FONT_DIR, name + ".ttf")
    dl(url, dest)
    pdfmetrics.registerFont(TTFont(name, dest))

print("Fuentes OK")

# ── Datos de productos ────────────────────────────────────────
PRODUCTOS = [
    # SELLADOS
    {"id":41,"cat":"iphones","nombre":"iPhone 17 256GB","sub":"Sellado · Nuevo","disponibilidad":"disponible","precioStock":990,"caracteristicas":"White"},
    {"id":42,"cat":"iphones","nombre":"iPhone 17 256GB","sub":"Sellado · Nuevo","disponibilidad":"disponible","precioStock":990,"caracteristicas":"Black"},
    {"id":2, "cat":"iphones","nombre":"iPhone 17 Pro 256GB","sub":"Sellado · Nuevo","disponibilidad":"disponible","precioStock":1190,"caracteristicas":"Cosmic Orange"},
    {"id":3, "cat":"iphones","nombre":"iPhone 17 Pro 256GB","sub":"Sellado · Nuevo","disponibilidad":"disponible","precioStock":1250,"caracteristicas":"Silver"},
    {"id":4, "cat":"iphones","nombre":"iPhone 17 Pro 256GB","sub":"Sellado · Nuevo","disponibilidad":"disponible","precioStock":1250,"caracteristicas":"Deep Blue"},
    {"id":5, "cat":"iphones","nombre":"iPhone 17 Pro Max 256GB","sub":"Sellado · Nuevo","disponibilidad":"disponible","precioStock":1350,"caracteristicas":"Silver"},
    {"id":6, "cat":"iphones","nombre":"iPhone 17 Pro Max 256GB","sub":"Sellado · Nuevo","disponibilidad":"disponible","precioStock":1350,"caracteristicas":"Blue Titanium"},
    # USADOS
    {"id":43,"cat":"usados","nombre":"iPhone 15 128GB","sub":"Usado · Verificado","disponibilidad":"disponible","precioStock":490,"caracteristicas":"Black · Batería 83%"},
    {"id":44,"cat":"usados","nombre":"iPhone 14 128GB","sub":"Usado · Verificado","disponibilidad":"disponible","precioStock":410,"caracteristicas":"Celeste · Batería 100%"},
    {"id":7, "cat":"usados","nombre":"iPhone 15 128GB","sub":"Usado · Verificado","disponibilidad":"vendido","precioStock":490,"caracteristicas":"Pink · Batería 80%"},
    {"id":9, "cat":"usados","nombre":"iPhone 15 Pro 128GB","sub":"Usado · Verificado","disponibilidad":"disponible","precioStock":610,"caracteristicas":"Blue Titanium · Batería 87%"},
    {"id":10,"cat":"usados","nombre":"iPhone 15 Pro 128GB","sub":"Usado · Verificado","disponibilidad":"disponible","precioStock":610,"caracteristicas":"Natural Titanium · Batería 86%"},
    {"id":45,"cat":"usados","nombre":"iPhone 15 Pro Max 256GB","sub":"Usado · Verificado","disponibilidad":"disponible","precioStock":710,"caracteristicas":"Blue Titanium · Batería 87%"},
    {"id":11,"cat":"usados","nombre":"iPhone 16 128GB","sub":"Usado · Verificado","disponibilidad":"disponible","precioStock":650,"caracteristicas":"Ultramarine · Batería 100%"},
    {"id":12,"cat":"usados","nombre":"iPhone 16 Pro 128GB","sub":"Usado · Verificado","disponibilidad":"disponible","precioStock":830,"caracteristicas":"Desert · Batería 93%"},
    {"id":46,"cat":"usados","nombre":"iPhone 16 Pro 128GB","sub":"Usado · Verificado","disponibilidad":"disponible","precioStock":810,"caracteristicas":"White Titanium · Batería 91%"},
    # MACBOOK
    {"id":15,"cat":"macbook","nombre":"MacBook Neo 256GB","sub":"Sellado · Nuevo","disponibilidad":"disponible","precioStock":850,"caracteristicas":"Silver"},
    {"id":40,"cat":"macbook","nombre":'MacBook Air M5 13"',"sub":"Sellado · Nuevo","disponibilidad":"disponible","precioStock":1450,"caracteristicas":"16GB RAM · 512GB · Midnight"},
    # AIRPODS
    {"id":16,"cat":"airpods","nombre":"AirPods Pro 3","sub":"Sellado · Nuevo","disponibilidad":"disponible","precioStock":270,"caracteristicas":"USB-C"},
    {"id":17,"cat":"airpods","nombre":"AirPods 4","sub":"Sellado · Nuevo","disponibilidad":"disponible","precioStock":210,"caracteristicas":"Active Noise Cancellation"},
    {"id":18,"cat":"airpods","nombre":"AirPods Max (2nd Gen)","sub":"Sellado · Nuevo","disponibilidad":"disponible","precioStock":600,"caracteristicas":"2026 · USB-C"},
    # ACCESORIOS
    {"id":19,"cat":"accesorios","nombre":"Apple Pencil Pro","sub":"Sellado · Nuevo","disponibilidad":"vendido","precioStock":140,"caracteristicas":"2a Generacion"},
    {"id":20,"cat":"accesorios","nombre":"AirTag","sub":"Sellado · Nuevo","disponibilidad":"disponible","precioStock":40,"caracteristicas":"x1"},
    {"id":30,"cat":"accesorios","nombre":"Cargador 20W","sub":"Sellado · Nuevo","disponibilidad":"disponible","precioStock":50,"caracteristicas":"USB-C · Original Apple"},
    {"id":31,"cat":"accesorios","nombre":"Cable USB-C","sub":"Sellado · Nuevo","disponibilidad":"disponible","precioStock":20,"caracteristicas":"Original Apple · 1m"},
    {"id":32,"cat":"accesorios","nombre":"Funda MagSafe","sub":"Sellado · Nuevo","disponibilidad":"disponible","precioStock":5,"caracteristicas":"Compatible iPhone"},
    {"id":33,"cat":"accesorios","nombre":"Templado","sub":"Sellado · Nuevo","disponibilidad":"disponible","precioStock":3,"caracteristicas":"Vidrio templado · iPhone"},
    {"id":34,"cat":"accesorios","nombre":"Funda Silicon","sub":"Sellado · Nuevo","disponibilidad":"disponible","precioStock":5,"caracteristicas":"Compatible iPhone"},
    # SAMSUNG
    {"id":25,"cat":"samsung","nombre":"Samsung S25 Ultra","sub":"Sellado · Nuevo","disponibilidad":"disponible","precioStock":950,"caracteristicas":"12GB RAM · 256GB · Black"},
    {"id":29,"cat":"samsung","nombre":"Samsung S26 Ultra","sub":"Sellado · Nuevo","disponibilidad":"disponible","precioStock":1250,"caracteristicas":"12GB RAM · 512GB · Black"},
    # APPLE WATCH
    {"id":26,"cat":"applewatch","nombre":"Apple Watch Series 11","sub":"Sellado · Nuevo","disponibilidad":"disponible","precioStock":390,"caracteristicas":"42mm · Black"},
    {"id":27,"cat":"applewatch","nombre":"Apple Watch Series 11","sub":"Sellado · Nuevo","disponibilidad":"vendido","precioStock":430,"caracteristicas":"46mm · Black"},
    {"id":28,"cat":"applewatch","nombre":"Apple Watch Ultra 3","sub":"Sellado · Nuevo","disponibilidad":"disponible","precioStock":820,"caracteristicas":"49mm · Titanio · 2025"},
    # IPAD
    {"id":35,"cat":"ipad","nombre":"iPad A16 128GB","sub":"Sellado · Nuevo","disponibilidad":"disponible","precioStock":500,"caracteristicas":"Chip A16"},
    {"id":36,"cat":"ipad","nombre":"iPad A16 256GB","sub":"Sellado · Nuevo","disponibilidad":"disponible","precioStock":610,"caracteristicas":"Chip A16"},
    {"id":37,"cat":"ipad","nombre":'iPad Air 11" M4 128GB',"sub":"Sellado · Nuevo","disponibilidad":"disponible","precioStock":850,"caracteristicas":"Chip M4 · 11 pulgadas"},
    {"id":38,"cat":"ipad","nombre":'iPad Air 11" M4 256GB',"sub":"Sellado · Nuevo","disponibilidad":"disponible","precioStock":950,"caracteristicas":"Chip M4 · 11 pulgadas"},
    {"id":39,"cat":"ipad","nombre":"iPad Pro M5 256GB","sub":"Sellado · Nuevo","disponibilidad":"disponible","precioStock":1250,"caracteristicas":"Chip M5 · OLED"},
]

# ── Orden y etiquetas de categorías ──────────────────────────
CAT_ORDER  = ["iphones","usados","macbook","airpods","ipad","applewatch","samsung","accesorios"]
CAT_LABELS = {
    "iphones":    "iPhones Sellados",
    "usados":     "iPhones Usados Verificados",
    "macbook":    "MacBooks",
    "airpods":    "AirPods",
    "ipad":       "iPads",
    "applewatch": "Apple Watch",
    "samsung":    "Samsung",
    "accesorios": "Accesorios",
}

# descuentos por qty
def precios(base):
    return [
        f"USD {base}",
        f"USD {base - 10}",
        f"USD {base - 20}",
        f"USD {base - 25}",
    ]

TODAY = date.today().strftime("%d/%m/%Y")
OUTPUT = os.path.join(os.path.dirname(__file__), "HIGHTECH-lista-precios-mayorista.pdf")

# ── Estilos de párrafo ────────────────────────────────────────
def S(name, font, size, color=BLACK, align=TA_LEFT, leading=None, spaceBefore=0, spaceAfter=0):
    return ParagraphStyle(
        name, fontName=font, fontSize=size,
        textColor=color, alignment=align,
        leading=leading or size * 1.3,
        spaceBefore=spaceBefore, spaceAfter=spaceAfter,
    )

sTitle    = S("sTitle",   "Poppins-Bold",    22, NAVY,  TA_LEFT,  28)
sSubtitle = S("sSub",     "Poppins-Regular", 9,  GRAY2, TA_LEFT,  12)
sDate     = S("sDate",    "Poppins-Regular", 9,  GRAY2, TA_RIGHT, 12)
sCondBox  = S("sCond",    "Poppins-Regular", 8.5, BLACK, TA_LEFT, 12)
sCatHead  = S("sCatH",    "Poppins-Bold",    10, WHITE, TA_LEFT,  14)
sModel    = S("sModel",   "Poppins-SemiBold",8.5, BLACK, TA_LEFT, 12)
sSub      = S("sSubP",    "Poppins-Regular", 7,  GRAY2, TA_LEFT, 10)
sPrice    = S("sPrice",   "IBMPlexMono-Bold",9,  BLUE,  TA_CENTER,12)
sPriceW   = S("sPriceW",  "IBMPlexMono-Bold",9,  WHITE, TA_CENTER,12)
sColHead  = S("sColH",    "Poppins-Bold",    8,  WHITE, TA_CENTER,11)
sFooter   = S("sFoot",    "Poppins-Regular", 7.5,GRAY2, TA_CENTER,10)

# ── Página: header y footer via canvas ───────────────────────
PAGE_W, PAGE_H = A4
MARGIN = 20 * mm

class HTPdf(BaseDocTemplate):
    def __init__(self, filename, **kw):
        super().__init__(filename, **kw)
        self._total_pages = 0

    def handle_documentBegin(self):
        super().handle_documentBegin()

    def afterPage(self):
        self._total_pages = self.page

def header_footer(canvas, doc):
    canvas.saveState()
    w, h = A4

    # ── Header band ──
    band_h = 18 * mm
    canvas.setFillColor(NAVY)
    canvas.rect(0, h - band_h, w, band_h, fill=1, stroke=0)

    # Título izquierda
    canvas.setFillColor(WHITE)
    canvas.setFont("Poppins-Bold", 13)
    canvas.drawString(MARGIN, h - 11.5 * mm, "HIGHTECH ROSARIO")
    canvas.setFont("Poppins-Regular", 7.5)
    canvas.setFillColor(colors.HexColor("#8BA3D4"))
    canvas.drawString(MARGIN, h - 15.5 * mm, "LISTA DE PRECIOS MAYORISTA")

    # Fecha derecha
    canvas.setFont("Poppins-Regular", 8)
    canvas.setFillColor(colors.HexColor("#8BA3D4"))
    canvas.drawRightString(w - MARGIN, h - 10 * mm, TODAY)

    # Línea azul bajo el header
    canvas.setStrokeColor(BLUE)
    canvas.setLineWidth(2)
    canvas.line(0, h - band_h, w, h - band_h)

    # ── Footer ──
    canvas.setFont("Poppins-Regular", 7)
    canvas.setFillColor(GRAY2)
    footer_txt = f"HIGHTECH ROSARIO  ·  Puerto Norte, Rosario  ·  @hightech.rosario  ·  pag. {doc.page}"
    canvas.drawCentredString(w / 2, 10 * mm, footer_txt)

    # línea sobre footer
    canvas.setStrokeColor(colors.HexColor("#E5E7EB"))
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN, 14 * mm, w - MARGIN, 14 * mm)

    canvas.restoreState()

# ── Construir documento ───────────────────────────────────────
def build_pdf():
    doc = HTPdf(
        OUTPUT,
        pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=26 * mm, bottomMargin=20 * mm,
    )

    frame = Frame(
        MARGIN, 20 * mm,
        PAGE_W - 2 * MARGIN, PAGE_H - 46 * mm,
        id="main",
    )
    tpl = PageTemplate(id="main", frames=[frame], onPage=header_footer)
    doc.addPageTemplates([tpl])

    story = []

    # ── Bloque de condiciones ─────────────────────────────────
    cond_text = (
        "<b>Metodos de pago:</b> USDT / USDC  ·  Transferencia en pesos (+3%)  ·  "
        "Efectivo (pesos o dolares).<br/>"
        "Los equipos se pueden <b>MIXEAR</b>  ·  precios por cantidad  ·  "
        "precios sujetos a cambio sin previo aviso."
    )
    cond_para = Paragraph(cond_text, sCondBox)
    cond_table = Table(
        [[cond_para]],
        colWidths=[PAGE_W - 2 * MARGIN],
    )
    cond_table.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,-1), colors.HexColor("#EEF3FF")),
        ("BOX",          (0,0), (-1,-1), 0.8, BLUE),
        ("LEFTPADDING",  (0,0), (-1,-1), 10),
        ("RIGHTPADDING", (0,0), (-1,-1), 10),
        ("TOPPADDING",   (0,0), (-1,-1), 7),
        ("BOTTOMPADDING",(0,0), (-1,-1), 7),
        ("ROUNDEDCORNERS", [4]),
    ]))
    story.append(cond_table)
    story.append(Spacer(1, 6 * mm))

    # ── Agrupar por categoría ─────────────────────────────────
    by_cat = {}
    for p in PRODUCTOS:
        by_cat.setdefault(p["cat"], []).append(p)

    col_w = PAGE_W - 2 * MARGIN
    # Modelo col + 4 precio cols
    cols = [col_w * 0.44, col_w * 0.14, col_w * 0.14, col_w * 0.14, col_w * 0.14]

    for cat in CAT_ORDER:
        prods = by_cat.get(cat, [])
        if not prods:
            continue

        # Encabezado de categoría
        cat_header = Table(
            [[Paragraph(CAT_LABELS[cat].upper(), sCatHead)]],
            colWidths=[col_w],
        )
        cat_header.setStyle(TableStyle([
            ("BACKGROUND",    (0,0), (-1,-1), NAVY),
            ("LEFTPADDING",   (0,0), (-1,-1), 10),
            ("TOPPADDING",    (0,0), (-1,-1), 5),
            ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ]))

        # Fila de columnas
        col_row = [
            Paragraph("MODELO / VARIANTE", sColHead),
            Paragraph("x1", sColHead),
            Paragraph("x3", sColHead),
            Paragraph("x5", sColHead),
            Paragraph("x10", sColHead),
        ]

        rows = [col_row]
        ts = [
            # col header row
            ("BACKGROUND",    (0,0), (-1,0), colors.HexColor("#0A2060")),
            ("TOPPADDING",    (0,0), (-1,0), 5),
            ("BOTTOMPADDING", (0,0), (-1,0), 5),
            ("LEFTPADDING",   (0,0), (0,0),  10),
            ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
            ("ROWBACKGROUNDS",(0,1), (-1,-1), [WHITE, GRAY]),
            ("LINEBELOW",     (0,0), (-1,-1), 0.3, colors.HexColor("#D1D5DB")),
            ("BOX",           (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ]

        for i, p in enumerate(prods):
            base = p["precioStock"]
            pp = precios(base)

            model_cell = [
                Paragraph(p["nombre"], sModel),
                Paragraph(p["caracteristicas"], sSub),
            ]

            disp = p["disponibilidad"]
            if disp == "vendido":
                price_style = S(f"ps{i}", "IBMPlexMono-Bold", 8, GRAY2, TA_CENTER, 11)
                pp_rendered = [Paragraph("VENDIDO", price_style)] + [Paragraph("—", price_style)] * 3
            else:
                pp_rendered = [Paragraph(v, sPrice) for v in pp]

            rows.append([model_cell] + pp_rendered)

            row_idx = i + 1
            ts.append(("TOPPADDING",    (0, row_idx), (-1, row_idx), 5))
            ts.append(("BOTTOMPADDING", (0, row_idx), (-1, row_idx), 5))
            ts.append(("LEFTPADDING",   (0, row_idx), (0, row_idx), 10))

        table = Table(rows, colWidths=cols, repeatRows=1)
        table.setStyle(TableStyle(ts))

        block = KeepTogether([cat_header, table, Spacer(1, 5 * mm)])
        story.append(block)

    doc.build(story)
    print(f"PDF generado: {OUTPUT}")

build_pdf()
