# Topic: Image Processing – Manipulate Image

**Package :**

* Numpy – dealing with matrix / array creation and calculation

* Opencv - dealing with image processing

* Matplot – plotting the matrix

**References:**

Open CV: [OpenCV: OpenCV modules](https://docs.opencv.org/4.x/index.html)

Numpy: [NumPy user guide — NumPy v2.1 Manual](https://numpy.org/doc/2.1/user/index.html)

Matplotlib: <https://matplotlib.org/stable/api/figure_api.html>

1. Create import the relevant library, if you have not done so, please install these packages.

```python
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plot
```

2. Download any color image and load it into the system

```python
# Load  image
image = cv.imread('lab\sceneImage.jpeg')
```

3. study the image dimension, size and resolution. We will resize the image as my downloaded image is too small. So I increase the image with scale factor 2.

```python
print("Original shape: ",image.shape)
print("Original Size: ", image.size)
h,w,d = image.shape
newimg = cv.resize(image, (w*2, h*2))
print("new shape: ",newimg.shape)
print("new Size: ", newimg.size)
```

4. Display the image using open cv. To prevent the program continue to load, use the waitkey function to pause the program to continue running, type any key to continue and close all the windows that are open.

```python
#display the image
cv.imshow('Original - New Image', image)
cv.imshow('New Image', newimg)
cv.waitKey(0)
cv.destroyAllWindows()
```

5. Convert the image to different colour.

```python
grayImg = cv.cvtColor(newimg, cv.COLOR_BGR2GRAY)
hsvImg = cv.cvtColor(newimg, cv.COLOR_BGR2HSV)
labImg = cv.cvtColor(newimg, cv.COLOR_BGR2LAB)
```

6. Instead of displaying the image in many window, do the stacking horizontally in a window using numpy package and display it in a single window. The dimensions must be the same

```python
combineImages = np.hstack((newimg, hsvImg, labImg))
cv.imshow('converted - new, hsv, lab Image', combineImages)
cv.waitKey(0)
cv.destroyAllWindows()
```

7. Now we deal with color channel, where we manipulate the image color. Split the channel to get the color for each layer.

```python
b, g, r = cv.split(newimg)
h, s, v = cv.split(hsvImg)
```

8. Now manipulate the image with 1 channel only.

```python
# channels
zeros = np.zeros_like(b)
rgbImg = cv.merge((r, g, b))
RedChannel = cv.merge((zeros, zeros, r)) #bgr
BlueChannel = cv.merge((b, zeros, zeros))
GreenChannel = cv.merge((zeros, g, zeros))
```

9. Adjust the image brightness and contrast

```python
#beta - brightness
#alpha - contrast
updatedImage1 = cv.convertScaleAbs(newimg, alpha=1, beta=0.5)
updatedImage2 = cv.convertScaleAbs(newimg, alpha=1.5, beta=1)
```

10. Display the images in multiple windows

```python
# Display the images
cv.imshow('new Image', newimg)
cv.imshow('Grayscale Image', grayImg)
cv.imshow('rbg Image', rgbImg)
cv.imshow('darker Image', updatedImage1)
cv.imshow('brighter Image', updatedImage2)
cv.waitKey(0)
cv.destroyAllWindows()
```

11. create a list where we can combine all the images (must be same dimensions)

```python
images = [image, grayImg, hsvImg,labImg, rgbImg, RedChannel, BlueChannel, GreenChannel]
titles = ['Original Image', 'Grayscale Image', 'HSV Image', 'LAB Image', 'RGB Image', 'Red Channel', 'Blue channel', 'green channel']
```

12. Now we will plot the images by looping through the list created in the q11. Use subplotting of 4 rows and 2 columns to display the image – gray / color.

```python
# Plot the images
plot.figure(figsize=(10, 8))
for i in range(len(images)):
    plot.subplot(4, 2, i+1)
    plot.imshow(images[i], cmap='gray' if len(images[i].shape) == 2 else None)
    plot.title(titles[i])
    plot.axis('off')

plot.tight_layout()
plot.show()
```

13. Run the program and following image will be displayed.

<ins>**Resize image**</ins>

![](data:image/png;base64...)

<ins>**Converted color image**</ins>

![A screenshot of a video game  Description automatically generated](data:image/png;base64...)

<ins>**Color manipulation**</ins>

**![Screenshots of a computer screen  Description automatically generated](data:image/png;base64...)**

<ins>**Matplot – color channels**</ins>

**![A screenshot of a video game  Description automatically generated](data:image/png;base64...)**

<ins>**Full coding**</ins>

```python
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plot

# Load  image
image = cv.imread('lab\sceneImage.jpeg')

#understnading image
print("Original shape: ",image.shape)
print("Original Size: ", image.size)
h,w,d = image.shape
newimg = cv.resize(image, (w*2, h*2))
print("new shape: ",newimg.shape)
print("new Size: ", newimg.size)

#display the image
cv.imshow('Original - New Image', image)
cv.imshow('New Image', newimg)

cv.waitKey(0)
cv.destroyAllWindows()

# Convert to different color spaces
grayImg = cv.cvtColor(newimg, cv.COLOR_BGR2GRAY)
hsvImg = cv.cvtColor(newimg, cv.COLOR_BGR2HSV)
labImg = cv.cvtColor(newimg, cv.COLOR_BGR2LAB)

combineImages = np.hstack((newimg, hsvImg, labImg))
cv.imshow('converted - new, hsv, lab Image', combineImages)
cv.waitKey(0)
cv.destroyAllWindows()

b, g, r = cv.split(newimg)
h, s, v = cv.split(hsvImg)

# channels
zeros = np.zeros_like(b)
rgbImg = cv.merge((r, g, b))
RedChannel = cv.merge((zeros, zeros, r)) #bgr
BlueChannel = cv.merge((b, zeros, zeros))
GreenChannel = cv.merge((zeros, g, zeros))

#beta - brigthness
#alpha - contrast
updatedImage1 = cv.convertScaleAbs(newimg, alpha=1, beta=0.5)
updatedImage2 = cv.convertScaleAbs(newimg, alpha=1.5, beta=1)

# Display the images
cv.imshow('new Image', newimg)
cv.imshow('Grayscale Image', grayImg)
cv.imshow('rbg Image', rgbImg)
cv.imshow('darker Image', updatedImage1)
cv.imshow('brighter Image', updatedImage2)

cv.waitKey(0)
cv.destroyAllWindows()

images = [image, grayImg, hsvImg,labImg, rgbImg, RedChannel, BlueChannel, GreenChannel]
titles = ['Original Image', 'Grayscale Image', 'HSV Image', 'LAB Image', 'RGB Image', 'Red Channel', 'Blue channel', 'green channel']
# Plot the images
plot.figure(figsize=(10, 8))
for i in range(len(images)):
    plot.subplot(4, 2, i+1)
    plot.imshow(images[i], cmap='gray' if len(images[i].shape) == 2 else None)
    plot.title(titles[i])
    plot.axis('off')

plot.tight_layout()
plot.show()
```

**Task:**

a. Download the background scene for your group assignment and change adjust the colour – red channel / blue channel / green channel.

b. Convert the adjust the brightness of your background .

c. Integrate one of the image (outcomes from the opencv library – example redchannel image) as the scene (background) for your pygame display.
