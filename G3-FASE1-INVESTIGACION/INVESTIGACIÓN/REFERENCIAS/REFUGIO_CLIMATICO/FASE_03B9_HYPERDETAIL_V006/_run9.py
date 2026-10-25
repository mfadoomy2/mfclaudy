# -*- coding: utf-8 -*-
"""Runner forense 03B.6: python _run6.py <script.py> "<objetivo>" — ejecuta via flog.run."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, '..', '..', '_FORENSIC_PROCESS')))
import flog

ev = flog.run([sys.executable, os.path.join(HERE, sys.argv[1])] + sys.argv[3:], cwd=HERE,
              fase='03B6', objetivo=sys.argv[2] if len(sys.argv) > 2 else sys.argv[1])
print('LOGGED', ev)
code = ev[1].get('exit_code', 0) if isinstance(ev, tuple) and len(ev) > 1 and isinstance(ev[1], dict) else 0
sys.exit(code)
