[![PyPI Python package](https://img.shields.io/badge/PyPI-Python%20package-blue)](https://test.pypi.org/project/py-build-cmake-example)
[![Python Wheel](https://github.com/tttapa/py-build-cmake-example/actions/workflows/wheels.yml/badge.svg)](https://github.com/tttapa/py-build-cmake-example/actions/workflows/wheels.yml)
[![Documentation](https://img.shields.io/badge/Documentation-main-blue)](https://tttapa.github.io/py-build-cmake)

# py-build-cmake example project

This is an example project using [py-build-cmake](https://github.com/tttapa/py-build-cmake)
to build Python bindings for C++ code.

## Features

 - Building Python bindings for C++ code
 - `pyproject.toml` for configuration and metadata
 - Modern CMake build system
 - Installation of C++ dependencies using Conan
 - Automatic Python stub file generation for autocomplete and type checking
 - Continuous integration workflows for building Wheel packages for various platforms
 - Conan dependency caching
 - Compilation caching using sccache
 - Trusted publishing to PyPI
 - Testing using `pytest`

The project uses modern CMake, and uses Conan for painless installation of C++
dependencies. Python stub files for autocompletion and type checking are
generated automatically.

It includes extensive continuous integration (CI) scripts, building and testing
packages using [cibuildwheel](https://github.com/pypa/cibuildwheel), and
additionally cross-compiles the packages for AMD64/x86-64, ARM64/AArch64,
ARMv7 and ARMv6.
Deployment to the Python Package Index (PyPI) is also fully automated and uses
trusted publishing.

## Project layout

```
py-build-cmake-example
├── README.md
├── LICENSE
├── pyproject.toml         -- Python project metadata and py-build-cmake options
├── conanfile.txt          -- C++ dependencies
├── CMakeLists.txt         -- CMake build script
├── src
│   └── add_module.cpp          -- pybind11 extension module written in C++
├── python-src
│   └── py_build_cmake_example  -- Python package (without extension module)
│       ├── __init__.py
│       ├── add_module.py            -- Wrapper for the extension module
│       ├── add.py                   -- Command line utility using the package
│       ├── py.typed                 -- PEP 561 marker file
│       └── sub_package              -- Python-only sub-package
│           ├── __init__.py
│           └── sub.py
├── cmake
│   └── Pybind11Stubgen.cmake   -- automatic Python stub generation
├── .github
│   └── workflows
│       ├── setup-conan
│       │   └── action.yml      -- CI script to install Conan and sccache
│       └── wheels.yml          -- CI script to build and publish the package
├── scripts
│   └── ci                      -- Continuous integration scripts and configs
│       ├── ...                    -- Shell and Python scripts for building
│       └── profiles               -- Conan profiles with build configurations
│           └── ...
├── test                        -- Unit tests for the package
│   ├── test_add_module.py
│   └── test_sub_package.py
└── examples
    └── add_example.py          -- Python script that imports our package
```

## Continuous Integration

The continuous integration workflows are built using GitHub actions and perform
the following steps when creating a release:

 1. The package is built natively on Linux. This allows importing the package to
    generate the Python stub files (for type hints and code completion). These
    stub files are then included in the cross-compiled packages later on.
 2. The unit tests are run using pytest.
 3. The package is cross-compiled for various Python versions, architectures and
    operating systems (Linux x86-64, ARM64, ARMv7 and ARMv6; Windows x86, x86-64
    and ARM64; macOS Universal2, x86-64 and ARM64).
 4. A final pre-release check is performed to make sure the version of the
    Python package matches the version of the GitHub release.
 5. The package is published to test-PyPI using trusted publishing.

![CI pipeline](https://tttapa.github.io/py-build-cmake/images/ci-pipeline.png)

## Local installation

Make sure you have Python 3 and a C++ compiler installed. CMake and Ninja can be
installed using Pip.

**Linux/macOS**
```sh
# Install Conan and other build tools
python3 -m pip install -U pip conan build pytest cmake ninja
# Generate a default Conan profile (only needed if you didn't use Conan before)
conan profile detect
# Install the project's dependencies using Conan (Linux/macOS)
conan install . --build=missing -c tools.cmake.cmaketoolchain:generator="Ninja Multi-Config"
# Build the Python Wheel package
python3 -m build -w
# Install the Python package
python3 -m pip install -v .
# Test the Python package
python3 -m pytest
# Use the command-line utility provided by the package
add 1 2  # >> 3
# Run the example script
python3 examples/add_example.py
```

**Windows**
```sh
# Install Conan and other build tools
py -3 -m pip install -U pip conan build pytest cmake
# Generate a default Conan profile (only needed if you didn't use Conan before)
conan profile detect
# Install the project's dependencies using Conan (Linux/macOS)
conan install . --build=missing
# Build the Python Wheel package
py -3 -m build -w
# Install the Python package
py -3 -m pip install -v .
# Test the Python package
py -3 -m pytest
# Use the command-line utility provided by the package
add 1 2  # >> 3
# Run the example script
py -3 examples/add_example.py
```

## Debugging (VSCode)

**Linux/macOS**
```sh
# Install py-build-cmake
python3 -m pip install py-build-cmake~=0.4.0a0 pybind11-stubgen~=2.5.1
# Install the debug version of the C++ dependencies
conan install . --build=missing -c tools.cmake.cmaketoolchain:generator="Ninja Multi-Config" -s build_type=Debug
```

With the project open in VSCode, go to the “Debug” panel and start debugging
using the **“(gdb) Launch Python”** configuration. The Python package will be
built in debug mode automatically (see `.vscode/tasks.json`), and a debug
session will start.

**Windows**
```sh
# Install py-build-cmake
py -3 -m pip install py-build-cmake~=0.4.0a0 pybind11-stubgen~=2.5.1
# Install the debug version of the C++ dependencies
conan install . --build=missing -s build_type=Debug
```

With the project open in VSCode, select a debug version of Python
(<kbd>Ctrl+Shift+P</kbd>, “Python: Select Interpreter”, `python_d.exe`), then
go to the “Debug” panel and start debugging using the
**“(Windows) Launch Python”** configuration. The Python package will be built
in debug mode automatically (see `.vscode/tasks.json`), and a debug session
will start.
