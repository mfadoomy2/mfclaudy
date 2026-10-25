# -*- coding: utf-8 -*-
"""COMPENDIO ANALITICO — nucleo comun: seccion, tabla paginada, carga de todos los datos.

El compendio vuelca TODO el dato disponible (no resumenes): cada modulo de auditoria con
sus filas, cada escenario climatico con sus cifras, los 160 puntos de mantenimiento, las
17 especies, los 279 analisis catalogados y las 48 metricas publicadas.
"""
import csv
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.normpath(os.path.join(HERE, '..', '..'))
RC = os.path.normpath(os.path.join(BASE, '..'))
F9 = os.path.join(RC, 'FASE_03B9_HYPERDETAIL_V006')
AUD = os.path.join(F9, '_reaudit9', '_data')
CLI = os.path.join(F9, '_reclima9', '_data')
SYS = os.path.join(BASE, '00_SISTEMA_Y_FUENTES')
sys.path.insert(0, os.path.join(SYS, '_scripts'))
sys.path.insert(0, os.path.join(BASE, '01_CLIMA_Y_CONFORT', '_scripts'))
import refugio_editorial as E  # noqa: E402

MXW = E.A4W - 2 * E.MX


def J(*p):
    with io.open(os.path.join(*p), encoding='utf-8') as f:
        return json.load(f)


def C(*p):
    with io.open(os.path.join(*p), encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))


# ---------------------------------------------------------------- datos globales
AU = {k: J(AUD, k + '.json') for k in
      ('a1_paths', 'a2_clear', 'a3_heights', 'a4_ribbon', 'a5_access', 'a6_metro',
       'a7_views', 'a8_density', 'a9_maint', 'a10_collisions', 'a12_edificios',
       'issues', 'summary')}
CL = {k: J(CLI, k + '.json') for k in
      ('zonas', 'cinta', 'spots', 'agua', 'aire', 'refugio', 'neb_escenarios',
       'vegetacion', 'metricas', 'escena_meta', 'mist', 'discos')}
BD = {}
for carp, fn in (('01_CLIMA_Y_CONFORT', 'cli_stats'), ('02_MOVILIDAD_Y_ACCESIBILIDAD', 'mob_stats'),
                 ('04_AGUA_ECOLOGIA_Y_VEGETACION', 'agu_stats'),
                 ('05_CONSTRUCCION_ESTRUCTURA_Y_MANTENIMIENTO', 'tec_stats'),
                 ('06_USO_SOCIAL_Y_EXPERIENCIA', 'soc_stats'),
                 ('07_ECONOMIA_OPERACION_Y_ESCENARIOS', 'eco_stats'),
                 ('08_PATRIMONIO_VISUALES_Y_PAISAJE_URBANO', 'pat_stats'),
                 ('10_SINTESIS_GLOBAL', 'kpis'), ('10_SINTESIS_GLOBAL', 'global_cross')):
    BD[fn] = J(BASE, carp, 'B_DATOS', fn + '.json')
REG = C(SYS, 'ANALYSIS_MASTER_REGISTER.csv')
MET = C(SYS, 'FINAL_METRICS_REGISTRY.csv')
SNAP = J(SYS, 'BASELINE_SNAPSHOT.json')
VEGCLI = J(F9, '_veg_clima.json')
BOT = C(F9, 'BOTANICAL_MASTERPLAN_v001.csv')
MANT = C(BASE, '05_CONSTRUCCION_ESTRUCTURA_Y_MANTENIMIENTO', 'B_DATOS', 'matriz_mantenimiento.csv')
AGUAEL = C(BASE, '04_AGUA_ECOLOGIA_Y_VEGETACION', 'B_DATOS', 'elementos_agua.csv')
FUENTES = C(BASE, '07_ECONOMIA_OPERACION_Y_ESCENARIOS', 'B_DATOS', 'fuentes_externas.csv')
DISC = io.open(os.path.join(SYS, 'DISCOVERIES_REGISTER.md'), encoding='utf-8').read()
geo = E.load_geo()


