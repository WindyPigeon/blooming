CT029-3-2 Imaging and Special Effects
# Digital Artefact

## TOPIC LEARNING OUTCOMES

At the end of this topic, you should be able to:

1. Explain the term “digital artefact”

2. Provide examples of digital artefact

3. Setup scene and sprite

## Contents & Structure

- Overview

- Why is it important

- Advantages

- Issues

## Recap From Last Lesson

- Why do you need to implement special / visual effect?

- Provide 2 example of visual effect and where it can be applied?

- Picture on the right, is it a special effect or visual effect?

![Inside the Visual Effects of Avatar: The Way of Water: “Water Is Both a Blessing and a Curse” | Vanity Fair](Picture2.jpg)

## Image

- Visual representation of an object, scene, or concept.

- Created through various mediums:

  - Photography, painting, or digital technology.

- Form: analog or digital.

  - Painting, photography, drawing, computer graphic and other artistic or physical means.

![Image of Mona Lisa painting by Leonardo da Vinci](Picture2.jpg)

![Image of painting](Picture6.jpg)

![Image of computergenerated 3D model](Picture4.jpg)

<!-- Slide number: 6 -->
## Digital Image

- Specific type of image represented as discrete data

- Characteristics

  - Composed of pixels (grid of individual elements) in 2D – **entire image**

    - Tiny squares of color (Discrete representations of light intensity)

  - Finite resolution e.g. 1200 X 1000 pixels (w x h)

  - Maintain consistent quality (no degraded over the time)

  - Highly manipulable

  - Various format : png, jpeg etc.

![Understanding Digital Images for Image Processing and Computer Vision (Part 1): | by Md. Jewel | Medium](Picture4.jpg)

<!-- Slide number: 7 -->
## Digital Image

- Images can be represented by an array with an entry for each pixel.

- Represented as matrices where each element corresponds to a pixel's intensity or color value.

- 2D matrix grayscale images

  - A single-channel (grayscale)

  - Pixel intensities of shape (row, column) => brightness

- 3D for color images

  - Matrix with dimensions for height, width, and color channels.

  - Each dimension contains the color plane (red, green and blue).

![2: A three-dimensional RGB matrix. Each layer of the matrix ...](Picture2.jpg)

## Two Dimension Image

- Grayscale Images to represent scene or objects

- The smallest unit is a pixel. Each pixel carries only intensity information.

- Each element corresponds to a pixel's intensity, ranging from 0 (black) to 255 (white) in 8-bits image

- Image is composed of shades of gray, varying from black at the weakest intensity to white at the strongest.

- Resolution refers to the number of pixels in an image, usually given as width x height (e.g., 1920x1080).

![a) Grayscale image of character 'A' (b) Binary representation of... | Download Scientific Diagram](Picture2.jpg)

## Digital Video

- Electronic representation of audio/visual content in the form of encoded binary data (zeros and ones).

- A moving visual media

  - Encoding images into digital signals and display as a sequence of frames. (series of digital images)

![A video is a sequence of images called ...](Picture2.jpg)

## Digital Video

- Streams are made up of individual frames, each representing a time slice of the scene.


- Smooth running of the video.

  - Number of frames per second (fps)

![frames from a video into a matrix ...](Picture2.jpg)

## Sound

- A type of energy made by vibrations.

- Essential element (Audio) of any film or video project to enhance the movie experience.

- Video / Movie

  - Dialogue,

  - Sound effects - Ambient noise / background noise

  - Music/ soundtracks

![What is Sound? | Soundproofing Company](Picture2.jpg)

## Digital Artefact Overview

Any item that is created and exists in a digital format. 

->

Include

Documents, 

Images, 

Audio files, 

Videos, 

Software, and more. 

## Application

- Documents

  - Slides, words, spreadsheet.

- Images

  - Photographs, artwork, graphics.

- Audio Files

  - Music tracks, podcasts, sound effects.

- Videos

  - Movies, animations, video clips.

- Software

  - Applications, games, scripts.

- Web Content

  - Websites, forums, blogs, articles

- 3D Models

  - Games, simulations, and virtual reality.

## Digital Artefact (Image Processing Perspective)

- Unintended or undesirable distortions, anomalies, or visual effects in digital images or videos

- Affect the quality of an image or video,

- Causes: limitations of technology or improper processing

![Image of compression artifacts in an image](Picture2.jpg)

## Example of Digital Artefact

![JPEG artifacts and image noise](Picture6.jpg)

![Chromatic Aberration: How to Detect and ...](Picture2.jpg)

![Ghosting Definition - What is Ghosting ...](Picture8.jpg)

![Mavic 3 Pro-main camera-unusual moiré pattern in image? | DJI FORUM](Picture4.jpg)

## Why is it Important?

- Quality Control

  - Detection of Issues - indicate problems in image generation.

- Creative Effects

  - Create specific visual effects and enhanced story telling

- Technological Development

  - Drives innovation in imaging technology. 

