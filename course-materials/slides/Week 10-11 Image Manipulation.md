CT029-3-2 Imaging and Special Effects
# Image Manipulation

## TOPIC LEARNING OUTCOMES

At the end of this topic, you should be able to:

- Transform image

- Apply adjust image colour

- Explain the techniques used to manipulate image.

## Contents & Structure

- Digital Image Transformation

- Image Color Model and adjustment

- Image Manipulation Technique

## Recap From Last Lesson

![Recap Clip Art Image - ClipSafari](Picture2.jpg)

**What is digital image?**

A representation of a visual object,

- photograph

- graphic

Composed of pixels

## Format

- JPEG (Joint Photographic Experts Group)

- PNG (Portable Network Graphics)

- GIF (Graphics Interchange Format)

- BMP (Bitmap)

- TIFF (Tagged Image File Format)

## Image Dimension

- Refer to the width and height of an image - measured in pixels.

- Resolution is the total number of pixels in an image.

  - Affect the size and quality of the image

  - Resolution = width x height (e.g., 1920x1080).

- Aspect ratio is the proportional relationship between the width and height of an image.

  - Affect the image shape

  - Aspect ration = width to height (16:9, 4:3).

Image resizing (also called image scaling or resampling) is the process of changing the dimensions of a digital image by either increasing (upscaling) or decreasing (downscaling) its size

## Scaling Up (Upsampling)

- Increases the number of pixels in an image.

- Can lead to a loss of quality,

- Basic Example

  - Original image dimensions: 800x600 pixels

  - Scaling factor: 2 (double the size)

    - New width = 800 pixels * 2 = 1600 pixels

    - New height = 600 pixels * 2 = 1200 pixels

  - New image dimensions: 1600x1200 pixels

- Other Example : Nearest Neighbor

  Interpolation

- Original Image Dimensions: 4x4 pixels (grayscale)

```
[ 10, 20, 30, 40 ]
[ 50, 60, 70, 80 ]
[ 90, 100, 110, 120 ]
[ 130, 140, 150, 160 ]
```

- Scaling Factor: 2

- New Dimensions: 8x8 pixels

Steps

1. Create a new grid for the scaled image.

2. Map new pixel to the nearest pixel in the original grid

<ins>**New Dimension: 8X8**</ins>

```
[ 10, 10, 20, 20, 30, 30, 40, 40 ]
[ 10, 10, 20, 20, 30, 30, 40, 40 ]
[ 50, 50, 60, 60, 70, 70, 80, 80 ]
[ 50, 50, 60, 60, 70, 70, 80, 80 ]
[ 90, 90, 100, 100, 110, 110, 120, 120 ]
[ 90, 90, 100, 100, 110, 110, 120, 120 ]
[ 130, 130, 140, 140, 150, 150, 160, 160 ]
[ 130, 130, 140, 140, 150, 150, 160, 160 ]
```

## Scaling Down (Downsampling)

- Reduces the number of pixels in an image.

- Retains more quality than upsampling, but some detail may be lost.

- Basic Example

  - Original image dimensions: 1600x1200 pixels

  - Scaling factor: 0.5 (reduce by half)

    - New width = 1600 pixels * 0.5 = 800 pixels

    - New height = 1200 pixels * 0.5 = 600 pixels

    - New image dimensions: 800x600 pixels

- Other Example :Averaging

- Original Image Dimensions: 4x4 pixels (grayscale)

```
[ 10, 20, 30, 40 ]
[ 50, 60, 70, 80 ]
[ 90, 100, 110, 120 ]
[ 130, 140, 150, 160 ]
```

- Scaling Factor: 0.5 => New Dimensions: 2x2 pixels

- Steps

  1. Divide the original image into non-overlapping blocks

  2. Calculate the average value of the pixels in each block.

- First Block - Top-Left

  Pixels: [10, 20, 50, 60]

  Average: (10 + 20 + 50 + 60) / 4 = 35

- Second Block - Top-Right

  Pixels: [30, 40, 70, 80]

  Average: (30 + 40 + 70 + 80) / 4 = 55

- Third Block - Bottom-Left

  Pixels: [90, 100, 130, 140]

  Average: (90 + 100 + 130 + 140) / 4 = 115

- Fourth Block - Bottom-Right

  Pixels: [110, 120, 150, 160]

  Average: (110 + 120 + 150 + 160) / 4 = 135

<ins>**New Dimension: 2X2**</ins>

```
[ 35, 55 ]
[ 115, 135 ]
```

## Color Model

- Representing and manipulating colors in digital image

- How colors are created and represented in digital images

- Models

  - RGB (Red, Green, Blue)

  - CMYK (Cyan, Magenta, Yellow, Black)

  - HSL (Hue, Saturation, Lightness)

  - HSV (Hue, Saturation, Value)

![Color Theory Wheel Chart: CMYK, RGB, HSB, and Grayscale](Picture4.jpg)

![What is CMYK Color? | Plum Grove](Picture2.jpg)

## Color Channel

- Individual components of a color model that represent the intensity of specific primary colors in an image.

- Each channel corresponds to one of the primary colors in the color model being used.

- Example: RGB Color Model Channels

  - Red Channel - Represents the intensity of red light in the image.

  - Green Channel - Represents the intensity of green light in the image.

  - Blue Channel - Represents the intensity of blue light in the image.

  - Combination - Produce the full range of colors in the image.

