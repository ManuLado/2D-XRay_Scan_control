"""
Paste one image on top of another such that given points in each are coincident.
"""

from PIL import Image , ImageDraw, ImageFont

def hcombine(imagen1,imagen2,resultado):
	# Open images and ensure RGB
	#im1 = Image.open(imagen1).convert('RGB')
	im1=imagen1
	size1=im1.size

	#im2 = Image.open(imagen2).convert('RGB')
	im2=imagen2
	size2=im2.size

	# x,y coordinates of point in each image
	p1x, p1y = int(size1[0]), 0
	p2x, p2y = 0, 0
	
	# Draw a diagonal blue line with thickness of 5 px
	draw = ImageDraw.Draw(im1) 
	draw.line((0,int(size1[1]/2), int(size1[0]), int(size1[1]/2)), fill=(100,255,100,128), width=1)
	draw.line((int(size1[0]/2),0, int(size1[0]/2), int(size1[1])), fill=(100,255,100,128), width=1)
	draw.text((int(size1[0]/2),int(size1[1]/2)), str(resultado), fill=(255,100,0,128))
	gridtick=10
	#fnt = ImageFont.truetype("Pillow/Tests/fonts/FreeMono.ttf", 40)
	for x in range(0, size1[0], int(size1[0] / gridtick)):
		line = ((x, 0), (x, size1[0]))
		draw.line(line, fill=(255,255,255,128))
		draw.text((x,10), str(x), fill=(255,255,255,128))
	
	for y in range(0, size1[0], int(size1[0] / gridtick)):
		line = ((0, y), (size1[0], y))
		draw.line(line, fill=(255,255,255,128))
		draw.text((10,y), str(y), fill=(255,255,255,128))
	#'''
	#im1.save('line1.png')
	draw = ImageDraw.Draw(im2) 
	draw.line((0,int(size2[1]/2), int(size2[0]), int(size2[1]/2)), fill=(100,255,0,128), width=1)
	draw.line((int(size2[0]/2),0, int(size2[0]/2), int(size2[1])), fill=(100,255,0,128), width=1)
	
	for x in range(0, size2[0], int(size2[0] / gridtick)):
		line = ((x, 0), (x, size2[0]))
		draw.line(line, fill=(255,255,255,128))
		draw.text((x,10), str(x), fill=(255,255,255,128))
	for y in range(0, size2[0], int(size2[0] / gridtick)):
		line = ((0, y), (size2[0], y))
		draw.line(line, fill=(255,255,255,128))	
		draw.text((10,y), str(y), fill=(255,255,255,128))
	im2.save('line2.png')
	#'''
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
	bg.save(resultado+'.png')
	res=Image.open(resultado+'.png').convert('RGB')
	return res

def vcombine(imagen1,imagen2,resultado):
	# Open images and ensure RGB
	#im1 = Image.open(imagen1).convert('RGB')
	im1=imagen1
	size1=im1.size

	#im2 = Image.open(imagen2).convert('RGB')
	im2=imagen2
	size2=im2.size

	# x,y coordinates of point in each image
	p1x, p1y = 0, int(size1[1])
	p2x, p2y = 0, 0
	'''
	# Draw a diagonal blue line with thickness of 5 px
	draw = ImageDraw.Draw(im1) 
	draw.line((0,int(size1[1]/2), int(size1[0]), int(size1[1]/2)), fill=(100,255,100,128), width=1)
	draw.line((int(size1[0]/2),0, int(size1[0]/2), int(size1[1])), fill=(100,255,100,128), width=1)
	gridtick=10
	for x in range(0, size1[0], int(size1[0] / gridtick)):
		line = ((x, 0), (x, size1[1]))
		draw.line(line, fill=(255,255,255,128))

	for y in range(0, size1[1], int(size1[1] / gridtick)):
		line = ((0, y), (size1[1], y))
		draw.line(line, fill=(255,255,255,128))

	#im1.save('line1.png')
	draw = ImageDraw.Draw(im2) 
	draw.line((0,int(size2[1]/2), int(size2[0]), int(size2[1]/2)), fill=(100,255,0,128), width=1)
	draw.line((int(size2[0]/2),0, int(size2[0]/2), int(size2[1])), fill=(100,255,0,128), width=1)
	
	for x in range(0, size1[0], int(size1[0] / gridtick)):
		line = ((x, 0), (x, size1[0]))
		draw.line(line, fill=(255,255,255,128))
		draw.text((x,10), str(x), fill=(255,255,255,128))
	
	for y in range(0, size1[1], int(size1[1] / gridtick)):
		line = ((0, y), (size1[1], y))
		draw.line(line, fill=(255,255,255,128))
		draw.text((10,y), str(y), fill=(255,10,255,128))

	#im2.save('line2.png')
	'''
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
	bg.save(resultado+'.png')
	res=Image.open(resultado+'.png').convert('RGB')
	return res