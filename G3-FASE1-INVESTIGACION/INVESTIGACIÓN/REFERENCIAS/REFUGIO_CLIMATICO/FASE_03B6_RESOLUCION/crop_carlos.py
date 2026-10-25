import os

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.normpath(os.path.join(HERE, '..', '..', 'MONTESERIN IA', 'MONTESERIN IA',
                                    'MUTACIONES (DIBUJO + IA)', 'DIBUJO3 (REFUGIO CLIMATICO)',
                                    'IN PROGRESS REFUGIO', '0F53E6F0-C499-4057-8C95-A0928F3680D9.png'))
im = Image.open(SRC)
w, h = im.size
print('size', im.size)
crop = im.crop((int(w * 0.38), int(h * 0.28), int(w * 0.64), int(h * 0.62)))
crop = crop.resize((crop.width * 2, crop.height * 2), Image.LANCZOS)
crop.save(os.path.join(HERE, '_carlos_iii_zoom.png'))
print('crop ok', crop.size)
