cmake_minimum_required(VERSION 3.18)
project(py-build-cmake-example VERSION 0.3.0)
set(PY_VERSION_SUFFIX "a3")  # e.g. b3.dev1, see PEP 440
set(PY_FULL_VERSION ${PROJECT_VERSION}${PY_VERSION_SUFFIX})

# Make sure that the Python and CMake versions match
if (DEFINED PY_BUILD_CMAKE_PACKAGE_VERSION)
    if (NOT "${PY_BUILD_CMAKE_PACKAGE_VERSION}" MATCHES "^${PY_FULL_VERSION}$")
        message(FATAL_ERROR "Version number does not match "
                             "(${PY_BUILD_CMAKE_PACKAGE_VERSION} - ${PY_FULL_VERSION}).")
    endif()
endif()

# Find the pybind11 package
include(cmake/QueryPythonForPybind11.cmake)
find_pybind11_python_first()

# Compile the example Python module
pybind11_add_module(_add_module MODULE "src/add_module.cpp")
target_compile_definitions(_add_module PRIVATE
    MODULE_NAME=$<TARGET_FILE_BASE_NAME:_add_module>
    VERSION_INFO="${PY_FULL_VERSION}"
)
# Hide all symbols by default (including external libraries on Linux)
set_target_properties(_add_module PROPERTIES
    CXX_VISIBILITY_PRESET "hidden"
    VISIBILITY_INLINES_HIDDEN true)
if (CMAKE_SYSTEM_NAME MATCHES "Linux")
    target_link_options(_add_module PRIVATE "LINKER:--exclude-libs,ALL")
endif()

# Install the Python module
set(PYTHON_MODULE_DESTINATION ${PY_BUILD_CMAKE_MODULE_NAME})
install(TARGETS _add_module
        EXCLUDE_FROM_ALL
        COMPONENT python_modules
        DESTINATION ${PYTHON_MODULE_DESTINATION})
# Install the debug file for the Python module (Windows only)
if (WIN32)
    install(FILES $<TARGET_PDB_FILE:_add_module>
            EXCLUDE_FROM_ALL
            COMPONENT python_modules
            DESTINATION ${PYTHON_MODULE_DESTINATION}
            OPTIONAL)
endif()

# Generate stubs for the Python module
set(PY_STUBS_INSTALLDIR ""
    CACHE PATH "Installation directory for Python stubs (relative to Python package)")
set(WITH_PY_STUBS_DEFAULT On)
if (CMAKE_CROSSCOMPILING)
    set(WITH_PY_STUBS_DEFAULT Off)
endif()
option(WITH_PY_STUBS
    "Generate Python stub files (.pyi) for the Python module."
    ${WITH_PY_STUBS_DEFAULT})
if (WITH_PY_STUBS)
    include(cmake/Pybind11Stubgen.cmake)
    pybind11_stubgen(_add_module
        PACKAGE ${PYTHON_MODULE_DESTINATION}
        DESTINATION ${PY_STUBS_INSTALLDIR}
        COMPONENT python_stubs
    )
endif()
