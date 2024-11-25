[![PyPI Python package](https://img.shields.io/badge/PyPI-Python%20package-blue)](https://test.pypi.org/project/py-build-cmake-example)
[![Python Wheel](https://github.com/tttapa/py-build-cmake-example/actions/workflows/wheels.yml/badge.svg)](https://github.com/tttapa/py-build-cmake-example/actions/workflows/wheels.yml)
[![Documentation](https://img.shields.io/badge/Documentation-main-blue)](https://tttapa.github.io/py-build-cmake)

# py-build-cmake example project

This is an example project using [py-build-cmake](https://github.com/tttapa/py-build-cmake)
to build Python bindings for C++ code.

The package uses modern CMake, and uses Conan for installing C++ dependencies.
Python stub files for autocompletion and type checking are generated
automatically.

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
│       ├── python-build
│       │   └── action.yml      -- CI script to (cross-)compile the package
│       └── wheels.yml          -- CI script to build and publish the package
├── scripts
│   └── ci                      -- CIBW scripts to install Conan dependencies
│       ├── pre-build-macos.py
│       └── pre-build-windows.py
├── test                        -- Unit tests for the package
│   ├── test_add_module.py
│   └── test_sub_package.py
└── examples
    └── add_example.py          -- Python script that imports our package
```

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
python3 -m pip install py-build-cmake~=0.3.0a3
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
py -3 -m pip install py-build-cmake~=0.3.0a3
# Install the debug version of the C++ dependencies
conan install . --build=missing -s build_type=Debug
```

With the project open in VSCode, go to the “Debug” panel and start debugging
using the **“(Windows) Launch Python”** configuration. The Python package will
be built in debug mode automatically (see `.vscode/tasks.json`), and a debug
session will start.
