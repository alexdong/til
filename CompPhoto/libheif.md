# Install pyheif 0.5+ on ubuntu 18+

[pyheif](https://pypi.org/project/pyheif/) is a wrapper around the [libheif](https://github.com/strukturag/libheif). Unfortunately
the default `libheif` that comes with Ubuntu 18.04 does not work with the latest pyheif.

```shell
# Default libheif is 1.1.0
$ apt search libheif

Sorting... Done
Full Text Search... Done
libheif-dev/bionic,now 1.1.0-2 amd64 [installed]
  ISO/IEC 23008-12:2017 HEIF file format decoder - development files

libheif-examples/bionic 1.1.0-2 amd64
  ISO/IEC 23008-12:2017 HEIF file format decoder - examples

libheif1/bionic,now 1.1.0-2 amd64 [installed,automatic]
  ISO/IEC 23008-12:2017 HEIF file format decoder - shared library


# Build pyheif against 1.1.0 does not quite work. 
$ pip install pyheif

...

    build/temp.linux-x86_64-3.7/_libheif_cffi.c:5445:59: error: invalid application of ‘sizeof’ to incomplete type ‘enum heif_color_profile_type’
       { "heif_color_profile_type", 225, _cffi_prim_int(sizeof(enum heif_color_profile_type), ((enum heif_color_profile_type)-1) <= 0),
                                                               ^
    build/temp.linux-x86_64-3.7/_libheif_cffi.c:467:7: note: in definition of macro ‘_cffi_prim_int’
          (size) == 8 ? ((sign) ? _CFFI_PRIM_INT64 : _CFFI_PRIM_UINT64) :    \
           ^~~~
    build/temp.linux-x86_64-3.7/_libheif_cffi.c:467:13: warning: comparison between pointer and integer
          (size) == 8 ? ((sign) ? _CFFI_PRIM_INT64 : _CFFI_PRIM_UINT64) :    \
                 ^
```

Luckily the developer for `libheif` maintains an Ubuntu PPA with the latest build. So here are the steps to grab the latest libheif so you can proceed with pyheif.  

```shell
$ sudo add-apt-repository ppa:strukturag/libheif
$ apt install libheif-dev
$ pip install pyheif
```
