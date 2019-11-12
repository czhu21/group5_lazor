from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage
from matplotlib.offsetbox import AnnotationBbox
import glob
import os
from simulate_board import Lazor

def place_blocks(dictofblocks, backgroundimage, width, height, empty):
	bg_h = height * 81
	bg_w = width * 81
	background = Image.new('RGB', (bg_w, bg_h), (96, 86, 89))
	background.save("image_files/board_images/background.png")
	background = Image.open(backgroundimage)
	absorb = Image.open('image_files/board_images/absorb.png')
	reflect = Image.open('image_files/board_images/reflect.png')
	refract = Image.open('image_files/board_images/refract.png')
	openspace = Image.open('image_files/board_images/openspace.png')
	bg_w, bg_h = background.size
	xscalefactor = int(bg_w/width)
	yscalefactor = int(bg_h/height)
	coordinate_list = []
	for i in range(width):
		for j in range(height):
			coordinate_list.append((i, j))
	for coordinate, block in dictofblocks.items():
		x, y = coordinate
		newx = 0
		newy = 0
		if block == 'A':
			background.paste(reflect, (x*xscalefactor, y*yscalefactor))
			background.save('image_files/board_images/background.png')
		elif block == 'B':
			background.paste(absorb, (x*xscalefactor, y*yscalefactor))
			background.save('image_files/board_images/background.png')
		elif block == 'C':
			background.paste(refract, ((x * xscalefactor), y * yscalefactor))
			background.save('image_files/board_images/background.png')
	open_spaces = []
	for coordinate in dictofblocks.keys():
		if coordinate in coordinate_list:
			coordinate_list.remove(coordinate)
	for (i, j) in empty:
		if (i, j) in coordinate_list:
			coordinate_list.remove((i, j))
	for coordinate in coordinate_list:
		x, y = coordinate
		background.paste(openspace, ((x * xscalefactor), y * yscalefactor))
		background.save('image_files/board_images/background.png')


def plot_lazor_path(listOfLazors, width, height, lasers, targetList, filename):
	lazorlist = []
	for lazor in lasers:
		lazorlist.append((lazor[0], lazor[1]))
	normal = Image.open('image_files/board_images/background.png')
	rotated = normal.rotate(180)
	flipped = rotated.transpose(Image.FLIP_LEFT_RIGHT)
	flipped.save('image_files/board_images/background.png')
	fig, ax = plt.subplots()
	img = plt.imread('image_files/board_images/background.png')
	ax.imshow(img, extent=[0, width*2, 0, height*2])
	plt.axis('off')
	ax.set_ylim(ax.get_ylim()[::-1])

	lazorPathList = []

	for lazor in listOfLazors:
		new = []
		for point in lazor.path:
			new.append(point[0])
		lazorPathList.append(new)

	


	for lazor in lazorPathList:
		x, y = zip(*lazor)
		line, = ax.plot(x, y, color='r')

	
	target_props = dict(boxstyle="circle,pad=0.001",
						fc="black", ec="b", lw=0.01)
	lazor_props = dict(boxstyle="circle,pad=0.001", fc="red", ec="r", lw=0.01)

	lazorimg = plt.imread('image_files/board_images/lazororigin.png')

	lazorbox = OffsetImage(lazorimg, zoom=0.25)
	lazorbox.image.axes = ax
	for lazor in lazorlist:
		i, j = lazor
		lb = AnnotationBbox(lazorbox, (i, j), bboxprops=lazor_props)
		ax.add_artist(lb)

	targetimg = plt.imread('image_files/board_images/targetimage.png')

	targetbox = OffsetImage(targetimg, zoom=0.5)
	targetbox.image.axes = ax
	for target in targetList:
		k, l = target
		tb = AnnotationBbox(targetbox, (k, l), bboxprops=target_props)
		ax.add_artist(tb)

	# for lazor in lazorPathList:
	# for n in range(len(x)):
		# lin = line.set_data(x[:n], y[:n])
	fname1 = filename.split('.')[0]
	fname2 = fname1.split('/')[1]
	fig.savefig('image_files/solution_images/{}_solution.png'.format(fname2), bbox_inches='tight', bbox_color='white')


def animate():
	fp_in = 'image_files/solution_images/Frame0*.png'
	fp_out = 'solution.gif'
	img, *imgs = [Image.open(f) for f in sorted(glob.glob(fp_in))]
	img.save(fp=fp_out, format='GIF', append_images=imgs,
			 save_all=True, duration=75, loop=3)
	files = glob.glob(r'image_files/solution_images/*')
	for items in files:
		os.remove(items)

if __name__ == '__main__':
	pass
