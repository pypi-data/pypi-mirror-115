# image_intensities
Python implementation of the great [derpibooru/image_intensities](https://github.com/derpibooru/image_intensities/tree/8aa43674f61f77cfc756c23556b6ae45e1b210b1).

> The algorithmic overview is to convert the image into the yuv colorspace, drop the u and v components, 
> and then average the y component over 4 evenly-spaced rectangles on the image dimensions.

# Usage

```python
from image_intensities import png_intensities, jpg_intensities, image_intensities, Intensities

# Let's calculate some values
luma_a = png_intensities('/absolute/path/to/954482.png')  # image can ge found in the tests folder.
luma_b = jpg_intensities('/absolute/path/to/2544057.jpg')  # image can ge found in the tests folder.
# if you don't know the file type, you can have it picked up with the `mimetype` module:
luma_b = image_intensities('/absolute/path/to/2544057.jpg')  # image can ge found in the tests folder.

# returns something like
luma_a = Intensities(nw=35.832628091300684, ne=10.513891063388744, sw=20.76546499989676, se=20.831389937866714)
luma_b = Intensities(nw=8.284639125603292, ne=8.466390155604937, sw=22.851929679674072, se=23.26008498727572)

# You can compare them, exact match (which is probably not what you want, see .compare(…) below)
luma_a == luma_b
# -> False

# or a distance comparison
luma_a.compare(luma_b, distance=0.25)
# -> False  # those two images are very different, after all
```

A good distance is usually between `0.2` and `0.5`, the default is `0.25`.


### Pure Python
There's also a pure python version, which thanks to PIL/Pillow supports about every image type:

> ⚠️ Note: You need to install **Pillow** (`pip install Pillow`) for this to work, see [Dependencies](#dependencies) below.  
> ⚠️ Note: For animated image types it will probably use the first frame.

```python
from image_intensities.pure_python import png_intensities, jpg_intensities, image_intensities, Intensities

luma = image_intensities('/path/to/image.gif')

# returns something like
luma == Intensities(nw=0.42, ne=0.44, sw=0.58, se=0.69)
```

# Documentation
If not mentioned otherwise, those are available for both the speed up native c and the pure python variant.

#### class `Intensities` <a name="intensities" href="#top">🔝</a>

This is the class returned by the calculations, containing the 4 quadrant sums.

Field | Type | Description
----- | ---- | -----------
nw | float | the first (top left) quadrant    
ne | float | the second (top right) quadrant    
sw | float | the third (bottom left) quadrant    
se | float | the last (bottom right) quadrant    

#### def `png_intensities(…)` <a name="png_intensities" href="#top">🔝</a>

This function calculates the sums over a given PNG file. 

Parameter | Type | Required | Description
--------- | ---- | -------- | -----------
filename | str | Yes | The absolute path to the PNG file to run the sums over. 

#### def `jpg_intensities(…)` <a name="jpg_intensities" href="#top">🔝</a>

This function calculates the sums over a given JPG file. 

Parameter | Type | Required | Description
--------- | ---- | -------- | -----------
filename | str | Yes | The absolute path to the JPG file to run the sums over. 


#### def `image_intensities(…)` <a name="image_intensities" href="#top">🔝</a>

This function calculates the sums over a given file, with unknown file type.
> Note: if you're using the cffi bindings, only PNG and JPEG are available natively. It will try to use Pillow/PIL if installed to read other formats.  
> Note: if you're using the pure python version, Pillow/PIL needs to be installed.

Parameter | Type | Required | Description
--------- | ---- | -------- | -----------
filename | str | Yes | The absolute path to the JPG file to run the sums over. 


#### def `pixel_array_intensities(…)` <a name="pixel_array_intensities" href="#top">🔝</a>
<!-- pixels: Union[List[int], List[Tuple[int, int, int]]], *, width: int, height: int -->
This function calculates the sums over the given image pixel data.

> Note, the given list of `pixels` has to have a length of `width x height` for the tuple form, or `width x height x 3` for the continuous integer stream.  

Parameter | Type | Required | Description
--------- | ---- | -------- | -----------
pixels | List[int] or List[Tuple[int, int, int]] | Yes | List of pixel values, either a tuple of `(R, G, B)` integers (0-255) or a continuous list of `R`, `G` and `B` values of pixels.
width | int | Yes | Width of the image, needed to figure out the quadrant a pixel is in.
height | int | Yes | Height of the image, needed to figure out the quadrant a pixel is in. 


#### def `pixel_bytes_intensities(…)` <a name="pixel_bytes_intensities" href="#top">🔝</a>
<!-- pixels: Union[List[int], List[Tuple[int, int, int]]], *, width: int, height: int -->
This function calculates the sums over the given image pixel data.

> Note, the given list of `pixels` has to have a length of `width x height`.  

Parameter | Type | Required | Description
--------- | ---- | -------- | -----------
pixels | bytes | Yes | A binary stream of `R`, `G` and `B` values, repeated for every pixel. (For example it could look like `b'\0x255\0x0\0x44\0x58\0x0\0x69...'`).
width | int | Yes | Width of the image, needed to figure out the quadrant a pixel is in.
height | int | Yes | Height of the image, needed to figure out the quadrant a pixel is in. 
 


# Dependencies
### C-Extension
#### MacOS
```bash
brew install libpng
```
 (tested to work with 1.6.37)

#### Ubuntu
(There's also a version for [Dockerfiles](#dockerfile) available)
```bash
sudo apt-get update
sudo apt-get install libpng-dev
```

<a name="dockerfile"></a>
#### Dockerfile (Ubuntu based)
```bash
apt-get update -y && apt-get install -y libpng-dev && apt-get clean && rm -rfv /var/lib/apt/lists/*
```
> ⚠️ Make sure you pull a recent release of the python docker image (even if it's an older python version!).
> Especially if you're getting errors complaining about a `png_set_longjmp_fn` function when you try to use it.
> As time of writing the 2-month old version did not work, but the newest releases (`python:3.6`: `6ac87e65b6d0`, `pythong:3.9`: `1b33974176a3`) ones have that fixed.  

### Pure python algorithm _(optional)_
This one is usually not needed, unless you wanna benefit from pillow's ability to read the strangest image formats.
But probably it's faster to write it to disk as either `.jpg` or `.png` and use the native C versions as above.

```bash
pip install Pillow
```

# Installation
See dependencies above, and make sure those are installed as needed. 

### Install via pip
```bash
pip install image_intensities
```

##### Mac OS:
```bash
CPPFLAGS='-I/usr/local/include/' LDFLAGS='-L/usr/local/lib/' pip install image_intensities
```

### From source
E.g. you checked out this repository:
```bash
python setup.py install
```

##### Mac OS:
```bash
CPPFLAGS='-I/usr/local/include/' LDFLAGS='-L/usr/local/lib/' python setup.py install
```


### Minimal installation example

Using docker as it already has a working `libpng-dev`:

```sh
docker pull python:3.9
docker run -it --rm python:3.9 bash
pip install image_intensities

# test import
python -c"import image_intensities as it; print(it._intensities.ffi)"

# test with a png
wget https://derpicdn.net/img/download/2015/8/9/954482.png -O /tmp/954482.png
python -c"from image_intensities import png_intensities; print(png_intensities('/tmp/954482.png'))"

# test with a jpg
wget https://derpicdn.net/img/download/2021/2/4/2544057.jpg -O /tmp/2544057.jpg  # we need to use an absolute path!
python -c"from image_intensities import jpg_intensities; print(jpg_intensities('/tmp/2544057.jpg'))"
```