class Comp:
    """Documento del compendio con paginacion automatica de tablas largas."""

    def __init__(self, path, titulo, cap):
        self.doc = E.Doc(path, titulo, cap)
        self.cap = cap
        self.p = None
        self.y = 0

    def nueva(self, cap=None, top=1.0):
        if self.p is not None:
            self.doc.add(self.p)
        self.p = self.doc.page(cap or self.cap)
        self.y = E.A4H - top
        return self.p

    def espacio(self, alto):
        """Garantiza 'alto' pulgadas libres; si no, salta de pagina."""
        if self.y - alto < 0.95:
            self.nueva()
        return self.y

    def seccion(self, kicker, titulo, sub=None, size=16, nueva=True):
        if nueva or self.p is None:
            self.nueva()
        self.y = self.p.kicker(self.y, kicker)
        self.y = self.p.title(self.y, titulo, size=size)
        if sub:
            self.y = self.p.subtitle(self.y, sub)
        return self.y

    def texto(self, s, wrap=104, size=8.2, gap=0.08):
        self.espacio(0.6)
        self.y = self.p.body(E.MX, self.y, s, wrap=wrap, size=size) - gap
        return self.y

    def lista(self, items, wrap=100, size=8.0):
        for it in items:
            self.espacio(0.45)
            self.y = self.p.dashlist(E.MX, self.y, [it], wrap=wrap, size=size)
        return self.y

    def tabla(self, cols, rows, col_w, size=6.6, titulo=None, fuente=None, row_h=0.155):
        """Tabla que se pagina sola repitiendo cabecera."""
        i = 0
        while i < len(rows):
            self.espacio(1.2)
            if titulo and i == 0:
                self.y = self.p.kicker(self.y, titulo)
            elif titulo:
                self.y = self.p.kicker(self.y, titulo + ' (cont.)')
            libre = self.y - 1.05
            cuantas = max(1, int(libre / row_h))
            chunk = rows[i:i + cuantas]
            self.y = self.p.tabla(E.MX, self.y, MXW, cols, chunk, col_w=col_w, size=size)
            i += len(chunk)
            if i < len(rows):
                self.nueva()
        if fuente:
            self.espacio(0.2)
            self.p.text(E.MX, self.y, fuente, size=5.4, color=E.GRAYTX)
            self.y -= 0.16
        return self.y

    ASPECTO = 212.0 / 123.0          # ambito -112..100 x -45..78

    def mapa(self, alto=None, dibuja=None, leyenda=None, cap_lead='', cap='', ancho=None):
        """Mapa del ambito con su relacion de aspecto real (sin aire lateral)."""
        ancho = ancho or MXW
        alto = alto or (ancho / self.ASPECTO)
        self.espacio(alto + 1.05)
        ax = self.p.axes(E.MX, self.y - alto, ancho, alto)
        im = dibuja(ax)
        if leyenda and im is not None:
            E.cbar(self.p, im, E.MX, self.y - alto - 0.34, 1.7, leyenda)
            self.y -= alto + 0.62
        else:
            self.y -= alto + 0.16
        if cap:
            self.espacio(0.4)
            self.y = self.p.caption(E.MX, self.y, cap_lead, cap, wrap=108)
        return self.y

    def mapa_doble(self, dibA, dibB, labA, labB, leyenda, cap_lead, cap):
        """Dos mapas A/B lado a lado con leyenda comun."""
        w = (MXW - 0.3) / 2
        alto = w / self.ASPECTO
        self.espacio(alto + 1.1)
        self.p.text(E.MX, self.y, labA, size=6.2, tracked=True, weight='bold',
                    color=E.GRAYTX)
        self.p.text(E.MX + w + 0.3, self.y, labB, size=6.2, tracked=True, weight='bold',
                    color=E.GRAYTX)
        self.y -= 0.14
        ax1 = self.p.axes(E.MX, self.y - alto, w, alto)
        im = dibA(ax1)
        ax2 = self.p.axes(E.MX + w + 0.3, self.y - alto, w, alto)
        dibB(ax2)
        if im is not None:
            E.cbar(self.p, im, E.MX, self.y - alto - 0.34, 1.7, leyenda)
        self.y -= alto + 0.62
        if cap:
            self.espacio(0.4)
            self.y = self.p.caption(E.MX, self.y, cap_lead, cap, wrap=108)
        return self.y

    def panel(self, titulo, texto, alto=1.3, wrap=98):
        self.espacio(alto + 0.2)
        yy = self.p.panel(E.MX, self.y, MXW, alto, titulo)
        self.p.text(E.MX + 0.16, yy, texto, size=8.0, wrap=wrap)
        self.y -= alto + 0.14
        return self.y

    def cerrar(self):
        if self.p is not None:
            self.doc.add(self.p)
        self.doc.close()
        return self.doc.folio
