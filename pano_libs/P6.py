"""
Paste one image on top of another such that given points in each are coincident.
"""

from PIL import Image

# Open images and ensure RGB
im1 = Image.open('1.jpg').convert('RGB')
size1=im1.size

im2 = Image.open('2.jpg').convert('RGB')
size2=im2.size

# x,y coordinates of point in each image
p1x, p1y = int(size1[0]/2), 0
p2x, p2y = 0, 0

# Work out how many pixels of space we need left, right, above, below common point in new image
pL = max(p1x, p2x)
pR = max(im1.width-p1x,  im2.width-p2x)
pT = max(p1y, p2y)
pB = max(im1.height-p1y, im2.height-p2y)

# Create background in solid white
bg = Image.new('RGB', (pL+pR, pT+pB),'white')
bg.save('DEBUG-bg.png')

# Paste im1 onto background
bg.paste(im1, (pL-p1x, pT-p1y))
bg.save('DEBUG-bg+im1.png')

# Make 40% opacity mask for im2
alpha = Image.new('L', (im2.width,im2.height), int(100*255/100))
alpha.save('DEBUG-alpha.png')

# Paste im2 over background with alpha
bg.paste(im2, (pL-p2x, pT-p2y), alpha)
bg.save('result.png')