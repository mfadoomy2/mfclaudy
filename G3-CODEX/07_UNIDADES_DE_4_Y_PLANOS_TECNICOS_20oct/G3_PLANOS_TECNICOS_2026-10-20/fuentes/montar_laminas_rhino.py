# -*- coding: utf-8 -*-
import Rhino, System, scriptcontext as sc
import os,json,math,traceback
from System.Drawing import Color
ROOT=u'/Volumes/T7/G3 Proyectos/G3 CLAUDE/07_UNIDADES_DE_4_Y_PLANOS_TECNICOS_20oct/G3_PLANOS_TECNICOS_2026-10-20'
doc=Rhino.RhinoDoc.ActiveDoc
report={'errors':[],'layouts':[],'texts':0,'curves':0,'hatches':0}
try:
    data=json.load(open(os.path.join(ROOT,'fuentes','DIBUJO_VECTORIAL.json')))
    if doc.Objects.Count>0:raise Exception('Este script exige un documento nuevo para no alterar el modelo abierto.')
    doc.ModelUnitSystem=Rhino.UnitSystem.Meters;doc.PageUnitSystem=Rhino.UnitSystem.Millimeters
    doc.ModelAbsoluteTolerance=.001;doc.ModelDistanceDisplayPrecision=3
    font=Rhino.DocObjects.Font('Ibarra Real Nova',Rhino.DocObjects.Font.FontWeight.Normal,Rhino.DocObjects.Font.FontStyle.Italic,False,False)
    style=Rhino.DocObjects.DimensionStyle();style.Name='G3_Ibarra_Real_Nova';style.Font=font;style.TextHeight=.25
    si=doc.DimStyles.Add(style,False);styleid=doc.DimStyles[si].Id
    layers={};ltypes={}
    def attrs(page,kind,lw=.13,dash=None):
        key=page+'_'+kind
        if key not in layers:
            la=Rhino.DocObjects.Layer();la.Name=key;la.Color=Color.Black;la.PlotColor=Color.Black;la.PlotWeight=lw
            layers[key]=doc.Layers.Add(la)
        a=Rhino.DocObjects.ObjectAttributes();a.LayerIndex=layers[key];a.PlotWeightSource=Rhino.DocObjects.ObjectPlotWeightSource.PlotWeightFromObject;a.PlotWeight=lw
        a.PlotColorSource=Rhino.DocObjects.ObjectPlotColorSource.PlotColorFromObject;a.PlotColor=Color.Black
        if dash:
            dk=tuple(dash)
            if dk not in ltypes:
                lt=Rhino.DocObjects.Linetype();lt.Name='G3_'+str(len(ltypes))
                for j,v in enumerate(dash):lt.AppendSegment(v/10.0,j%2==0)
                ltypes[dk]=doc.Linetypes.Add(lt)
            a.LinetypeIndex=ltypes[dk];a.LinetypeSource=Rhino.DocObjects.ObjectLinetypeSource.LinetypeFromObject
        return a
    pages=[]
    for i,s in enumerate(data):
        ox=i*70.0
        def point(p):return Rhino.Geometry.Point3d(ox+p[0]/10.,p[1]/10.,0)
        for op in s['ops']:
            a=attrs(s['page'],op['kind'],op.get('lw',.13),op.get('dash'))
            if op['type']=='text':
                te=Rhino.Geometry.TextEntity();te.PlainText=op['text'];te.DimensionStyleId=styleid;te.TextHeight=op['height']/10.
                plane=Rhino.Geometry.Plane(point(op['point']),Rhino.Geometry.Vector3d.ZAxis)
                plane.Rotate(math.radians(op['angle']),Rhino.Geometry.Vector3d.ZAxis,plane.Origin);te.Plane=plane
                te.Justification={'left':Rhino.Geometry.TextJustification.BottomLeft,'center':Rhino.Geometry.TextJustification.BottomCenter,'right':Rhino.Geometry.TextJustification.BottomRight}[op['align']]
                doc.Objects.AddText(te,a);report['texts']+=1;continue
            rings=op['rings'] if op['type']=='polygon' else [op['points']]
            curves=[]
            for ring in rings:
                pp=[point(p) for p in ring]
                if op['type']=='polygon' and pp[0].DistanceTo(pp[-1])>.000001:pp.append(pp[0])
                cv=Rhino.Geometry.PolylineCurve(pp);curves.append(cv);doc.Objects.AddCurve(cv,a);report['curves']+=1
            if op.get('fill')==0:
                try:
                    hs=Rhino.Geometry.Hatch.Create(curves,0,0.,1.,.001)
                    for hatch in hs or []:doc.Objects.AddHatch(hatch,a);report['hatches']+=1
                except Exception as e:report['errors'].append('Hatch: '+str(e))
        page=doc.Views.AddPageView(s['page']+'_'+s['code']+'_1_100',s['width'],s['height'])
        if page is None:raise Exception('No se pudo crear layout '+s['code'])
        detail=page.AddDetailView('PLANTA_'+s['code'],Rhino.Geometry.Point2d(0,0),Rhino.Geometry.Point2d(s['width'],s['height']),Rhino.Display.DefinedViewportProjection.Top)
        bb=Rhino.Geometry.BoundingBox(Rhino.Geometry.Point3d(ox,0,-.01),Rhino.Geometry.Point3d(ox+s['width']/10.,s['height']/10.,.01))
        detail.Viewport.ZoomBoundingBox(bb);detail.CommitViewportChanges()
        ok=detail.DetailGeometry.SetScale(1.0,Rhino.UnitSystem.Meters,10.0,Rhino.UnitSystem.Millimeters)
        detail.DetailGeometry.IsProjectionLocked=True;detail.CommitChanges()
        report['layouts'].append({'name':page.PageName,'paper_mm':[s['width'],s['height']],'scale_1m_to_10mm':bool(ok),'ratio':detail.DetailGeometry.PageToModelRatio})
        pages.append(page)
    if pages:doc.Views.ActiveView=pages[0];pages[0].SetPageAsActive()
    doc.Views.Redraw()
    dest=os.path.join(ROOT,'modelos','PLANOS_EDITABLES_Y_LAYOUTS_1_100.3dm')
    options=Rhino.FileIO.FileWriteOptions();options.FileVersion=8
    report['saved']=doc.WriteFile(dest,options);report['path']=dest
    report['font_face']=str(font)
    with open(os.path.join(ROOT,'verificacion','LAYOUTS_RHINO.json'),'w') as stream:json.dump(report,stream,ensure_ascii=True)
    print('G3: '+str(len(report['layouts']))+' layouts 1:100; '+str(report['texts'])+' textos; archivo guardado '+str(report['saved']))
except:
    report['fatal']=traceback.format_exc()
    with open(os.path.join(ROOT,'verificacion','LAYOUTS_RHINO_ERROR.json'),'w') as stream:json.dump(report,stream,ensure_ascii=True)
    print(traceback.format_exc())
