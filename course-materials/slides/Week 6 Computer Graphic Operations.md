CT029-3-2 Imaging and Special Effects
# Computer Graphic Operations

## TOPIC LEARNING OUTCOMES

At the end of this topic, you should be able to:

- Implements computer graphic technique in digital artefact

- Create and manipulate shape using matrix.

## Contents & Structure
Type of Graphics
Vector
Operations

<!-- Slide number: 4 -->
## Recap From Last Lesson

![Recap Clip Art Image - ClipSafari](Picture2.jpg)
What are the Computer Graphic Pipeline?

<!-- Slide number: 5 -->
## Graphics Representation – Two Methods
Raster (Bitmap) Graphics
Image is presented as a rectangular grid of colored squares.
Stored as the collection of small individual dots called pixels.
Called bitmap images.
Vector Graphics
Represented in - continuous geometric objects
Not based on pixel pattern.
Use Points to draw line.

![](Picture7.jpg)

<!-- Slide number: 6 -->
## Comparison
| Raster Graphics | Vector Graphics |
| --- | --- |
| Raster images are the collection of the pixel. | The Vector images are composed of paths |
| Scan conversion is required. | Scan Conversion is not required |
| Less costly | More costly compared to raster graphics |
| Use less space to store | Use more space. |
| Can draw mathematical curves, polygons, and boundaries. | Can only draw continuous and smooth lines |
| File Extension: .BMP, .TIF, .JPG etc. | File Extension: .SVG, .PDF, .AI etc. |

## Vector

![Geometric Figure PNG Transparent, Point ...](Picture2.jpg)

- Used to represent points, directions, and velocities (include transformations).

  - Geometric shapes such as points, lines, curves, and polygons

- Position - (x, y, z) can denote the coordinates of a point.

- Movement  - indicate direction and magnitude.

- Transformations -  translation, rotation, and scaling.

- Lighting -  light interacts with surfaces, affecting shading and reflections.

