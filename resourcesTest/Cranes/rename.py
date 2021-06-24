import os

i = 1
for f in os.listdir('.'):
    if f.startswith('gettyimages') and f.endswith('.jpg'):
        os.rename(f, str(i) + '.jpg')
        i += 1