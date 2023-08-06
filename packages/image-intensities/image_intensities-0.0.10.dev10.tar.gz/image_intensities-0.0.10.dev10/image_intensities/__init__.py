import image_intensities.classes as classes
import image_intensities.intensities as intensities
from .classes import Intensities
from .version import VERSION, __version__

__all__ = [
    'classes', 'intensities',
    'jpg_intensities', 'png_intensities', 'image_intensities',
    '__version__', 'VERSION'
]

try:
    from .intensities import jpg_intensities, png_intensities, image_intensities
except ImportError:
    from .pure_python import jpg_intensities, png_intensities, image_intensities
# end try
