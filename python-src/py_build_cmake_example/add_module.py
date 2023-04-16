"""Example module that adds two integers in C++."""

import os
import typing
if not typing.TYPE_CHECKING and os.getenv('PY_BUILD_CMAKE_EXAMPLE_PYTHON_DEBUG'):
    from py_build_cmake_example._add_module_d import *
    from py_build_cmake_example._add_module_d import __version__
else:
    from py_build_cmake_example._add_module import *
    from py_build_cmake_example._add_module import __version__
