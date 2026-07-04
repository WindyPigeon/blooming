CT029-3-2 Imaging and Special Effects
# Introduction to Computer Graphic

## TOPIC LEARNING OUTCOMES

At the end of this topic, you should be able to:

- Explain the computer graphic pipeline .

- Identify elements of computer graphics

- Explain the Cartesian Coordinate System

## Contents & Structure

1. Introduction to Computer Graphic

2. Computer Graphic Pipeline

3. Element of Computer Graphic

## Recap From Last Lesson

![Recap Clip Art Image - ClipSafari](Picture2.jpg)

- Digital Images

  - 2D/ 3D matrix (pixel)

  - Pixel – intensity (0-255)

  - Grayscale / colour image

  - Resolution (width x height)


- Digital Artefact

  - Unintended or undesirable distortions, anomalies, or visual effects in images

## What is Computer Graphic?

Definition :

The creation of, manipulation of, analysis of, and interaction with pictorial representations of objects and data using computers.

By Dictionary of Computing

## Introduction to Computer Graphics

- Focus on creating visual content from scratch.

- Also involved creating, manipulating, and rendering visual content

- Includes designing and rendering 2D and 3D models, animations, and special effects from simple 2D images / models , geometric shape , polygon etc.

![Sprite 2D Computer Graphics Animation Tile-based Video Game 3D Computer Graphics, PNG, 600x500px, 2d Computer](Picture7.jpg)

![Wire-frame model 3D computer graphics ...](Picture3.jpg)

![Animation and Computer Graphics ...](Picture5.jpg)

## Introduction to Computer Graphic

- The entire process of creating computer generated imagery.

	From creating digital three-dimensional models,
		to the process of texturing, rendering, lighting etc.
	end with display on the screen.

Create visually appealing images, scenes, or animation

  - Ranging from simple 2D images to complex 3D simulations

<!-- Slide number: 8 -->
## Introduction to Computer Graphic

- Use algorithms and mathematical models to:

  - Generate images

  - Display images

  - Interact with images

![Wireframe and shaded models](Picture2.jpg)

## Computer Graphic Pipeline

- A framework within computer graphics that outlines the necessary procedures for transforming a three-dimensional (3D) scene into a two-dimensional (2D) representation on a screen

- Graphics pipeline can be divided into three main parts:

  - Application,

  - Geometry

  - Rasterization.

![](Picture6.jpg)

## Application

<ins>Preparation stages:</ins>

First stage is used to set the scene and defines the objects,

- Define and create models (2D/3D) and scenes

**Tasks:**

- Decide what objects to model in scene.

- Definition of lighting, camera, and other scene properties.

- Specification of materials and textures.

## Geometric

<ins>Shaping stages:</ins>

Second stage will transform and manipulate the models and scenes to specific and orientation in virtual world.

- Stage positions and shapes those objects on the scene

**Tasks:**

- Application of transformation matrices for translation, rotation, and scaling.

- Clipping to remove any parts of the scene outside the view.

- Calculate objects projection from camera view point

## Rasterization

<ins>Painting stages:</ins>

Third stage converts the geometric shape (such as triangles) into pixel data on a screen (store in framebuffer).

- converts objects into pixels for display.

**Tasks:**

- Rasterization the geometric shape into pixels.

- Fill the object with colors, texture and shading.

- Decide which pixels are visible and which are hidden

## Screen

<ins>Displaying stages:</ins>

Last stage sent image to a screen.

- Display the image.

**Tasks:**

- Combine pixels color, smooth the edges / lines.

- Adjust color – brightness / contrast and tone

- Send Image from framebuffer will be shown on the screen..

## Cartesian Coordinate System

- Can be a 2D or 3D coordinate system that specifies each point uniquely in a plane by a set of numerical coordinates.

- 2D: Shown as a pair of numbers (x, y)

  - X axis generally points from left to right,

  - Y axis generally points from bottom to top.

