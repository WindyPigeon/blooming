# Topic: Image Processing – Manipulate Image Continue

**Package :**

* Numpy – dealing with matrix / array creation and calculation

* Opencv - dealing with image processing

* Pillow – another image library for manipulating images

**References:**

Open CV: [OpenCV: OpenCV modules](https://docs.opencv.org/4.x/index.html)

Numpy: [NumPy user guide — NumPy v2.1 Manual](https://numpy.org/doc/2.1/user/index.html)

PIL: [Pillow (PIL Fork) 11.1.0 documentation](https://pillow.readthedocs.io/en/stable/index.html)

# Add Noise

1. Import the relevant library – open cv and numpy.

```python
import cv2
import numpy as np
```

2. You may use old images from previous exercise. Read the image and enlarge it if necessary.

```python
image = cv2.imread("lab\\sceneImage.jpeg")
w,h = image.shape[:2]
image = cv2.resize(image, (h*2, w*2))
```

3. Create a function to add Gaussion Noise into existing image the image.

   * Using numpy to create random noise – normal distribution same size as image shape.

   * Add the noise to the image

   * Now show the image

```python
def addGaussianNoise():
    #0=average value-centre of noise, 10-noise strength
    noise = np.random.normal(0, 10, image.shape).astype(np.uint8)
    noisyImg = cv2.add(image, noise)
    cv2.imshow("GaussianNoise", noisyImg)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
```

4. Create another function to add salt and paper noise.

   * Copy the image

   * Use numpy to create random noise – 5% of the image array size. – for white and black dots.

   * Update the noise color in the existing image.

   * Show the image

```python
def saltPepperNoise():
    noisyImg = np.copy(image)

   #white noise - 5%
    saltMask = np.random.random(image.shape[:2]) < 0.05
    noisyImg[saltMask] = 255

    # black noise - 5%
    pepperMask = np.random.random(image.shape[:2]) < 0.05
    noisyImg[pepperMask] = 0

    cv2.imshow("GaussianNoise", noisyImg)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
```

5. You may test run program to check out the noise images

6. Lets test other libraries. PILLOW.

   * Import the library

```python
from PIL import Image, ImageDraw, ImageFilter, ImageFont
```

   * read and reside the images

```python
img1 = Image.open("lab\\sceneImage.jpeg").convert("RGBA")
img2 = Image.open("lab\\cartoonCharacter.png").convert("RGBA")
w, h = img1.size
img1 = img1.resize((w*2, h*2), Image.LANCZOS)
img2 = img2.resize(img1.size, Image.LANCZOS)
```

7. Blend two images together. Create a function to combine both images together. First image normal, second image – set the alpha value for transparency.

```python
def blendImage():
    blendedImg = Image.blend(img1, img2, 0.5) #alpha 0.5
    blendedImg.show()
```

8. Combine both image together by attaching one image on top of another image. Create a function to do this. The set second image with transparent – alpha value. So it will look like Q7.

```python
def compositeImage():
    compositeImg = img1.copy()
    #compositeImg.paste(img2, (100,200), img2) #paste image at specific position
    img2.putalpha(100) # add transparency
    compositeImg = Image.alpha_composite(img1, img2)
    compositeImg.show()
```

9. Add the Masking features. Create a function to do this.

   * Create a mask – duplicate the image by duplicating the image.

   * Create an ellipse, so that we can see the background image in the circle.

   * Create another image – same size with RGBA(transparency)

   * Now paste the image with the mask.

```python
def addMask():

    # Create a mask
    mask = Image.new("L", img1.size, 0)
    draw = ImageDraw.Draw(mask)

    #white ellipse -view area
    draw.ellipse((50, 50, 250, 250), fill=255)
    maskImage = Image.new("RGBA", img1.size)
    maskImage.paste(img1, (0, 0), mask=mask)
    maskImage.show()
```

10. Create a function to blur the image using the filter function.

```python
def gaussionBlur():
blurImage = img1.filter(ImageFilter.GaussianBlur(radius=5))
blurImage.show()
```

11. Test run all the functions.

<ins>**Full coding**</ins>

```python
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

#using opencv
image = cv2.imread("lab\\sceneImage.jpeg")
w,h = image.shape[:2]
image = cv2.resize(image, (h*2, w*2))

#using pillow
img1 = Image.open("lab\\sceneImage.jpeg").convert("RGBA")
img2 = Image.open("lab\\cartoonCharacter.png").convert("RGBA")
w, h = img1.size
img1 = img1.resize((w*2, h*2), Image.LANCZOS)
img2 = img2.resize(img1.size, Image.LANCZOS)

# Gaussian noise
def addGaussianNoise():
# Generate noise
#0=average value-centre of noise, 10-noise strenght
noise = np.random.normal(0, 10, image.shape).astype(np.uint8)
noisyImg = cv2.add(image, noise)
cv2.imshow("GaussianNoise", noisyImg)
cv2.waitKey(0)
cv2.destroyAllWindows()

#Salt and pepper noise
def saltPepperNoise():
noisyImg = np.copy(image)

#white noise - 5%
saltMask = np.random.random(image.shape[:2]) < 0.05
noisyImg[saltMask] = 255

# black noise - 5%
pepperMask = np.random.random(image.shape[:2]) < 0.05
noisyImg[pepperMask] = 0

cv2.imshow("GaussianNoise", noisyImg)
cv2.waitKey(0)
cv2.destroyAllWindows()

def blendImage():
blendedImg = Image.blend(img1, img2, 0.5) #alpha 0.5
blendedImg.show()

def compositeImage():
compositeImg = img1.copy()
compositeImg.paste(img2, (100,200), img2) #paste image at specific position
img2.putalpha(100) # add transparency
compositeImg = Image.alpha_composite(img1, img2)
compositeImg.show()

def addMask():

# Create a mask
mask = Image.new("L", img1.size, 0)
draw = ImageDraw.Draw(mask)

#white ellipse -view area
draw.ellipse((50, 50, 250, 250), fill=255)
maskImage = Image.new("RGBA", img1.size)
maskImage.paste(img1, (0, 0), mask=mask)
maskImage.show()

def gaussionBlur():
blurImage = img1.filter(ImageFilter.GaussianBlur(radius=5))
blurImage.show()

def SharpeningImage():
# radius – Blur Radius
# percent – Unsharp strength, in percent
# threshold – Threshold controls the minimum brightness change that will be sharpened
# class PIL.ImageFilter.UnsharpMask(radius: float = 2, percent: int = 150, threshold: int = 3)
sharpImage = img1.filter(ImageFilter.UnsharpMask(10, 100,4 ))
sharpImage.show()

#addGaussianNoise()
#saltPepperNoise()
#blendImage()
#compositeImage()
#addMask()
#gaussionBlur()
#SharpeningImage()
```

# Task:

a. Try to use other filter features from the pillow package Convert the adjust the brightness of your background .
