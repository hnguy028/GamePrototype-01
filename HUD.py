class HUD:
    # initialize hud variables
    def __init__(self, hudSize, world):
        # hud size in tiles
        self.hudSize = hudSize

        world.surface.blit()
