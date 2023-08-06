# Dominant Color Recognizer



## General info
DCR is a Python library created to obtain a specific number of dominant colors from image.
You can define number of colors and color model in which values will be returned.

Currently supported color models:
| Color model  | Example         |
|--------------|-----------------|
|    HEX       | #0040ff         |
|    RGB       | rgb(0, 64, 255) |


## Instalation

Use the package manager [pip](https://pip.pypa.io/en/stable/getting-started/) to install DCR library:
```commandline
pip install dominantcolorrecognizer
```

## Usage

```python
from dominant_color_recognizer import ColorAnalyzer, RGBColorModel, HEXColorModel

# RGB color model:
print(ColorAnalyzer(RGBColorModel()).get_dominant_colors('test.jpg', 3))
# You can also use URL
print(ColorAnalyzer(RGBColorModel()).get_dominant_colors('https://swiatkolorow.com.pl/userdata/public/gfx/252817/1ee9698f09e987d3e9a3785167b180b0.jpg', 3))
# Expected result:
# ["(185, 154, 90)", "(52, 40, 24)", "(25, 18, 0)"]

# HEX color model:
print(ColorAnalyzer(HEXColorModel()).get_dominant_colors('test.jpg', 3))
# Same as with RGB, you can also use URL
print(ColorAnalyzer(HEXColorModel()).get_dominant_colors('https://swiatkolorow.com.pl/userdata/public/gfx/252817/1ee9698f09e987d3e9a3785167b180b0.jpg', 3))
# Expected result:
# ['#B99A5A', '#342818', '#191200']
```

## Tests

To run a tests you have to install [pytest](https://pypi.org/project/pytest/) and run it with the command:
```commandline
pytest
```

## License

Bittapps