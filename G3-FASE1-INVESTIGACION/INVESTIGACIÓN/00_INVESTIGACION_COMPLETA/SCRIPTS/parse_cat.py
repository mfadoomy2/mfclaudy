import re, json
from shapely.geometry import Polygon, mapping, shape
from shapely.ops import unary_union
U="/mnt/user-data/uploads/G3 Proyectos/INVESTIGACIÓN/00_INVESTIGACION_COMPLETA/DATOS/CATASTRO_2026-09-23"
def rings(block):
    polys=[]
    for pm in re.findall(r"<gml:PolygonPatch>(.*?)</gml:PolygonPatch>",block,re.S):
        ext=re.search(r"<gml:exterior>.*?<gml:posList[^>]*>(.*?)</gml:posList>",pm,re.S)
        ints=re.findall(r"<gml:interior>.*?<gml:posList[^>]*>(.*?)</gml:posList>",pm,re.S)
        f=lambda s: [(float(a),float(b)) for a,b in zip(*[iter(s.split())]*2)]
        try: polys.append(Polygon(f(ext.group(1)),[f(i) for i in ints]).buffer(0))
        except Exception as e: pass
    return unary_union(polys) if polys else None
def tag(b,t):
    m=re.search(rf"<{t}[^>]*>([^<]*)</{t}>",b); return m.group(1).strip() if m else None
t=open(U+"/G3CAT_BU_Building_400m.gml",encoding="latin-1").read()
B=[]
for b in re.findall(r"<bu-ext2d:Building gml:id=\"ES\.SDGC\.BU\.([^\"]+)\">(.*?)</bu-ext2d:Building>",t,re.S):
    rc,blk=b; g=rings(blk)
    yr=re.search(r"<bu-core2d:beginning>(\d{4})",blk)
    B.append({"rc":rc,"anio":int(yr.group(1)) if yr else None,"uso":tag(blk,"bu-ext2d:currentUse"),"estado":tag(blk,"bu-core2d:conditionOfConstruction"),
      "unidades":int(tag(blk,"bu-ext2d:numberOfBuildingUnits") or 0),"viviendas":int(tag(blk,"bu-ext2d:numberOfDwellings") or 0),
      "sup_oficial":float(tag(blk,"bu-ext2d:value") or 0) if tag(blk,"bu-ext2d:value") else None,"geom":g})
t=open(U+"/G3CAT_BU_BuildingPart_400m.gml",encoding="latin-1").read()
P=[]
for rc,blk in re.findall(r"<bu-ext2d:BuildingPart gml:id=\"ES\.SDGC\.BU\.([^\"]+)\">(.*?)</bu-ext2d:BuildingPart>",t,re.S):
    fa=tag(blk,"bu-ext2d:numberOfFloorsAboveGround"); fb=tag(blk,"bu-ext2d:numberOfFloorsBelowGround")
    P.append({"id":rc,"rc":rc.split("_")[0],"plantas_sr":int(fa) if fa and fa.isdigit() else None,"plantas_br":int(fb) if fb and fb.isdigit() else None,"geom":rings(blk)})
print("edificios",len(B),"partes",len(P))
mx={}
for p in P:
    if p["plantas_sr"] is not None: mx[p["rc"]]=max(mx.get(p["rc"],0),p["plantas_sr"])
for b in B: b["plantas_max"]=mx.get(b["rc"])
def fc(L,name):
    feats=[{"type":"Feature","geometry":mapping(x["geom"]),"properties":{k:v for k,v in x.items() if k!="geom"}} for x in L if x["geom"] is not None and not x["geom"].is_empty]
    json.dump({"type":"FeatureCollection","name":name,"crs":{"type":"name","properties":{"name":"urn:ogc:def:crs:EPSG::25830"}},"features":feats},open(f"datos/{name}.geojson","w"))
    return len(feats)
print(fc(B,"catastro_edificios_400m"), fc(P,"catastro_partes_400m"))
import collections
print("usos",collections.Counter(b["uso"] for b in B).most_common())
print("con año",sum(1 for b in B if b["anio"]), "con plantas",sum(1 for b in B if b["plantas_max"] is not None))
print("plantas partes", collections.Counter(p["plantas_sr"] for p in P).most_common(15))
