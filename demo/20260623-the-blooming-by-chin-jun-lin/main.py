"""
THE BLOOMING
============
A 2D point-and-click psychological horror game (flora theme).
Group 24  -  CT029-3-2 Imaging and Special Effects.

RUN:
    python main.py

CONTROLS:
    Left click  - interact with hotspots / advance dialogue / menu
    Click an inventory item to SELECT it, then click a target to USE it
    J           - open / close the journal
    Space/Enter - advance dialogue
    Esc         - quit

To add your own art and audio, just drop correctly named files into the
assets/ folders. See ASSET_GUIDE.md. No code changes needed.
"""

import sys
import os
import pygame

# Make sure imports work no matter where the game is launched from.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import settings as S


def main():
    pygame.init()
    # Audio is optional; if a machine has no audio device, keep running silently.
    try:
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.mixer.init()
    except pygame.error:
        print("[audio] no audio device found - running without sound.")

    screen = pygame.display.set_mode((S.WIDTH, S.HEIGHT))
    pygame.display.set_caption(S.TITLE)
    clock = pygame.time.Clock()

    # Import after display is up (some sprites are pre-rendered on load).
    from core.assets import AssetManager
    from core.scene import GameContext, SceneManager
    from scenes.menu import MenuScene

    print("\n=== THE BLOOMING - asset check ===")
    print("Any line below marked [placeholder] means the game is using a")
    print("generated stand-in; drop a real file at that path to replace it.\n")

    assets = AssetManager()
    ctx = GameContext(assets)
    manager = SceneManager(ctx)
    manager.start(MenuScene)

    print("\n(Placeholders are fine - the game is fully playable as-is.)\n")

    running = True
    while running:
        dt = clock.tick(S.FPS) / 1000.0
        dt = min(dt, 0.05)  # clamp to avoid huge steps after a stall

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                running = False
            else:
                manager.handle_event(e)

        manager.update(dt)
        manager.draw(screen)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