![Vectors (Geometry, Transformations ...](Picture4.jpg)

## Straight line

- A line contains two points.

- Point is an important element of a line

- Equation

  Y = mx + a

  where,

  - (x, y) = axis of the line.

  - m = Slope of the line.

  - a = Interception point

![](Picture7.jpg)

<!-- Slide number: 9 -->
## Straight line - Example

- Example - P(2, 3) and Q(6, 7)

- Equation: y = mx + a (recall high school y = mx + c)

  - Use P(2, 3) to find a,

## Movement

- A vector represents movement by defining both **direction** and magnitude.

  - Arrow pointing from one point (location) to another
  
  - **Direction** of the movement between 2 points
  
  - **Magnitude** (or length) is the distance between two points

## Movement - Example

- Point P(2, 3) move to Point Q(6, 7)

  - Direction of the movement PQ

    $$
    $$

  - Magnitude between P and Q

    $$
    $$

## Transformations

- Changing some graphics into something else by applying rules.

- Play an important role in computer graphics to reposition the graphics on the screen and change their size or orientation.

- Type

  - Translation,

  - Scaling up or down,

  - Rotation

- Point represented with 3 numbers (Homogenous Coordinate system).

  - Cartesian point PX,YX,Y can be converted to homogenous coordinates by P’ (Xh, Yh, h).

## Translation

- Moving an object from one position to another in 3D space.

- Adds a translation vector to the object's coordinates.

  - Shifting a set of points or objects by a specific distance along one or more axes

  - The translation pair (Tx,Ty) AKA shift vector, often denoted as T

- In 2D,

  T = [Tx, Ty],

  where

  Tx is the horizontal shift

  Ty is the vertical shift.

- In 3D,

  T = [Tx, Ty, Tz],

  Tz representing the depth shift.

## Translation

- Let P is a point with coordinates (x, y). It will be translated as (x1 y1).

- Translation Matrix

$$
\begin{pmatrix} 1 & 0 & t_x \\ 0 & 1 & t_y \\ 0 & 0 & 1 \end{pmatrix}
$$

![](Picture4.jpg)

## Translation Example

- A rectangular geometric shape with following points:

  - A (1, 4)

  - B (1, 1)

  - C (3, 1)

  - D (3, 4)

- Translation Matrix for Tx = 3 (rightward shift) and Ty = 2 (upward shift)

$$
\begin{pmatrix} 1 & 0 & 3 \\ 0 & 1 & 2 \\ 0 & 0 & 1 \end{pmatrix}
$$

- Calculation

For point A: $\begin{pmatrix} 1 & 0 & 3 \\ 0 & 1 & 2 \\ 0 & 0 & 1 \end{pmatrix} * \begin{pmatrix} 1 \\ 4 \\ 1 \end{pmatrix}$

Result

$$
\begin{pmatrix} (1 \times 1) + (0 \times 4) + (3 \times 1) \\ (0 \times 1) + (1 \times 4) + (2 \times 1) \\ (0 \times 1) + (0 \times 4) + (1 \times 1) \end{pmatrix} = $\begin{pmatrix} 4 \\ 6 \\ 1 \end{pmatrix}
$$

- New coordinates for point A: (4, 6)

## Scaling

- Process of expanding or compressing the dimensions of an object (changing the size of an object).

- Size of an object can be change by multiplying the points of an object by scaling factor

  - SF (scale factor) > 1 then the object is enlarged

  - SF (scale factor) < 1 then the object is compressed

  - SF (scale factor) = 1 then the object is unchanged

- Scaling matrix.

![The Similar Polygons Area Theorem - Andrea Minini](Picture2.jpg)

<ins>Scaling factor</ins>

Sx: x-axis

Sy: y-axis


- Two types of Scaling

  - Uniform Scaling  - Sx = Sy

  - Non-Uniform Scaling - Sx ≠ Sy

Condition

- Sx > 1, object is scaled larger (x-direction).

- Sx < 1, object is scaled smaller (x-direction).

- Sy > 1, object is scaled larger (y-direction).

- Sy < 1, object is scaled smaller (y-direction).

![A diagram of a graph Description automatically generated with medium confidence](Picture7.jpg)

## Scaling Example

- Use the rectangular geometric shape from previous example:

  - A(1, 4), B(1, 1), C(3, 1), D(3, 4)

- Scale the shape by scaling factor of 2 (both x and y directions). => Uniform Scaling

- Scaling matrix.

#### Notes:

## Rotation

- Rotate the object at particular angle θ from its origin.

- In the image:

  - The point G(X,YX,Y) is located at angle φ from the horizontal X coordinate with distance r from the origin.

  - Rotate it at the angle θ.

  - New location, point G’ (X′,Y′X′,Y′)

  - Rotation angle, θ is anti-clockwise direction.

![](Picture9.jpg)

## Rotation

- Transforming an object around a fixed point, origin.

- Rotate objects around the z-axis.

- 2D rotation matrix formula (anti Clockwise)

$$
\begin{bmatrix} x' \\ y' \end{bmatrix} = \begin{bmatrix} cos \theta & -sin \theta \\ sin \theta & cos \theta \end{bmatrix} \begin{bmatrix} x \\ y \end{bmatrix}
$$

x' = xcosθ - ysinθ.

y' = xsinθ + ycosθ.


## Rotation Example

- Reuse the rectangular geometric shape from previous example:

  - A (1, 4), B (1, 1), C (3, 1), D (3, 4)

- Rotate: 90 degree, anti-clockwise around **origin (0, 0)**

  - cos⁡90° = 0 

  - sin⁡90° = 1

$$
R(90) = \begin{pmatrix} 0 & -1 \\ 1 & 0 \end{pmatrix}
$$

$$
\begin{pmatrix} X' \\ Y' \end{pmatrix} &= \begin{pmatrix} 0 & -1 \\ 1 & 0 \end{pmatrix} \begin{pmatrix} 1 \\ 4 \end{pmatrix}
                                       &= \begin{pmatrix} 0.1 + (-1) \cdot 4 \\ 1.1 + 0.4 \end{pmatrix}
                                       &= \begin{pmatrix} -4 \\ 1 \end{pmatrix}
                                       &= A (-4, 1)
$$

## Rotation

A(1,4)becomes A′(−4,1)

B(1,1)becomes B′(−1,1)

C(3,1) becomes C′(−1,3)

D(3,4) becomes D′(−4,3)

## Shearing

- A shear transformation has the effect of slanting the shape.

- A transformation that skews the coordinate space - add a multiple of one coordinate to the other.

- Formula

- Horizontal shear $\begin{pmatrix} 1 & k \\ 0 & 1 \end{pmatrix}$

  - Where k is the shear factor

- Vertical shear $\begin{pmatrix} 1 & 0 \\ k & 1 \end{pmatrix}$

![](Picture4.jpg)

<!-- Slide number: 24 -->
## Shearing - Example

- Shearing factor positive (to right) : 2

- $$
  Formula &= \begin{pmatrix} 1 & 2 \\ 0 & 1 \end{pmatrix} \begin{pmatrix} 1 \\ 4 \end{pmatrix}
          &= \begin{pmatrix} 1.1 + 2.4 \\ 0.1 + 1.4 \end{pmatrix}
          &= \begin{pmatrix} 9 \\ 4 \end{pmatrix}
          &= A (9, 4)
  $$

Outcomes

- A'(9, 4)

- B’(1, 1)	remains unchanged

- C’(3, 1)

- D'(11, 4)

<!-- Slide number: 25 -->
## Mirroring

- Mirroring a shape across the line of symmetry.

- Reversed orientation / flip it across its line of symmetry

- Use matrix multiplication

  - To flip over the x-axis, multiply by $\begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix}$

  - To flip over the y-axis, multiply by $\begin{pmatrix} -1 & 0 \\ 0 & 1 \end{pmatrix}$

  - To flip over the line y=x, multiply by $\begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}$

