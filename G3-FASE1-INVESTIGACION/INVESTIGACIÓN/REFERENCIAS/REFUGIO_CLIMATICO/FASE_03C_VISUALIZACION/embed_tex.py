import base64
import os

HERE = os.path.dirname(os.path.abspath(__file__))
d = os.path.join(HERE, '_viewer', 'tex')
out = []
for (var, fn) in [('GRAN_COL_URI', 'granito.jpg'), ('GRAN_RGH_URI', 'granito_rough.jpg')]:
    b = base64.b64encode(open(os.path.join(d, fn), 'rb').read()).decode()
    out.append('const %s = "data:image/jpeg;base64,%s";' % (var, b))
dst = os.path.join(HERE, '_viewer', 'tex_data.js')
open(dst, 'w').write('\n'.join(out))
print('tex_data.js', os.path.getsize(dst) // 1024, 'KB')