## Color Channel – RGB Example

- RGB (255, 0, 0) – Red Color

  - Red Channel: 255

  - Green Channel: 0

  - Blue Channel: 0

![Understanding Channels in Photoshop - Part One](Picture2.jpg)

![original RGB histological image ...](Picture4.jpg)

![Thumbnail Image sample image with RGB values 255,0,0](Picture6.jpg)

## RGB to Grayscale Conversion

- Method: luminance formula

- Convert an RGB (Red, Green, Blue) color image to a grayscale image by calculating the perceived brightness of each pixel

- Based on Rec. 601 standard,

  - Grayscale= 0.299×R + 0.587×G + 0.114×B

    - Where, coefficient for the red channel is 0.299, contributes about 29.9% to the overall brightness

    - Conclusion : The eye is moderately sensitive to red light, most sensitive to green light and least sensitive to blue light.

- Use previous example Red Color : RGB(255,0,0)

- Grayscale = 0.299×255 + 0.587×0 + 0.114×0

- Grayscale =76.245

- Final grayscale value = 76

## Grayscale to RGB Conversion

- Assign the grayscale value to each RGB channel.

- Example:

  - Grayscale value: 76

  - RGB = (76, 76, 76)

## Gradient Map

1. Maps the grayscale values of an image to a gradient of colors.

2. Dark areas of the image are mapped to the colors at the left end of the gradient, while light areas are mapped to the colors at the right end.

3. Customizing the gradient color or blending and opacity of the gradient map layer

4. Special effect:

   - Duotone, tritone, and other multi-tone effects.

![Gradient Tool In Photoshop](Picture2.jpg)

![Blending Modes: A Complete Guide for ...](Picture4.jpg)

## Split Toning

- Applying different colors to the highlights and shadows of an image.

  - One color to the highlights (warm tone) and another color (blue tones) to the shadows.

- Enhance the mood and atmosphere of an image.

  - Adjust hue and saturation

![The Power of Split Toning in Lightroom : r/postprocessing](Picture4.jpg)

![From Split Toning to Color Grading ...](Picture2.jpg)

<!-- Slide number: 20 -->
## Image Blending

- Involves merging two images to produce a smooth transition between them.

- This technique is often used in panorama creation and HDR (High Dynamic Range) photography.

- Technique:

  - Use alpha channel to control the transparency of each image.

![How To Merge Layer Blend Modes In Photoshop](Picture2.jpg)

## Image Composition

- Placing and combining various elements within a frame.

- Use lines within the image to guide the viewer’s eye to the main subject.

![28 Composition Techniques That Will Improve Your Photos | PetaPixel](Picture2.jpg)

## Masking

- Use mask to selectively hide or reveal parts of an image.

- Masks can be created

  - Brushes,

  - Selections,

  - Gradients.

![Gradient mask blending in opencv python - Stack Overflow](Picture2.jpg)

![enter image description here](Picture2.jpg)

Type of Mask

- Layer Masks

  - Applied to specific layers to control their visibility. Black hides the content, white reveals it, and gray provides partial transparency.

- Clipping Masks

  - The content of one layer to mask another layer.

![Clipping Mask Illustrator](Picture4.jpg)

![enter image description here](Picture2.jpg)

![Clipping Mask Illustrator](Picture4.jpg)

## Noise

- Refers to random variations in pixel intensity.

- Types of Noise

  - Gaussian Noise

    - Adds random variations following a Gaussian distribution.

  - Salt and Pepper Noise

    - Randomly adds black and white pixels to an image.

![Image affected by Gaussian noise ...](Picture2.jpg)

![Salt and pepper noise and how to remove ...](Picture4.jpg)

## Blurring

- Reduces sharpness and detail in an image

  - Create a sense of motion

- Techniques

  1. Gaussian Blur

  2. Motion Blur

  3. Lens Blur

![Gaussian Blurring — A Gentle ...](Picture2.jpg)

**Motion Blur**

**Lens Blur**

![Input image](Picture2.jpg)

![Motion blur - OpenCV with Python By Example Book](Picture4.jpg)

![Result image](Picture8.jpg)

## Sharpening

- Enhances the edges and details in an image

  - Appear crisper and more defined.

- Techniques

  - Unsharp Mask

  - High Pass Filter

![Unsharp Mask filter in Motion – Apple Support (MY)](Picture4.jpg)

![](Picture6.jpg)

## Review Questions

1. Which color model is primarily used for digital screens and web graphics?
   A. CMYK   B. RGB    C. HSL       D. HSV

2. In the RGB color model, what are the primary colors?

   A. Red, Yellow, Blue

   B. Cyan, Magenta, Yellow

   C. Red, Green, Blue

   D. Red, Green, Yellow

## Summary / Recap of Main Points

- A digital image is a representation of a visual object, such as a photograph or graphic, in a format that can be processed by a computer.

- Resolution will affect the image detail and file size.
Scaling Up / down of image  and color conversion can lead to quality loss.

- Color channel – RGB

- Techniques used to manipulate image.
  - Colour conversion and adjustment
  - Image Blending , Composition, Blurring

## What To Expect Next Week

**In Class**

- Effect Application

**Preparation for Class**

- Manipulate images
