# Check Imaging

A collection of tools for processing check images, especially for use in Image Cash Letter (X9) file creation.

## Dependencies

- **Python 3**
- **ImageMagick 7+** There is a bug in ImageMagick 6 that will cause the black and white images to appear red
- **MICR font** For deposit ticket generation

## Example usage

Convert an image of a check to a black and white TIFF for use in an X9 file. You may have to tweak the threshold to arrive at a clear image.

```python
from check_imaging import format_check_image_for_x9

with open('tests/check_front.jpg', 'rb') as in_file:
    converted = format_check_image_for_x9(in_file, threshold=.67)
    with open('tests/check_front.tiff', 'wb') as out_file:
        out_file.write(converted.getvalue())
```
