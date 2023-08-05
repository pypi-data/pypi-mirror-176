"""
Ujan RoyBandyopadhyay
November 2022

View and save randomly colored images generated from JSON files
containing Label Studio annotations.
"""

from __future__ import annotations

import argparse
import json
import random

# Import pygame silently.
from contextlib import redirect_stdout
from io import StringIO
with redirect_stdout(StringIO()):
    import pygame as pg


def _parse_arguments() -> tuple[str, str, bool]:
    """Read and return command line arguments."""
    parser = argparse.ArgumentParser(
        description='generate, view, and save randomly colored images from '
                    'JSON files containing Label Studio annotations'
    )
    parser.add_argument('path_to_json', type=str,
                        help='path to JSON file containing annotations')
    parser.add_argument('image_path', type=str,
                        help='path to save generated image (*.jpg, *.png, '
                             '*.bmp)')
    parser.add_argument('-v', '--view', help='preview generated image',
                        action='store_true')

    args = parser.parse_args()
    return (args.path_to_json, args.image_path, args.view)

def save_image(json_path: str, save_path: str, view: bool = False):
    """Save a colored image generated from a JSON file.

    Arguments:
        - json_path
            path to JSON file containing Label Studio annotations
        - save_path
            path (PNG, JPG, or BMP) where to save generated image
        - view
            whether to view image after saving
    """
    with open(json_path) as file:
        data = json.load(file)[0]['annotations'][0]['result']

    # Convert Label Studio's percentage-based coordinates to pixels.
    raw_polygons = [annotation['value']['points'] for annotation in data]
    width, height = data[0]['original_width'], data[0]['original_height']
    polygons = [[(point[0]/100 * width, point[1]/100 * height)
                for point in polygon] for polygon in raw_polygons]

    # Draw colored image on a pygame surface.
    pg.init()
    surface = pg.Surface((width, height))
    surface.fill((0, 0, 0))
    for polygon in polygons:
        color = tuple(random.randrange(60, 256) for _ in range(3))
        pg.draw.polygon(surface, color, polygon)

    # Save image.
    pg.image.save(surface, save_path)

    # Display image in a new window.
    if view:
        window = pg.display.set_mode((width, height))
        pg.display.set_caption(f'{save_path} — Preview')
        window.blit(surface, (0, 0))
        pg.display.update()

        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                    break

                pg.display.update()


if __name__ == '__main__':
    args = _parse_arguments()
    save_image(*args)