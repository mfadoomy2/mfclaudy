"""Escribe piezas (mallas trimesh) en un .3dm de Rhino 8 con capas jerárquicas y colores."""
import rhino3dm as rh
import numpy as np


def _color(hexcol):
    c = hexcol.lstrip('#')
    return (int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16), 255)


class Escritor:
    def __init__(self, notas=''):
        self.m = rh.File3dm()
        self.m.Settings.ModelUnitSystem = rh.UnitSystem.Meters
        self.capas = {}
        self.notas = notas

    def capa(self, ruta, color='#808080'):
        if ruta in self.capas:
            return self.capas[ruta]
        partes = ruta.split('::')
        padre = None
        acum = []
        for p in partes:
            acum.append(p)
            clave = '::'.join(acum)
            if clave not in self.capas:
                l = rh.Layer()
                l.Name = p
                l.Color = _color(color)
                if padre is not None:
                    l.ParentLayerId = self.m.Layers[self.capas[padre]].Id
                idx = self.m.Layers.Add(l)
                self.capas[clave] = idx
            padre = clave
        return self.capas[ruta]

    def malla(self, pieza, prefijo=''):
        tm = pieza.malla
        if tm is None or len(tm.faces) == 0:
            return
        idx = self.capa(prefijo + pieza.capa if prefijo else pieza.capa, pieza.color)
        m = rh.Mesh()
        for v in tm.vertices:
            m.Vertices.Add(float(v[0]), float(v[1]), float(v[2]))
        for f in tm.faces:
            m.Faces.AddFace(int(f[0]), int(f[1]), int(f[2]))
        m.Normals.ComputeNormals()
        m.Compact()
        a = rh.ObjectAttributes()
        a.LayerIndex = idx
        a.Name = pieza.nombre
        a.ColorSource = rh.ObjectColorSource.ColorFromLayer
        self.m.Objects.AddMesh(m, a)

    def piezas(self, lista, prefijo=''):
        for p in lista:
            self.malla(p, prefijo)

    def texto(self, clave, valor):
        try:
            self.m.Strings.SetString(clave, valor)
        except Exception:
            pass

    def vista(self, nombre, posicion, objetivo, paralela=True):
        try:
            vi = rh.ViewInfo()
            vi.Name = nombre
            vp = vi.Viewport
            vp.SetCameraLocation(rh.Point3d(*posicion))
            d = np.array(objetivo) - np.array(posicion)
            vp.SetCameraDirection(rh.Vector3d(*d))
            vp.SetCameraUp(rh.Vector3d(0, 0, 1))
            if paralela:
                vp.ChangeToParallelProjection(True)
            self.m.NamedViews.Add(vi)
        except Exception:
            pass

    def guardar(self, ruta):
        if self.notas:
            try:
                self.m.Notes = self.notas
            except Exception:
                pass
        self.m.Write(ruta, 8)
        return ruta
