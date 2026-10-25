"""Sistema editorial IRAXXXDIOS aplicado a G3 · Ribera de Curtidores 31.
Georgia -> Gelasio (métrica equivalente). Magenta solo navega. A4 vertical, márgenes 16 mm."""
import json, math
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER
from reportlab.lib.utils import ImageReader

pdfmetrics.registerFont(TTFont("G", "/home/claude/fonts/G400.ttf"))
pdfmetrics.registerFont(TTFont("GB", "/home/claude/fonts/G700.ttf"))
pdfmetrics.registerFont(TTFont("GI", "/home/claude/fonts/GI400.ttf"))
pdfmetrics.registerFont(TTFont("GBI", "/home/claude/fonts/GI700.ttf"))
from reportlab.pdfbase.pdfmetrics import registerFontFamily
registerFontFamily("G", normal="G", bold="GB", italic="GI", boldItalic="GBI")

TINTA = HexColor("#1c1c1c"); MAG = HexColor("#e5007e"); ROSA = HexColor("#f2a0c0")
VERDE = HexColor("#1f6f50"); AGUA = HexColor("#2e7f9e"); PANEL = HexColor("#f6f3ee")
FILETE = HexColor("#cfcac2"); TEC = HexColor("#33322e"); GRIS = HexColor("#8a867e")
PW, PH = 210 * mm, 297 * mm
ML, MR, MT, MB = 16 * mm, 16 * mm, 16 * mm, 16 * mm
CW = PW - ML - MR

def sty(size=8.3, lead=None, font="G", color=TINTA, align=TA_LEFT, space=0):
    return ParagraphStyle("s", fontName=font, fontSize=size, leading=lead or size * 1.38,
                          textColor=color, alignment=align, spaceAfter=space)
BODY = sty(8.3, 11.6)
SMALL = sty(6.9, 9.3)
CAP = sty(6.6, 8.9, color=TEC)
LEAD = sty(9.6, 13.2, color=TEC)

def spaced(s):
    return " ".join(list(s.upper()))
def spaced_html(s):
    return "&nbsp;&nbsp;".join(" ".join(list(w)) for w in s.upper().split(" "))

