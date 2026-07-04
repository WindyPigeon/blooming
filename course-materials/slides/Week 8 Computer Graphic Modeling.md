CT029-3-2 Imaging and Special Effects
# Computer Graphic Modeling

## TOPIC LEARNING OUTCOMES

At the end of this topic, you should be able to:

- Explain various type of animations

- Choose the right particles to apply

- Enhance the image  / visual after rendering

## Contents & Structure

- Animation

- Particle System

- Post Processing

## Recap From Last Lesson

![Recap Clip Art Image - ClipSafari](Picture2.jpg)

1. What are the three type of lighting?

2. Explain how vertices, edges, and faces work in 3D modelling

<!-- Slide number: 5 -->
## Introduction

**What is Computer Graphic Modeling?**

- Process of creating a digital representation of objects, characters, or environments in a digital space using geometric shapes like lines, curves, and polygons in a computer system.

- Primarily works with Vector graphics.

- Tasks :

  - Designing, creating, and manipulating the model (2D / 3D)

    ***Manipulating points in virtual space (vertices) to form a mesh, which consists of vertices, edges, and faces*

## Object Modeling

Model:

- 2D models - height and width

- 3D models - depth and volume

- Application

  - Create objects or assets, often used in video games, animations, or graphic design.

  - Create characters, environments, and special effects

## Modeling Workflow

1. **Pre-Production**

   - Concept art, references, and design brainstorming.

2. **Production**

   - Main modeling process - create object.

3. **Post-Production**

   - Final touches, rendering, texturing, shading, animation and export.

4. **Final Output**

   - Deployment – game / illustration / asset etc

## Shape Creation

![2d shape geometric model word cards for kid Vector Image](Picture2.jpg)

- Every shape create is defined

  - Points and the lines (path) connecting them.

  - Combines multiple shapes into one.

  - Fill with color, gradient, or pattern inside a shape.

  - Define the Weight (thickness), Color, and Style (solid / dashed) of the outline around a shape.

![Geometric Low Poly Cat / 2D wall art by ...](Picture6.jpg)

## 2D Model Workflow

**Step 1: Pre-Production Stage**

- Conceptualization, planning, and preparation

- Task 1: Conceptualization

  - Start with a clear concept or idea (what to create - character, scene, object, or pattern).

  - Create initial sketches

- Task 2: Refining the Design

  - Turning a rough sketch (after approval) into a more defined line drawing.

**Step 2: Production Stage**

- Create and add visual detailed to the model.

- Task 1: Coloring

  - Colors the design (separating areas).

- Task 2: Shading and Highlights

  - Add lighting effect to show shadows and highlights (feel depth and dimension)

- Task 3: Detailing and Texturing

  - Add textures or patterns (surface) to enhance the model.

**Step 3: Post-Production Stage**

- Final touches – refine and preparing for export into desired format.

- Task 1: Final Touches and Adjustments

  - Final adjustments.

- Task 2: Exporting

  - Export to desired file format (e.g., .png, .svg, .jpg)

Step 4: Final Output

- Task : Integration into the Final Product

## How to improve the visual quality, realism, and aesthetic appeal of an object?

Which CG elements is important?

![Memory Recall Illustrations Stock ...](Picture2.jpg)

## Lighting

- Define the appearance of objects in a scene.

- Three types

  - Ambient Lighting

    - General light that illuminates all objects equally (no specific direction).

  - Directional Lighting

    - Light comes from a specific direction (like sunlight, and creates strong shadows)

  - Point Lighting

    - Light source emits light in all directions from a single point, like a light bulb.

![Unity - Manual: Lighting overview](Picture4.jpg)

![Lighting & Materials in 3D Design ...](Picture2.jpg)

## Contrast

- Difference in luminance or color that makes an object distinguishable.

- High contrast makes objects stand out

  - Have a wide range of tones, from deep shadows to bright highlights

- Low contrast can make them blend into the background.

  - Have a narrow range of tones.

- Application

  - Increasing contrast makes the dark areas darker and the light areas lighter

  - Decreasing contrast reduces the differences, making the image appear flat

## Composition

- Object composition is a technique used to build complex graphical scenes by combining simpler objects or elements.

