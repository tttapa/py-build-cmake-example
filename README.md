# py-build-cmake example project

This is an example project using [py-build-cmake](https://github.com/tttapa/py-build-cmake)
to build Python bindings for C++ code.

The package uses modern CMake, and uses Conan for installing C++ dependencies.
Python stub files for autocompletion and type checking are generated
automatically.

It includes extensive continuous integration (CI) scripts, building and testing
packages using [cibuildwheel](https://github.com/pypa/cibuildwheel), and
additionally cross-compiles the packages for ARM64/AArch64, ARMv7 and ARMv6.
Deployment to the Python Package Index (PyPI) is also fully automated.
