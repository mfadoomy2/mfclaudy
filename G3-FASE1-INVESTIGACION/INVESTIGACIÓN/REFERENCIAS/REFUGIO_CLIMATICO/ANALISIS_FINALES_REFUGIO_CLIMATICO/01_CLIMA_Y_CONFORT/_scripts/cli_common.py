# -*- coding: utf-8 -*-
"""Comunes de la suite CLI: cabecera normalizada §27, mapa doble A/B, mascara pisable."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.normpath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(BASE, '00_SISTEMA_Y_FUENTES', '_scripts'))
import refugio_editorial as E  # noqa: E402

geo = E.load_geo()
_w = E.np_aud('walk.npy')[::2, ::2].astype(bool)
ny, nx = E.np_cli('u_E2_16_B.npy').shape
W = _w[:ny, :nx]
FUENTE = ('FUENTE: _reclima9/_data (v006 build 12, 2026-08-13) · celda 0,5 m · '
          'ventana crítica 15 jun–15 sep')


def cabecera_analisis(doc, cid, titulo, pregunta, metodo, datos, nivel, limitaciones):
    """Primera pagina normalizada §27: PREGUNTA / METODO / DATOS / NIVEL."""
    p = doc.page(cid)
    y = E.A4H - 1.0
    tema = doc.capitulo.split('·')[-1].strip() if doc.capitulo else 'ANÁLISIS'
    y = p.kicker(y, cid + ' · ' + tema)
    y = p.title(y, titulo, size=19)
    y = p.subtitle(y, pregunta)
    p.chip(E.MX, y - 0.02, nivel)
    y -= 0.34
    colw = (E.A4W - 2 * E.MX - 0.4) / 2
    y1 = p.ficha(E.MX, y, [('MÉTODO', metodo)], wcol=colw, wrap=int(colw * 7.4))
    y2 = p.ficha(E.MX + colw + 0.4, y, [('DATOS', datos), ('LIMITACIONES', limitaciones)],
                 wcol=colw, wrap=int(colw * 7.4))
    return p, min(y1, y2) - 0.08


def mapa_doble(p, y, arrA, arrB, cmap, vmin, vmax, labA, labB, leyenda, cap_lead, cap,
               alto=3.0):
    w = (E.A4W - 2 * E.MX - 0.35) / 2
    ax = p.axes(E.MX, y - alto, w, alto)
    E.draw_context(ax, geo)
    im = E.show_raster(ax, arrA, cmap, vmin=vmin, vmax=vmax, mask=W)
    p.text(E.MX, y + 0.06, labA, size=6.2, tracked=True, weight='bold', color=E.GRAYTX)
    ax2 = p.axes(E.MX + w + 0.35, y - alto, w, alto)
    E.draw_context(ax2, geo)
    E.show_raster(ax2, arrB, cmap, vmin=vmin, vmax=vmax, mask=W)
    p.text(E.MX + w + 0.35, y + 0.06, labB, size=6.2, tracked=True, weight='bold',
           color=E.GRAYTX)
    E.cbar(p, im, E.MX, y - alto - 0.32, 1.7, leyenda)
    yy = p.caption(E.MX + 2.1, y - alto - 0.30, cap_lead, cap, fuente=None, wrap=66)
    p.text(E.MX, min(yy, y - alto - 0.62) - 0.02, FUENTE, size=5.4, color=E.GRAYTX)
    return min(yy, y - alto - 0.62) - 0.30
