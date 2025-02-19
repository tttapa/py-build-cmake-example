# pyodide-build sets the CMAKE_TOOLCHAIN_FILE environment variable to point to
# its own wrapper for the emsdk toolchain file. We need to include this emsdk
# wrapper in the current toolchain file, so read the environment variable and
# save its value in the cache for later.
# Since the Pyodide toolchain file is in a temporary folder, it may be deleted
# at any point, so we always check if it exists, and we update our cache entry
# accordingly.
if (DEFINED ENV{CMAKE_TOOLCHAIN_FILE} AND (NOT DEFINED PYODIDE_TOOLCHAIN_FILE
                                           OR NOT EXISTS "${PYODIDE_TOOLCHAIN_FILE}"))
    set(PYODIDE_TOOLCHAIN_FILE "$ENV{CMAKE_TOOLCHAIN_FILE}" CACHE INTERNAL "")
endif()
# Make sure the Pyodide toolchain file is selected.
if (NOT DEFINED PYODIDE_TOOLCHAIN_FILE OR NOT "${PYODIDE_TOOLCHAIN_FILE}" MATCHES "Emscripten.cmake$")
    message(FATAL_ERROR "Invalid value of PYODIDE_TOOLCHAIN_FILE: ${PYODIDE_TOOLCHAIN_FILE}")
endif()
message(STATUS "Including Pyodide toolchain: ${PYODIDE_TOOLCHAIN_FILE}")
include("${PYODIDE_TOOLCHAIN_FILE}")

# These CMAKE_XXX_FLAGS variables are set by the Pyodide toolchain file, but
# they would override the Conan flags. Instead, toolchain files should set the
# CMAKE_XXX_FLAGS_INIT versions of these variables.
set(CMAKE_C_FLAGS_INIT ${CMAKE_C_FLAGS})
set(CMAKE_CXX_FLAGS_INIT ${CMAKE_CXX_FLAGS})
set(CMAKE_SHARED_LINKER_FLAGS_INIT ${CMAKE_SHARED_LINKER_FLAGS})
unset(CMAKE_C_FLAGS)
unset(CMAKE_CXX_FLAGS)
unset(CMAKE_SHARED_LINKER_FLAGS)
