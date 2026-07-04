CT029-3-2 Imaging and Special Effects
# Computer Graphic Manipulation

## TOPIC LEARNING OUTCOMES

At the end of this topic, you should be able to:

- Calculate and explain the concept of interpolation.

- Explain the use of texture and normal mapping

## Contents & Structure

- Interpolation Overview

- Type of Interpolation

## Recap From Last Lesson

![Recap Clip Art Image - ClipSafari](Picture2.jpg)

1. What is the identity matrix for scaling?

2. Following figure is an example of ____ transformation.

![](Picture5.jpg)

<!-- Slide number: 5 -->
## Interpolation

- A fundamental technique used to estimate or generate intermediate values or data points between data points.

- Purpose:

  - Filling in the Gaps.

  - Creating Smoothness

  - Generating Detail

  - Resizing and Transformation

![](Picture7.jpg)

## Types of Interpolation

- Types of Interpolation

  - Nearest Neighbor Interpolation – most common method

  - Linear Interpolation - Estimates values along a straight line between two known points

  - Bilinear Interpolation - For 2D data (like images)

  - Bicubic Interpolation - Uses the 16 nearest neighbors (in a 2D grid)

  - Spline Interpolation - Uses mathematical splines (like cubic splines)

## Nearest Neighbor Interpolation

- The simplest form of interpolation

- Assigns (choose) the value of the nearest known data point(neighbour pixel value) to the interpolated point.

- No blending or averaging — only replication of the closest known value.

- Output pixel takes the color value of the closest pixel in the input image.

- Weakness:

  - Blocky Appearance

  - No Smoothing

![Nearest Neighbor Interpolation. Easy ...](Picture3.jpg)

## Nearest Neighbor Interpolation

<ins>**Example (2X2 image to 4X4 image)**</ins>

1. calculate Scaling factor
	xScale = originalWidth / newWidth =>2/4 = 0.5
	yScale = originalHeight / newHeight => 2/4 = 0.5
2. Calculate the pixel value for each 4X4 pixel
	(row) origX = round(i * xScale)
	(col) origY = round(j * yScale)

 Updated index	row		col   		orig Pixel val of existing index
 pixel (0,0)  row1 = (0X0.5) ; col1 = (0X0.5) => take the value of (0,0) => A
 pixel (1,0)  row2 = (1X0.5) ; col1 = (0X0.5) => take the value of (0,0) => A
 pixel (2,0)  row3 = (2X0.5) ; col1 = (0X0.5) => take the value of (1,0) => C
 pixel (3,0)  row4 = (3X0.5) ; col1 = (0X0.5) => take the value of (1,0) => C

![Nearest Neighbor Interpolation. Easy ...](Picture3.jpg)

 Updated index	row		col   		orig Pixel val of existing index
 pixel (0,1)  row1 = (0X0.5) ; col2 = (1X0.5) => take the value of (0,0) => A
 pixel (1,1)  row2 = (1X0.5) ; col2 = (1X0.5) => take the value of (0,0) => A
 pixel (2,1)  row3 = (2X0.5) ; col2 = (1X0.5) => take the value of (1,0) => C
 pixel (3,1)  row4 = (3X0.5) ; col2 = (1X0.5) => take the value of (1,0) => C
 pixel (0,2)  row1 = (0X0.5) ; col3 = (2X0.5) => take the value of (0,1) => B
 pixel (1,2)  row2 = (1X0.5) ; col3 = (2X0.5) => take the value of (0,1) => B
 pixel (2,2)  row3 = (2X0.5) ; col3 = (2X0.5) => take the value of (1,1) => D
 pixel (3,2)  row4 = (3X0.5) ; col3 = (2X0.5) => take the value of (1,1) => D
 pixel (0,3)  row1 = (0X0.5) ; col4 = (3X0.5) => take the value of (0,1) => B
 pixel (1,3)  row2 = (1X0.5) ; col4 = (3X0.5) => take the value of (0,1) => B
 pixel (2,3)  row3 = (2X0.5) ; col4 = (3X0.5) => take the value of (1,1) => D
 pixel (3,3)  row4 = (3X0.5) ; col4 = (3X0.5) => take the value of (1,1) => D

## Linear Interpolation

- Estimate the unknown point value by assuming a linear relationship between two known data points using weighted average.

- Draws a straight line between the two known points and finds the value on that line at the desired location.

- Weakness

  - blurry or blocky artifacts

![Linear Interpolation Formula: Definition, Formula, Solved Examples](Picture2.jpg)

## Linear Interpolation

- Formula

	y = y₁ + (((x - x₁) * (y₂ - y₁)) / (x₂ - x₁))

	where,

(x, y) is the point to be interpolated.