![](Picture7.jpg)

<!-- Slide number: 26 -->
## Mirroring - Example

- Relection on x-axis

- Use matrix multiplication $\begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix}$

- Vertex A = $\begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix} \begin{pmatrix} 1 \\ 4 \end{pmatrix}$

  $$
  A' &= \begin{pmatrix} 1.1 + 0.4 \\ 0.1 & -1.4 \end{pmatrix}
     &= \begin{pmatrix} 1 \\ -4 \end{pmatrix}
  $$

Outcomes

- B'(1, -1)

- C'(3, -1)

- D'(3, -4)

## Review Questions

Q1: Which of the following matrices represents a 90-degree clockwise rotation about the origin in 2D space?

A $\begin{pmatrix} 0 & 1 \\ -1 & 0 \end{pmatrix}$

B $\begin{pmatrix} 0 & -1 \\ 1 & 0 \end{pmatrix}$

C $\begin{pmatrix} -1 & 0 \\ 0 & -1 \end{pmatrix}$

D $\begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix}$

Q2: Given line defined by the equation y = 2x + 1. Find the coordinates of the point that is 3 units to the right of the point (2, 5).

A. (5,11)

B.(5,3)

C. (6,3)

D. (6,5)

## Review Questions - Solution

Q1: Which of the following matrices represents a 90-degree clockwise rotation about the origin in 2D space?

**A $\begin{pmatrix} 0 & 1 \\ -1 & 0 \end{pmatrix}$**

B $\begin{pmatrix} 0 & -1 \\ 1 & 0 \end{pmatrix}$

C $\begin{pmatrix} -1 & 0 \\ 0 & -1 \end{pmatrix}$

D $\begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix}$

Q2: Given line defined by the equation y = 2x + 1. Find the coordinates of the point that is 3 units to the right of the point (2, 5).

**A. (5,11)**
B. (5,3)
C. (6,3)
D. (6,5)

<!-- Slide number: 29 -->
## Summary / Recap of Main Points

- Graphic Representation – Raster & Vector

- Process – Movement and Transformation

- Translation

- To translate a point, add the translation vector to its coordinates.

- Rotation

  - The rotation matrix is used to rotate points around the origin.

- Reflection

  - The reflection matrix flips points across a specific axis.

- Scaling

  - The scaling matrix scales points by a certain factor in each direction.

## What To Expect Next Week

**In Class**

- Computer Graphic Manipulation

**Preparation for Class**

- Matrices Calculation
