from pathlib import Path
import runpy,gc
R=Path(__file__).parent
for n in ['analizar_luz.py','analizar_luz_v5.py','analizar_luz_pb.py']:
 print('INICIO',n,flush=True)
 runpy.run_path(str(R/n),run_name='__main__')
 gc.collect()
print('TODOS_LOS_ENSAYOS_COMPLETOS',flush=True)
