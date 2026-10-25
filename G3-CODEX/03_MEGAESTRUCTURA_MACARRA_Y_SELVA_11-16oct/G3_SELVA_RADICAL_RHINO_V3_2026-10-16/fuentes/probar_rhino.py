# -*- coding: utf-8 -*-
import Rhino, System, json
p='/Volumes/T7/G3 Proyectos/G3 CLAUDE/03_MEGAESTRUCTURA_MACARRA_Y_SELVA_11-16oct/G3_SELVA_RADICAL_RHINO_V3_2026-10-16/verificacion/rhino_disponible.json'
a={'version':str(Rhino.RhinoApp.Version),'doc':Rhino.RhinoDoc.ActiveDoc.Name,'python':'native','brep_loft':hasattr(Rhino.Geometry.Brep,'CreateFromLoft'),'pipe':hasattr(Rhino.Geometry.Brep,'CreatePipe')}
with open(p,'w') as f:json.dump(a,f)
print('SELVA_V3_RHINO_OK')
