# json2img

A Python script for generating randomly colored images from Label Studio annotations

## Installation
```shell
% pip install json2img
```

## Usage

### Command line

```shell
% python -m json2img brick_annotation.json bricks.png
% python -m json2img hand_annotation.json sign.jpg -v
```

### Module

```python
>>> from json2img import *
>>> save_image('brick_annotation.json', 'bricks.png')
>>> save_image('hand_annotation.json', 'sign.jpg', view=True)
```
## Dependencies

* CPython >= 3.7
* pygame >= 2.0.0