- Organizing objects in a hierarchy, where each object can contain other objects. This helps manage the complexity and allows for better control over transformations

![ArtStation - Composition of geometric ...](Picture2.jpg)

## Animation

- Creates the illusion of movement by displaying a sequence of images ( AKA frame)

- Consists of multiple still images displayed at a certain speed.

- Frame rates

  - <=12 FPS : simple animations

  - 24 FPS : movie

  - 30 FPS : digital artefact / video games.

- Keyframes

  - Specific frames where significant changes

  - occur in the animation (start and end points )

![12 Basic Principles of Animation ...](Picture4.jpg)

## Animation Techniques

- Frame-by-Frame Animation

  - Each frame is drawn individually (similar to a flipbook)

- Tweening (Interpolation)

  - Software automatically generates intermediate frames between keyframes.

- Rigging and Skeletal Animation

  - Instead of redrawing frames, characters are structured with a skeletal system, and movements are applied to bones.

![Building A Basic Low Poly Character Rig In Blender | Envato Tuts+](Picture2.jpg)

![What Is Tweening Animations? - An ...](Picture4.jpg)

## Particle System

- Technique used in computer graphics to simulate

  - Fuzzy and dynamic phenomena.

- Example: Collection of small particles

  - fire, smoke, rain, snow etc.

![Particles-x - Blender Market](Picture6.jpg)

![Blender: Particle System – Simply ...](Picture2.jpg)

![Blender Test: Particle smoke simulation ...](Picture4.jpg)

![Vfx Particle System glow with material question : r/Unity3D](Picture10.jpg)

## Component of Particle Systems

- Emitters

  - Sources that generate particles.

  - Can be points, lines, shapes, or volumes

  - Control where and how particles are created.


- Particles

  - Elements that make up the effect.

  - Particle properties

    - Position, velocity, color, lifespan, and size.


- Forces

  - External influences affect the movement and behavior of particles.

  - Example: gravity, wind, and turbulence.

- Life Cycle

  - Particles are created, live for a certain duration, and then die.

  - Properties can change over their lifespan to create realistic effects.

## Particle System Simulating Fuzzy Phenomena

<ins>**Smoke Example**</ins>

- Emitters

  - Emit particles from a point or area, often from the same source as fire.

- Particles

  - Use semi-transparent particles with varying shades of gray. Increase the size and fade out the particles over time.

- Forces

  - Apply upward force and turbulence to simulate the swirling motion of smoke.

## Rendering

- Process of generating image from input data such as 3D models.

- Converting 3D models into 2D images or animations

- Type of Rendering

  - Real-Time Rendering

    - Generates images or animations instantaneously.

    - Application: video games and interactive applications..

  - Offline Rendering

    - Involves pre-rendering frames or images

    - Application : Films, visual effect and architectural visualizations.

## Post-Processing

- Techniques and methods used to enhance or modify images or animations after they have been rendered.

- Essential step in digital graphics, used in movies, video games, and animation to achieve visual effects that are difficult or time-consuming to create during the initial rendering phase.

- Rendering effects that are based on an existing rendered Scene

![](Picture6.jpg)

<!-- Slide number: 24 -->
## Importance of Post-Processing

1. Enhancing Visual Quality

   - Color correction, simulates the blurring effect on moving object, adds a soft glow

2. Correcting Imperfections

   - Sharpen the object detail, contrast between pixels, simulates the way light interacts with surfaces (shadow)

3. Adding Visual Effects

   - Screen Space Reflections (SSR), creates light spectrums around objects

4. Improving Overall Image Quality

   - Modifies the image’s contrast, brightness, saturation, and exposure, highlighting the center

## Review Question

Identify where in the workflow does these tasks belong to?

1. Brainstorm an idea.

2. Use Drawing Tools  - to create shape (geometry / stroke) and fill it up with color and texture

3. Adjust and refine the model (cleaning up lines, adjusting colors, and adding details)

4. Save or export model (PNG, SVG, JPEG).

![animation - How can I animate a 2D face rig on any 3D object? - Blender Stack Exchange](Picture2.jpg)

## What To Expect Next Week

**In Class**

- Image Processing

**Preparation for Class**

- Review various digital artefacts