(x₁, y₁) and (x₂, y₂) are the two known data points.


  - Given the matrix [[10,20], [30,40]]

    - Programming perspective: X1 = 0, X2 = 1 and y1 = 0, y2=1

    - Mathematics perspective: X1 = 1, X2 = 2 and y1 = 1, y2=2

| 10 | 20 |
| --- | --- |
| 30 | 40 |


- Formula for interpolated result

	y = y₁ + (((x - x₁) * (y₂ - y₁)) / (x₂ - x₁))

	where,

y₁, y₂: y values at points x₁ and x₂

x₁, x₂: x coordinates

x: x coordinate to find y result

<ins>Find interpolation point value at index = 1.5 between 10 and 20</ins>

**Interpolation point at (1, 1.5)**

y1 = 10 (starting value) , y2 = 20 (ending value)

Y   = 10+((1.5−1)*(20−10)/(2−1))

     = 10 +(0.5*10 /1)

     = 10 + 5

     = 15

| 10 | 20 |
| --- | --- |
| 30 | 40 |

| 10 | 20 |
| --- | --- |
| 30 | 40 |

| 10 | 15 | 20 |
| --- | --- | --- |
| 30 |  | 40 |

**Value for Interpolation point at (2, 1.5)  second row**

y1 = 30 (starting value) , y2 = 40 (ending value)
Y   = 30+((1.5−1)*(40−30)/(2−1))
     = 30 +(0.5*10 /1)
     = 30 + 5
     = 35

| 10 | 20 |
| --- | --- |
| 30 | 40 |

| 10 | 15 | 20 |
| --- | --- | --- |
| 30 | 35 | 40 |

## Bilinear Interpolation

- A resampling method that scales or manipulates images and grids.

- Estimate a new pixel value within a two-dimensional array using the four nearest pixel values (neighboring points), which are directly adjacent both vertically and horizontally.

- Calculates the new value by performing linear interpolation first in one direction and then in the other.

- For image resizing, rotation, and texture mapping

- Formula (simplest form):

 	P(x,y)=Q11⋅(1−x)⋅(1−y)+Q12⋅x⋅(1−y)+Q21⋅(1−x)⋅y+Q22⋅x⋅y

Where:

Q₁₁, Q₁₂, Q₂₁, Q₂₂: The four corner values of your 2×2 grid

x, y: Normalized coordinates (0 ≤ x ≤ 1, 0 ≤ y ≤ 1)


- Convert point (1.5, 1.5) coordinate in 2X2 matrix with bounds [1,2] × [1,2]

  - Normalized coordinates = (actual coord –  min coord) / (max coord – min coordinate)

x = (1.5 - 1) / (2 - 1) = 0.5

y = (1.5 - 1) / (2 - 1) = 0.5

- Apply: P(x,y)=Q11⋅(1−x)⋅(1−y)+Q12⋅x⋅(1−y)+Q21⋅(1−x)⋅y+Q22⋅x⋅y

  - Normalized coordinates : x = 0.5, y = 0.5

  - Q11 = 10,  Q12 = 20, Q21 = 30, Q22 = 40

P(0.5,0.5) 	= 10⋅(1−0.5)⋅(1−0.5) + 20⋅0.5⋅(1−0.5) + 30⋅(1−0.5)⋅0.5 + 40⋅0.5⋅0.5
 		= (10⋅0.25) + (20⋅0.25) + (30⋅0.25) + (40⋅0.25)
		= 2.5+5+7.5+10
		= 25

| 10 | 20 |
| --- | --- |
| 30 | 40 |

| 10 |  | 20 |
| --- | --- | --- |
|  | 25 |  |
| 30 |  | 40 |

## Bilinear Interpolation Example

**Alternative method**

**Step 1: Determine the Rectangle and Corner Pixel Values**

- Input coordinates (x, y) for (2, 2)  = 50

- Output image are (1/2, 1/2) = (1, 2)

- Four corner pixels in the original image surround coordinate (1.5, 1.5)

	Q1 (Q11) : 10 (top left)

	Q2 (Q12): 20 (top right)

	Q3 (Q21): 40 (bottom left)

	Q4 (Q22): 50 (bottom right)

| 10 | 20 | 30 |
| --- | --- | --- |
| 40 | 50 | 60 |
| 70 | 80 | 90 |

**Step 2: Calculate the Relative Distances**

- Horizontal and vertical distances of the fractional input coordinate (1.5, 1.5) from the top-left corner (1, 1) of the rectangle.

  - Horizontal distance (dx):	 x - x0 = 1.5 - 1
	 	= 0.5

  - Vertical distance (dy): 		y - y0 	=1.5 - 1
		= 0.5

| 10 | 20 | 30 |
| --- | --- | --- |
| 40 | 50 | 60 |
| 70 | 80 | 90 |

**Step 3: Calculate the Intermediate Values**

- R1 Interpolation at the top row (horizontal position)

- R1 = Q1 * (1 - dx) + Q2* dx

