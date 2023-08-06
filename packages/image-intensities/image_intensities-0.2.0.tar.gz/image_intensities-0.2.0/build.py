import platform
from cffi import FFI
from pathlib import Path

image_intensities_root_path = Path(__file__).parent
image_intensities_sources_path = image_intensities_root_path / "sources"

image_intensities_definitions = """
    extern struct intensity_data {
        double nw;
        double ne;
        double sw;
        double se;
        int error;
    } intensity_data;

    struct intensity_data jpeg_intensities(const char *file_name);
    struct intensity_data png_intensities(const char *file_name);
"""

header_path = (image_intensities_sources_path / "definitions.h").resolve()
extra_kwargs = {}

ffi = FFI()
ffi.cdef("""
    typedef struct intensity_data {
        double nw;
        double ne;
        double sw;
        double se;
        int error;
    } intensity_data;

    struct intensity_data jpeg_intensities(const char *file_name);
    struct intensity_data png_intensities(const char *file_name);
""")

sources = [
    "sources/intensities.c",
    "sources/jpeg.c",
    "sources/png.c",

    "sources/turbojpeg/jsimd_none.c",
    "sources/turbojpeg/jchuff.c",
    "sources/turbojpeg/jcapimin.c",
    "sources/turbojpeg/jcapistd.c",
    "sources/turbojpeg/jccolor.c",
    "sources/turbojpeg/jcicc.c",
    "sources/turbojpeg/jccoefct.c",
    "sources/turbojpeg/jcinit.c",
    "sources/turbojpeg/jcdctmgr.c",
    "sources/turbojpeg/jcmainct.c",
    "sources/turbojpeg/jcmarker.c",
    "sources/turbojpeg/jcmaster.c",
    "sources/turbojpeg/jcomapi.c",
    "sources/turbojpeg/jcparam.c",
    "sources/turbojpeg/jcphuff.c",
    "sources/turbojpeg/jcprepct.c",
    "sources/turbojpeg/jcsample.c",
    "sources/turbojpeg/jctrans.c",
    "sources/turbojpeg/jdapimin.c",
    "sources/turbojpeg/jdapistd.c",
    "sources/turbojpeg/jdatadst.c",
    "sources/turbojpeg/jdatasrc.c",
    "sources/turbojpeg/jdcoefct.c",
    "sources/turbojpeg/jdcolor.c",
    "sources/turbojpeg/jddctmgr.c",
    "sources/turbojpeg/jdhuff.c",
    "sources/turbojpeg/jdicc.c",
    "sources/turbojpeg/jdinput.c",
    "sources/turbojpeg/jdmainct.c",
    "sources/turbojpeg/jdmarker.c",
    "sources/turbojpeg/jdmaster.c",
    "sources/turbojpeg/jdmerge.c",
    "sources/turbojpeg/jdphuff.c",
    "sources/turbojpeg/jdpostct.c",
    "sources/turbojpeg/jdsample.c",
    "sources/turbojpeg/jdtrans.c",
    "sources/turbojpeg/jerror.c",
    "sources/turbojpeg/jfdctflt.c",
    "sources/turbojpeg/jfdctfst.c",
    "sources/turbojpeg/jfdctint.c",
    "sources/turbojpeg/jidctflt.c",
    "sources/turbojpeg/jidctfst.c",
    "sources/turbojpeg/jidctint.c",
    "sources/turbojpeg/jidctred.c",
    "sources/turbojpeg/jquant1.c",
    "sources/turbojpeg/jquant2.c",
    "sources/turbojpeg/jutils.c",
    "sources/turbojpeg/jmemmgr.c",
    "sources/turbojpeg/jmemnobs.c",
    "sources/turbojpeg/jaricom.c",
    "sources/turbojpeg/jdarith.c",
    "sources/turbojpeg/jcarith.c",
    "sources/turbojpeg/turbojpeg.c",
    "sources/turbojpeg/transupp.c",
    "sources/turbojpeg/jdatadst-tj.c",
    "sources/turbojpeg/jdatasrc-tj.c",
    "sources/turbojpeg/rdbmp.c",
    "sources/turbojpeg/rdppm.c",
    "sources/turbojpeg/wrbmp.c",
    "sources/turbojpeg/wrppm.c",
]

include_dirs = [  # -I
    'sources/',
    'sources/turbojpeg/',
]
libraries = [  # -L
    'png',
]
extra_compile_args = [
    "-std=c99",
    "-fPIC",
    "-O3",
    "-DPPM_SUPPORTED",
    "-DBMP_SUPPORTED",
]

if "Windows" in platform.system():
    extra_kwargs["extra_link_args"] = ["/NODEFAULTLIB:MSVCRTD"]
    extra_kwargs["libraries"] = ["advapi32"]
# end def

ffi.set_source(
    'image_intensities._intensities',
    f'#include "{ str(header_path) }"',
    sources=sources,
    include_dirs=include_dirs,  # -I
    libraries=libraries,  # -L
    extra_compile_args=extra_compile_args,
    **extra_kwargs,
)

# end def


intensities_ffi = ffi

if __name__ == "__main__":
    intensities_ffi.compile(verbose=True)
# end def
