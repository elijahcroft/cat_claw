# tilemap.py
import pygame
import pytmx

class TileMap:
    def __init__(self, filename):
        # Load the map
        self.tmx_data = pytmx.load_pygame(filename)
        self.tile_width = self.tmx_data.tilewidth
        self.tile_height = self.tmx_data.tileheight
        self.map_width = self.tmx_data.width * self.tile_width
        self.map_height = self.tmx_data.height * self.tile_height

    def draw(self, surface):
        """Draw the tile map onto a Pygame surface."""
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        surface.blit(tile, (x * self.tile_width, y * self.tile_height))

    def get_size(self):
        """Return the size of the map in pixels."""
        return self.map_width, self.map_height