- R1 Interpolation at the bottom row(horizontal position)

- R2 = Q3 * (1 - dx) + Q4 * dx

  Need to use values from previous steps:

  Step 1: Q1 : 10, Q2 : 20, Q3 : 40, Q4 : 50

  Step 2: dx = 0.5, dy = 0
 	R1 	= 10 * 0.5 + 20 * 0.5
		= 5+10 => 15
	R2 	= 40 *0.5 + 50 * 0.5
		= 20+25 => 45

**Step 4: Calculate the Interpolate in the y-direction**

- P(x,y) = R1 ​⋅ (1−dy) + R2​ ⋅ dy

Need to use values from previous steps:

Step 1: Q1 : 10, Q2 : 20, Q3 : 40, Q4 : 50

Step 2: dx = 0.5, dy = 0.5

Step 3: R1 = 15,  R2 = 45

P(1.5,1.5) = 15 * (1-0.5) + 45* 0.5
	 	= 7.5+22.5
		= 30

| 10 |  | 20 | 30 |
| --- | --- | --- | --- |
|  | 30 |  |  |
| 40 |  | 50 | 60 |
| 70 |  | 80 | 90 |

## Bicubic interpolation

- Use 16 neighboring points to determine the value at an intermediate location.

- Yields smoother and more visually appealing results.

- Uses cubic polynomials in two dimensions

![Bicubic interpolation. | Download Scientific Diagram](Picture3.jpg)


- Formula

  where,

  - Qij : values at 16 neighboring grid points

  - w(i,j) : Weight coefficients based on distances in the horizontal (xx) and
	vertical (yy) directions, derived from cubic functions.	w(i,j)=f(∣x−xi∣)⋅f(∣y−yj∣)

![](Picture7.jpg)

## Spline interpolation

- Construct smooth curves through a set of data points.

- Uses piecewise polynomial functions (splines) to achieve a smooth and continuous interpolation.

- Produces a fluid curve that smoothly transitions between points.

![A diagram of a graph Description automatically generated](Picture2.jpg)


- Formula:

  where:

  - $a_i$, $b_i$, $c_i, $d_i$ :  coefficients determined using boundary conditions and continuity equations

  - $X_i$ and $x_{i+1}$ : consecutive data points.

![](Picture4.jpg)

## Application

- **Texture Mapping**

  - Interpolation determines how textures are applied to 3D models.

- **Normal Mapping**

  - Smoothly interpolates surface normals to simulate fine details on low-polygon models.

- **Image Scaling**

  - Bicubic or bilinear interpolation is used to resize images while preserving quality.

## Texture Mapping

- Process of applying a 2D image (texture) onto the surface of a 3D model to give it detail, color, and realism.

- Allow 3D object to look more realistic without adding more geometric complexity to the model.

- Example:

  - Adding wood grain, metal, or fabric patterns to objects like furniture or clothing.

  - Applying visual details like decals, logos, or surface imperfections.

## Texture mapping Application

![](Picture3.jpg)
*Map a texture(image) onto a geometry shape.

## Normal Mapping

- Create illusory surface details to enhance the realism of digital objects without increasing geometric complexity

- A texture where each pixel encodes a direction (a normal vector) using RGB values (how the surface should interact with light)

- Manipulate the surface normals used in lighting calculations, creating the appearance of intricate details like cracks, wrinkles, or rivets.

- Normal vectors are geometric entities, textures used for color information → storing normal vectors in a texture not obvious

- Modifies the way light interacts with a surface by altering its normal vectors. 

  Determine how light reflects or refracts off surfaces.

- Normal maps are just texture images where each pixel stores the object's surface normal vector in the form of RGB colours.

  - Red channel contains the value of the X axis,

  - Green channel contains the value of the Y axis

  - Blue channel contains the value of the Z axis.

![](Picture4.jpg)

## Comparison
| Feature | Texture Mapping | Normal Mapping |
| --- | --- | --- |
| Purpose | Adds visual details (color/pattern) | Simulates surface features (bumps, dents) |
| Output Type | 2D image applied to 3D models | Altered surface normals for lighting |
| Complexity | Basic | More advanced |
| Computational Cost | Low | Moderate |

## Review Questions

1. Given the 4x4 matrix below, perform bilinear interpolation to find the value at the point (1.5, 2.5).

Answer 3 or 4 or 5 ?

2. Do you think you can find the value for interpolation point at (1.6,2)?

![](Picture3.jpg)

## Summary / Recap of Main Points

- Interpolation is the process of estimating unknown values that fall between known data points.

- Plays a critical role in various fields, including computer graphics to  enabling smooth transitions and accurate predictions.

- Mapping techniques like texture mapping and normal mapping add intricate details to 3D models, making them visually realistic.

## What To Expect Next Week

**In Class**

- Modeling

**Preparation for Class**

- Review various digital artefacts
