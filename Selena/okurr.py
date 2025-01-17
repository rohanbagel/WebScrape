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
# cv2.imwrite(r"C:\movies\LEARN[PROJ]\WebScrape\Selena\data\nearbuy_inverted.png", inverted_img)
# display(r"C:\movies\LEARN[PROJ]\WebScrape\Selena\data\nearbuy_inverted.png")

def grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

gray_img = grayscale(img)
# # cv2.imwrite(r"C:\movies\LEARN[PROJ]\WebScrape\Selena\data\imgocr_gray.png", gray_img)

# # display(r"C:\movies\LEARN[PROJ]\WebScrape\Selena\data\imgocr_gray.png")

thresh, im_bw = cv2.threshold(gray_img, 200, 230, cv2.THRESH_BINARY)
# # cv2.imwrite(r"C:\movies\LEARN[PROJ]\WebScrape\Selena\data\imgocr_bw.png", im_bw)
# # display(r"C:\movies\LEARN[PROJ]\WebScrape\Selena\data\imgocr_bw.png")


def noise_removal(image):
    kernel = np.ones((1,1), np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    kernel = np.ones((1,1), np.uint8)
    image = cv2.erode(image, kernel, iterations=1)
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    image = cv2.medianBlur(image, 3)
    return image

no_noise = noise_removal(im_bw)
# cv2.imwrite(r"C:\movies\LEARN[PROJ]\WebScrape\Selena\data\no_noise.png", no_noise)
# display(r"C:\movies\LEARN[PROJ]\WebScrape\Selena\data\no_noise.png")


def thin_font(image):
    image = cv2.bitwise_not(image)
    kernel = np.ones((1,1), np.uint8)
    image = cv2.erode(image,kernel,iterations=1)
    image = cv2.bitwise_not(image)
    return image

eroded_image = thin_font(no_noise)
# cv2.imwrite(f"C:\movies\LEARN[PROJ]\WebScrape\Selena\data\eroded_img.png", eroded_image)
# display(f"C:\movies\LEARN[PROJ]\WebScrape\Selena\data\eroded_img.png")

def thick_font(image):
    image = cv2.bitwise_not(image)
    kernel = np.ones((1,1), np.uint8)
    image = cv2.dilate(image,kernel,iterations=1)
    image = cv2.bitwise_not(image)
    return image

dilated_image = thick_font(no_noise)
cv2.imwrite(f"C:\movies\LEARN[PROJ]\WebScrape\Selena\data\dilated_img.png", dilated_image)
display(f"C:\movies\LEARN[PROJ]\WebScrape\Selena\data\dilated_img.png")

#https://becominghuman.ai/how-to-automatically-deskew-straighten-a-text-image-using-opencv-a0c30aed83df
def getSkewAngle(cvImage) -> float:
    # Prep image, copy, convert to gray scale, blur, and threshold
    newImage = cvImage.copy()
    gray = cv2.cvtColor(newImage, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9, 9), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Apply dilate to merge text into meaningful lines/paragraphs.
    # Use larger kernel on X axis to merge characters into single line, cancelling out any spaces.
    # But use smaller kernel on Y axis to separate between different blocks of text
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 5))
    dilate = cv2.dilate(thresh, kernel, iterations=2)

    # Find all contours
    contours, hierarchy = cv2.findContours(dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key = cv2.contourArea, reverse = True)
    for c in contours:
        rect = cv2.boundingRect(c)
        x,y,w,h = rect
        cv2.rectangle(newImage,(x,y),(x+w,y+h),(0,255,0),2)

    # Find largest contour and surround in min area box
    largestContour = contours[0]
    print (len(contours))
    minAreaRect = cv2.minAreaRect(largestContour)
    cv2.imwrite("temp/boxes.jpg", newImage)
    # Determine the angle. Convert it to the value that was originally used to obtain skewed image
    angle = minAreaRect[-1]
    if angle < -45:
        angle = 90 + angle
    return -1.0 * angle
# Rotate the image around its center
def rotateImage(cvImage, angle: float):
    newImage = cvImage.copy()
    (h, w) = newImage.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    newImage = cv2.warpAffine(newImage, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return newImage

# Deskew image
def deskew(cvImage):
    angle = getSkewAngle(cvImage)
    return rotateImage(cvImage, -1.0 * angle)