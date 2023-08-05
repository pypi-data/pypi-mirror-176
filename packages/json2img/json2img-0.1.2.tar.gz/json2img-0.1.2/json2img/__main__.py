from __future__ import annotations

import argparse

from json2img.src.json_to_image import save_image

def main():
    args = parse_arguments()
    save_image(*args)

def parse_arguments() -> tuple[str, str, bool]:
    """Read and return command line arguments."""
    parser = argparse.ArgumentParser(
        prog='json2img',
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

if __name__ == '__main__':
    main()