class Doc:
    def __init__(self, path, titulo_corto="COMPENDIO DE INVESTIGACIÓN · G3"):
        self.c = canvas.Canvas(path, pagesize=(PW, PH))
        self.c.setTitle("Ribera de Curtidores 31 · Compendio de investigación")
        self.c.setAuthor("Adam · G3 · UEM")
        self.n = 0; self.part = ""; self.short = titulo_corto
        self.toc = []; self.y = PH - MT
    # ---------- page furniture
    def page(self, part=None, furniture=True):
        if self.n > 0:
            self.c.showPage()
        self.n += 1
        if part: self.part = part
        if furniture:
            c = self.c
            c.setFont("G", 5.6); c.setFillColor(GRIS)
            c.drawString(ML, PH - 9 * mm, spaced(self.short))
            c.drawRightString(PW - MR, PH - 9 * mm, spaced(self.part))
            c.drawString(ML, 8.5 * mm, spaced("IRAXXXDIOS · Ribera de Curtidores 31"))
            c.setFillColor(MAG); c.setFont("G", 8)
            c.drawRightString(PW - MR, 8.5 * mm, str(self.n))
        self.y = PH - MT - 4 * mm
    def kicker(self, text, y=None):
        if y is None:
            y = self.y if self.y > PH - MT - 6 * mm else self.y - 3.5 * mm
        self.c.setFont("GB", 6.4); self.c.setFillColor(MAG)
        self.c.drawString(ML, y, spaced(text)); self.y = y - 7.2 * mm
    def title(self, text, size=17, toc=True):
        p = Paragraph(text, sty(size, size * 1.18, "GB"))
        w, h = p.wrap(CW, 60 * mm); p.drawOn(self.c, ML, self.y - h + size * 0.9); self.y -= h + 1.5 * mm
        if toc: self.toc.append((self.part, text, self.n))
    def para(self, html, x=None, y=None, w=None, st=BODY, gap=2.2):
        x = ML if x is None else x; w = CW if w is None else w; y = self.y if y is None else y
        p = Paragraph(html, st); _, h = p.wrap(w, 400 * mm); p.drawOn(self.c, x, y - h)
        if x == ML and (w == CW): self.y = y - h - gap * mm
        return h
    def lead(self, html):
        self.para(html, st=LEAD, gap=3)
    def image(self, path, x=None, y=None, w=None, h=None):
        x = ML if x is None else x; y = self.y if y is None else y; w = CW if w is None else w
        ir = ImageReader(path); iw, ih = ir.getSize()
        if h is None: h = w * ih / iw
        self.c.drawImage(ir, x, y - h, w, h, mask="auto")
        if x == ML and w == CW: self.y = y - h - 2 * mm
        return h
    def caption(self, bold, text, src=None, x=None, w=None, y=None):
        x = ML if x is None else x; w = CW if w is None else w; y = self.y if y is None else y
        h = self.para(f"<b>{bold}</b> {text}", x=x, y=y, w=w, st=CAP)
        yy = y - h - 1.2 * mm
        if src:
            p = Paragraph(spaced_html("fuente") + ": " + src, sty(5.4, 7.2, color=GRIS)); _, h2 = p.wrap(w, 50 * mm)
            p.drawOn(self.c, x, yy - h2); yy -= h2 + 1 * mm
        if x == ML and w == CW: self.y = yy - 5 * mm
        return y - yy
    def nivel(self, lvl, x=None, y=None):
        x = PW - MR - 26 * mm if x is None else x; y = self.y if y is None else y
        lab = {"A": "A · MEDIDO", "B": "B · INFERIDO", "C": "C · HIPÓTESIS", "A/B": "A/B · MEDIDO E INFERIDO", "B/C": "B/C · INFERIDO E HIPÓTESIS"}[lvl]
        col = {"A": VERDE, "B": AGUA, "C": MAG, "A/B": VERDE, "B/C": AGUA}[lvl]
        c = self.c; c.setStrokeColor(col); c.setLineWidth(0.5)
        tw = pdfmetrics.stringWidth(spaced(lab), "G", 5) + 4 * mm
        c.roundRect(PW - MR - tw, y - 1.4 * mm, tw, 4.2 * mm, 2 * mm, stroke=1, fill=0)
        c.setFillColor(col); c.setFont("G", 5); c.drawCentredString(PW - MR - tw / 2, y + 0.1 * mm, spaced(lab))
    def bignum(self, x, y, val, unit, label, w=40 * mm, col=TINTA):
        c = self.c; c.setFillColor(col); c.setFont("GB", 19); c.drawString(x, y, val)
        vw = pdfmetrics.stringWidth(val, "GB", 19)
        c.setFont("G", 7.5); c.setFillColor(TEC); c.drawString(x + vw + 1.2 * mm, y, unit)
        p = Paragraph(label, sty(6.2, 8, color=TEC)); _, h = p.wrap(w, 30 * mm); p.drawOn(c, x, y - 2 * mm - h)
        return 10 * mm + h
    def panel(self, html, title=None, h=None, x=None, w=None, y=None):
        x = ML if x is None else x; w = CW if w is None else w; y = self.y if y is None else y
        p = Paragraph(html, sty(7.4, 10.2, color=TEC)); _, ph = p.wrap(w - 8 * mm, 200 * mm)
        th = 5 * mm if title else 0
        hh = h or ph + th + 7 * mm
        c = self.c; c.setFillColor(PANEL); c.rect(x, y - hh, w, hh, stroke=0, fill=1)
        if title:
            c.setFillColor(TEC); c.setFont("GB", 5.8); c.drawString(x + 4 * mm, y - 5 * mm, spaced(title))
        p.drawOn(c, x + 4 * mm, y - th - 3.5 * mm - ph)
        if x == ML and w == CW: self.y = y - hh - 3 * mm
        return hh
    def table(self, data, cw, x=None, y=None, fs=6.6, head=True, zebra=False):
        x = ML if x is None else x; y = self.y if y is None else y
        rows = []
        for i, r in enumerate(data):
            st = sty(fs, fs * 1.3, "GB" if (head and i == 0) else "G", MAG if (head and i == 0) else TINTA)
            rows.append([Paragraph(spaced_html(str(v)) if (head and i == 0) else str(v), st if not (head and i == 0) else sty(5.4, 7, "G", MAG)) for v in r])
        t = Table(rows, colWidths=cw)
        ts = [("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 1.5), ("RIGHTPADDING", (0, 0), (-1, -1), 3),
              ("TOPPADDING", (0, 0), (-1, -1), 1.6), ("BOTTOMPADDING", (0, 0), (-1, -1), 1.8),
              ("LINEBELOW", (0, 1), (-1, -1), 0.3, FILETE)]
        if head: ts += [("LINEBELOW", (0, 0), (-1, 0), 0.8, MAG)]
        t.setStyle(TableStyle(ts))
        _, h = t.wrap(sum(cw), 400 * mm); t.drawOn(self.c, x, y - h)
        if x == ML: self.y = y - h - 3 * mm
        return h
    def rule(self, y=None, col=FILETE, w=0.4):
        y = self.y if y is None else y
        self.c.setStrokeColor(col); self.c.setLineWidth(w); self.c.line(ML, y, PW - MR, y); self.y = y - 3 * mm
    def label(self, x, y, text, size=5.4, col=TEC, font="G", align="l"):
        self.c.setFont(font, size); self.c.setFillColor(col)
        {"l": self.c.drawString, "r": self.c.drawRightString, "c": self.c.drawCentredString}[align](x, y, text)
    def save(self):
        self.c.save()
