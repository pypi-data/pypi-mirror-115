import image_intensities.classes as classes
import image_intensities.intensities as intensities

from .classes import Luma

try:
    from .intensities import jpeg_intensities, png_intensities
except ImportError:
    from .pure_python import rgb_luma_from_filename
    jpeg_intensities = rgb_luma_from_filename
    png_intensities = rgb_luma_from_filename
# end try
