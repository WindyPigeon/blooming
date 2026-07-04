CT029-3-2 Imaging and Special Effects
# Special Effects and Visual Effects

## TOPIC LEARNING OUTCOMES

- At the end of this topic, you should be able to:

- Differentiate between the Special and Visual Effects.

- Integrate and Optimize the effects

- Apply it on different domains

## Contents & Structure

Special Effect and Visual Effects

- Integration

- Optimization

- Domain Application

## Recap From Last Lesson

![Recap Clip Art Image - ClipSafari](Picture2.jpg)

Question: Identify the technique to create the following scene

![what is motion blur in games](Picture2.jpg)

## Recap

| | |
| --- | --- |
| Special Effects (SFX) | Practical effects used in physical environments e.g., explosions, animatronics. |
| Visual Effects (VFX) | Implement Computer-generated imagery (CGI) Create or enhance visuals E.g. fire, smoke, magic, weather, and etc. |

**Often overlaps with each other

## Purpose

- Immersion

  - Simulates realistic or fantastical environments.

  - Emotion engagement

- Feedback

  - Communicates player actions and understand the state and actions.

- Narrative

  - Supports storytelling through cinematic effects.

- Aesthetics

  - Adds polish and visual appeal.

## Techniques

| | |
| --- | --- |
| **Particle Systems** | smoke, sparks |
| **Shaders** | surface effects -glowing, transparency |
| **Physics Simulation** | destruction, cloth, fluids |
| **Post-Processing** | After effect rendering - Bloom(bright lighting), motion blur, color grading |
| **AI Techniques** | Create content – texture, collision effect, style and strategies |

## Principles

- **Readability**

  - Effects should be clear and not clutter gameplay.

- **Consistency**

  - Match the game’s art style and tone.

- **Performance**

  - Optimize effects to maintain frame rates.

- **Timing**

  - Sync effects with gameplay events for maximum impact.

## Special Effects Integration

- Appropriate Effect

  - Based on logic, theme and narrative

- Effect Placement

  - Position effects where they enhance gameplay without clutter.

- Trigger Systems

  - User events to activate effects. (e.g collision)

- Layering

  - Combine sound, particles, and lighting for immersive feedback.

- Timing & Sync

  - Align effects with animations and gameplay logic

## Optimization

- **Purpose**

  - Game runs smoothly and doesn’t lag or crash

- 

  - Real-Time Constraints

    - Target frame rate: 30–60 FPS

    - Effects must run smoothly across devices

  - Optimization Goals

    - Reduce CPU/GPU load

    - Minimize memory usage

    - Avoid frame drops and stuttering

## Optimization Tips

<ins>**Potential Issue**</ins>

- Too many effects at once

  - Use fewer or smaller effects

- Effects keep restarting

  - Use object pooling (reuse effects instead of making new ones)

- Effects off-screen still running

  - Use culling (turn off effects the player can’t see)

- Big textures or sounds

  - Use compressed files (smaller size = faster game)

## Best Practices

- Design scalable effects for different devices

  - Support and compatible

- Modular effects

  - Reuse effects when possible (don’t keep making new ones)

- Keep your effects short and simple

- Use effects only when they help the player

- Don’t use too many effects at once

## Applications in Computer Science

- **Graphics Programming**

  - Apply APIs like OpenGL, DirectX.

- **Real-Time Rendering**

  - Optimizing effects for performance.

- **Simulation Algorithms**

  - Physics engines

- **Data Structures**

  - Efficient handling of particles and terrains

- **Parallel Computing**

  - GPU acceleration for rendering effects. (Hardware integration)

## Applications in AI

- Procedural Generation

  - Create environments and effects dynamically.

- Motion Capture & Animation

  - Character movements and facial expressions.

- Reinforcement Learning

  - Optimize effect parameters for realism.

- Computer Vision

  - Apply context-aware effects.

## Applications in Games

- Atmosphere and Environment

  - Audio transitions between scenes

  - Volumetric fog, light shafts, and glow effects, thunder, whispers, distant roars

  - Particle effects: dust, fog, rain, snow

- Feedback

  - Combat actions via sound , damage alerts, item pickup chimes

- Immersion

  - Player sense of presence and realism in the game world

  - Screen shake, Breathing, heartbeat

## Summary / Recap of Main Points

- Principles

  - Readability, Consistence, Performance, Timing 

- Integration

  - The right effect, placement, trigger, timing 

- Optimization

  - Scalable, modular –reused, simple and short
  
## What To Expect Next Week
**In Class**
- Revision

**Preparation for Class**
- -