## Advantages

- Enhanced Visual Effects

  - Add a layer of realism to digital images and videos, making them appear more natural and lifelike. 

    Create unique visual styles and artistic effects, contributing to the storytelling and aesthetic of a project. 

- Efficiency in Production

  - Reducing the need for expensive physical effects or props. 

    Easily add or remove artifacts, speeding up the post-production process. 

- Flexibility and Control

  - Achieve the desired effect, allowing for greater flexibility in the creative process

    Changes can be made without permanently altering the original image or footage, enabling experimentation and iterative improvements. 

- Enhanced Storytelling

  - Use color distortion to indicate a character's altered state of mind or adding film grain can give a vintage look

## Narrative Storyboarding

- A visual representation of a story's context and interactions over time.

- Provide a structured approach to visual storytelling and ensuring that the final product aligns with the creator's vision.

- Illustrate the context of an interaction sequence:

  - Physical environment,

  - Actions of people,

  - Events that unfold over time

## Narrative Storyboarding

In the context of digital artifacts

- Creating a visual representation of a story or sequence of events

  - Series of panels or frames.

    - Illustrations, text, and other visual elements.

- Serves as a communication tool among team members, ensuring everyone has a clear understanding of the vision and can contribute effectively

## Example

**Title: The Lost Key**

**Narrative (story framework – event arrangement and presentation)**

- The sequence of events where Lily finds a key and embarks on a quest to discover what it opens.

**Storytelling (story - engaging  entertaining the audience through expressive techniques)**

- The detailed description of Lily's emotions, actions, and discoveries, which brings the narrative to life and engages the reader.

## Narrative

- Once upon a time, in a small village nestled between rolling hills, there lived a young girl named Lily.

- She was known for her curiosity and adventurous spirit.

- One sunny afternoon, while exploring the attic of her grandmother's old house, Lily stumbled upon an ancient, rusty key hidden inside a dusty chest.

## Storytelling

- Lily's eyes sparkled with excitement as she held the key in her hand. "What could this open?" she wondered aloud. Determined to uncover the mystery, she set off on a quest around the village, asking the elders and searching for clues.

- Her journey led her to the edge of the village, where an old, abandoned cottage stood. The door was locked, and the keyhole seemed to match the shape of her newfound key. With a deep breath, Lily inserted the key and turned it. The door creaked open, revealing a room filled with forgotten treasures and memories of the past.

- Inside, she found old photographs, letters, and trinkets that told the story of her ancestors. Among the items, she discovered a diary belonging to her great-grandmother, detailing her life and adventures. Lily spent hours reading the diary, feeling a deep connection to her family's history.

- As the sun set, Lily realized that the key had unlocked more than just a door; it had opened a window to her heritage and identity. She returned home with a heart full of stories and a newfound appreciation for her roots.

## Environment

- Refers to the time and place in which the story occurs.

- Includes various elements

  - Location: geographical place

  - Time Period: Specific time frame.

  - Physical Surroundings: landscape, weather, and physical conditions.

  - Social Context: Cultural and social conditions

![The Lost Key | Story.com](Picture2.jpg)

![The Magical Journey of Lily and the ...](Picture4.jpg)

## Scene

![The Lost Key | Story.com](Picture2.jpg)

![](Picture6.jpg)

- A fundamental unit of storytelling,

- Consist of a sequence of events that occur in a specific location and time.

  - Characters,

  - Actions, and

  - Dialogues

![2D scenes for animation and games](Picture14.jpg)

![Setting up a 2D scene | Adventure Creator](Picture12.jpg)

## Sprite

- 2D image or animation that can be manipulated and moved around on a screen.

- Commonly used in video games and animations to represent characters, objects, and other elements.

![Sprite Character Retrogaming 8-bit, 8 ...](Picture6.jpg)

![Sprite Game Images – Browse 36,141 ...](Picture2.jpg)

![How to Make a Sprite for Games & RPGs | 6 Steps to Drawing with Piskel](Picture4.jpg)

## Rendering

- Process of generating a final image or sequence of images from a 2D or 3D model and scene.

  Stages:

  - vertex processing,

  - rasterization,

  - fragment processing.

- Involves converting the model into a visual representation that can be viewed on a screen.

- To simulate lighting, textures, and camera perspectives, enhancing the storytelling and visual impact of the narrative.

## Review Questions

1. Digital Artefact refer to ______

2. What kind of image can be created using 2D and 3D matrices?

3. Matrix with 3-dimensions refer to _____, width, and _____ channels.

4. ________ refer to the visual representation of a sequence of events

## Summary / Recap of Main Points

- Digital artifacts are not just flaws, also play a crucial role in quality control and creative expression.

- Image

  - Analogue (traditional)

  - Digital form

    - 2D - grayscale

    - 3D – colour

- Narrative Storytelling

  - Why is it important?

## What To Expect Next Week

**In Class**

- Computer Graphic

**Preparation for Class**

- Review various digital artefacts
