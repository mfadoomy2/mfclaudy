import geometria as G
import matplotlib.pyplot as plt
fig,axs=plt.subplots(1,3,figsize=(18,8))
for ax,f in zip(axs,[G.F[2],G.F[6],G.F[7]]):
 G.draw(ax,f['floor'],'#eee8da');G.draw(ax,f['priv'],'#d8e1d1');G.draw(ax,f['solid'],'#465c51')
 for g in f['furniture']:G.draw(ax,g,'#c07196')
 G.draw(ax,f['free'],'#299a9d',alpha=.5)
 ep=f['entry']['inside'];ax.plot(*ep,'ro');ax.text(*ep,'ENTRY')
 for i,p in enumerate(f['approaches']):ax.plot(p.x,p.y,'bo');ax.text(p.x,p.y,str(i+1))
 ax.set_aspect('equal');ax.set_title(f['audit']['codigo'])
fig.savefig(G.P/'verificacion/DEBUG.png',dpi=130)
for f in [G.F[2],G.F[6]]:
 p=G.Point(f['entry']['inside']);print(f['audit']['codigo'],'root',f['root'] is not None,'dist_solid',p.distance(f['solid']),'furnituredists',[round(p.distance(g),2) for g in f['furniture']])