- 3D: Shown as a triplet of numbers (x, y, z)

  - X axis generally points from left to right,

  - Y axis generally points from bottom to top.

  - Z-axis points points from front to back

## Cartesian Coordinate System

- Origin, ‘O’ represent the point where these lines meet.

- Located at the center or upper-left corner of the screen.

- The coordinate plane

2D plane

3D plane

![Coordinates System in 3D Space Lesson | Uxcel](Picture2.jpg)

![](Picture2.jpg)

## Coordinate System - Direction

- X-axis (aka ‘XX’ line)

  - Represents horizontal movement.

  - Positive values are to the right, and negative values are to the left.

- Y-axis (aka ‘YY’ line)

  - Represents vertical movement.

  - Positive values are upward, and negative values are downward.

- Z-axis

  - Represents depth or movement into and out of the screen.

  - Positive values move away from the viewer, while negative values move toward the viewer.

## Colour Models

- Mixing three primary colours at different intensity levels produces a variety of colours.

- Origin represents **black** colour.

- Diagonally opposite to the origin represents **white** colours.

- Diagonal line connecting black and white represents all gray colors between black and white, which is also known as **gray** axis.

![](Picture2.jpg)

<!-- Slide number: 18 -->
## Core Element of Computer Graphic


- Rendering

  - Geometric transformation, visibility, simulation of light

- Interaction

  - Input/output devices, tools

- Modelling

  - Representation choices, geometric processing

- Animation

  - Lifelike characters, natural phenomena, their interactions, surrounding environments

## Rendering

![](Picture2.jpg)

- **Rendering or image synthesis** is the process of generating image from 2D or 3D model.

- Aims to produce the final image that can be displayed on a screen.

- Encompasses the **entire process of creating a 2D image from a 3D scene.**

- Includes the graphics pipeline stages (application, geometric, rasterization) as well as additional steps like shading, texturing, and frame buffer operations.

## Interaction

- Involves user input and manipulation of the graphical environment.

- Tasks

  - Handling mouse and keyboard input

  - Enable camera movement within a 3D scene,

  - Object responding to user actions in real-time.

## Modeling

- Creation and manipulation of 3D models.

- Includes defining shapes, structures, and properties of objects within a virtual environment.

- Involve both geometric and mathematical representations of objects.

![](Picture5.jpg)

## Animation

- Involves the depiction of motion and change over time.

- To create dynamic and moving scenes.

- Techniques:

  - keyframing,

  - skeletal animation,

  - morphing

## Application

- Applications of Computer Graphics & Uses

  - Printing

  - Training

  - Entertainment

  - Visualization

  - Machine Drawing

  - Graphical User Interface

  - Image Processing

  - Presentation

  - Computer Art

  - Education

![](Picture3.jpg)

## Example Application

![VFX software - visual effects | Adobe](Picture4.jpg)

![Computer Graphics : Human Animation Methodology 1 min read](Picture10.jpg)

![20 Un-ignorable Rules of Graphic Design -Part 1](Picture6.jpg)

![6 Most Popular Charts Used in Infographics - Edraw](Picture8.jpg)

![Matte Painting In Film, VFX & Animation: What It Is & How It Works](Picture2.jpg)

## Review Questions

1. What is the primary purpose of the Application Stage in the graphics pipeline?

2. What does the Z-axis represent in a three-dimensional Cartesian coordinate system?

3. Which element of computer graphics involves the depiction of motion and dynamic changes within a scene?

## Summary / Recap of Main Points

- Computer graphics pipeline is a series of stages through which graphics data is processed to create a visual representation on a computer screen.

- Computer graphics pipeline stages are Application, Geometric and Rasterization

- Elements of computer graphics are rendering, interaction, modelling and animation

- Cartesian coordinate system is intuitive and versatile.

## What To Expect Next Week

**In Class**

- Graphic Pipeline (operations)

**Preparation for Class**

- Works on coordinate system
