from PIL import Image
import cv2
from matplotlib import pyplot as plt
import numpy as np

im_file = r"C:\movies\LEARN[PROJ]\WebScrape\Selena\data\imgocr.png"
img = cv2.imread(im_file)

def display(im_path):
    dpi = 80
    im_data = plt.imread(im_path)
    if len(im_data.shape) == 3:
        height, width, depth = im_data.shape
    else:
        height, width = im_data.shape
        depth = 1
    
    figsize = width / float(dpi), height / float(dpi)
    
    fig = plt.figure(figsize=figsize)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('off')
    ax.imshow(im_data, cmap='gray' if depth == 1 else None)
    
    plt.show()
    
# display(im_file)

# inverted_img = cv2.bitwise_not(img)
# cv2.imwrite(r"C:\movies\LEARN[PROJ]\WebScrape\Selena\data\imgocr_inverted.png", inverted_img)
# display(r"C:\movies\LEARN[PROJ]\WebScrape\Selena\data\imgocr_inverted.png")

def grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

gray_img = grayscale(img)
# cv2.imwrite(r"C:\movies\LEARN[PROJ]\WebScrape\Selena\data\imgocr_gray.png", gray_img)

# display(r"C:\movies\LEARN[PROJ]\WebScrape\Selena\data\imgocr_gray.png")

thresh, im_bw = cv2.threshold(gray_img, 200, 230, cv2.THRESH_BINARY)
# cv2.imwrite(r"C:\movies\LEARN[PROJ]\WebScrape\Selena\data\imgocr_bw.png", im_bw)
# display(r"C:\movies\LEARN[PROJ]\WebScrape\Selena\data\imgocr_bw.png")


def noise_removal(image):
    kernel = np.ones((1,1), np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    kernel = np.ones((1,1), np.uint8)
    image = cv2.erode(image, kernel, iterations=1)
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    image = cv2.medianBlur(image, 3)
    return image

# no_noise = noise_removal(im_bw)
# cv2.imwrite(r"C:\movies\LEARN[PROJ]\WebScrape\Selena\data\no_noise.png", no_noise)
# display(r"C:\movies\LEARN[PROJ]\WebScrape\Selena\data\no_noise.png")