from conan import ConanFile
from conan.tools.cmake import cmake_layout


class Recipe(ConanFile):
    name = "py-build-cmake-example"

    settings = "os", "compiler", "build_type", "arch"
    options = {"with_conan_python": [True, False]}
    default_options = {"with_conan_python": False}
    options_descriptions = {
        "with_conan_python": "Use Conan to provide the Python development files"
    }
    generators = "CMakeDeps", "CMakeToolchain"

    def requirements(self):
        self.requires("pybind11/2.13.6")
        if self.options.with_conan_python:
            self.requires("tttapa-python-dev/3.13.1")

    def layout(self):
        cmake_layout(self)
