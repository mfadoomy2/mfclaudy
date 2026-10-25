import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
for f in ["/home/claude/fonts/G400.ttf","/home/claude/fonts/G700.ttf","/home/claude/fonts/GI400.ttf"]: fm.fontManager.addfont(f)
FAM=fm.FontProperties(fname="/home/claude/fonts/G400.ttf").get_name()
plt.rcParams.update({"font.family":FAM,"font.size":6.5,"axes.linewidth":0.4,"xtick.major.width":0.4,"ytick.major.width":0.4,
  "xtick.major.size":2,"ytick.major.size":2,"axes.edgecolor":"#33322e","axes.labelcolor":"#33322e","xtick.color":"#33322e","ytick.color":"#33322e",
  "savefig.dpi":300,"axes.spines.top":False,"axes.spines.right":False})
TINTA="#1c1c1c"; MAG="#e5007e"; ROSA="#f2a0c0"; VERDE="#1f6f50"; HOJA="#7fbf9e"; AGUA="#2e7f9e"; PANEL="#f6f3ee"; FILETE="#cfcac2"
PIEDRA="#EDEAE4"; CONTX="#B5B1A9"; TEC="#33322e"; COBRE="#B08968"
CALOR=["#fff5eb","#fdd9b5","#f8a870","#e8683a","#c0392b","#7a1616"]
MM=1/25.4
def fig_mm(w,h): return plt.figure(figsize=(w*MM,h*MM))
def spaced(s): return " ".join(list(s.upper())).replace("   ","  ")
