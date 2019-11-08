from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage
from matplotlib.offsetbox import AnnotationBbox
import glob
import os


def setup(width, height):
    bg_h = height * 81
    bg_w = width * 81
    background = Image.new('RGB', (bg_w, bg_h), (96, 86, 89))
    background.save("image_files/board_images/background.png")


def placeblocks(dictofblocks, backgroundimage, width, height):
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
    for coordinate in coordinate_list:
        x, y = coordinate
        background.paste(openspace, ((x * xscalefactor), y * yscalefactor))
        background.save('image_files/board_images/background.png')


def plotlazorpath(lazorpath, width, height, listoflazors):
    normal = Image.open('image_files/board_images/background.png')
    rotated = normal.rotate(180)
    flipped = rotated.transpose(Image.FLIP_LEFT_RIGHT)
    flipped.save('image_files/board_images/background.png')
    x, y = zip(*lazorpath)
    img = plt.imread('image_files/board_images/background.png')
    fig, ax = plt.subplots()
    ax.imshow(img, extent=[0, width*2, 0, height*2])
    line, = ax.plot(x, y, color='r')
    plt.axis('off')
    ax.set_ylim(ax.get_ylim()[::-1])

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
    for target in targetlist:
        k, l = target
        tb = AnnotationBbox(targetbox, (k, l), bboxprops=target_props)
        ax.add_artist(tb)

    for n in range(len(x)):
        line.set_data(x[:n], y[:n])
        fig.savefig('image_files/solution_images/Frame%03d.png' %
                    n, bbox_inches='tight', bbox_color='white')


def animate(fp_in, fp_out):
    img, *imgs = [Image.open(f) for f in sorted(glob.glob(fp_in))]
    img.save(fp=fp_out, format='GIF', append_images=imgs,
             save_all=True, duration=75, loop=10)
    files = glob.glob(r'image_files/solution_images/*')
    for items in files:
        os.remove(items)


if __name__ == '__main__':
    width = 5
    height = 6
    bg = setup(width, height)

    dictofblocks = {(1, 0): 'B', (1, 1): 'A', (0, 2): 'A', (4, 2): 'A', (2, 3): 'A', (0, 4): 'A', (4, 4): 'A', (0, 5): 'B', (1, 5): 'A', (3, 5): 'A'}
    block = placeblocks(dictofblocks, 'image_files/board_images/background.png', width, height)

    targetlist = [(6, 9), (9, 2)]
    lazorlist = [(4, 1)]
    lazorpath = [(4, 1), (5, 2), (6, 3), (7, 4), (8, 5), (8, 5), (7, 6), (6, 7), (6, 7), (7, 8), (8, 9), (8, 9), (7, 10), (7, 10), (6, 9), (5, 8), (5, 8), (4, 9), (3, 10), (3, 10), (2, 9), (2, 9), (3, 8), (4, 7), (4, 7), (3, 6), (2, 5), (2, 5), (3, 4), (3, 4), (4, 5), (5, 6), (5, 6), (6, 5), (7, 4), (8, 3), (9, 2), (10, 1)]
    plotlazorpath(lazorpath, width, height, lazorlist)

    fp_in = 'image_files/solution_images/Frame0*.png'
    fp_out = 'yarn5solution.gif'

    animate(fp_in, fp_out)
