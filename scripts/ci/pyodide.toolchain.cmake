if (NOT DEFINED ENV{CMAKE_TOOLCHAIN_FILE} OR NOT "$ENV{CMAKE_TOOLCHAIN_FILE}" MATCHES "Emscripten.cmake$")
    message(FATAL_ERROR "Invalid value of CMAKE_TOOLCHAIN_FILE: $ENV{CMAKE_TOOLCHAIN_FILE}")
endif()
message(STATUS "Including Pyodide toolchain: $ENV{CMAKE_TOOLCHAIN_FILE}")
include("$ENV{CMAKE_TOOLCHAIN_FILE}")

# The CMAKE_XXX_FLAGS variables are set by the Pyodide toolchain file, but they
# would override the Conan flags. Instead, toolchain files should set the
# CMAKE_XXX_FLAGS_INIT versions of these variables.
set(CMAKE_C_FLAGS_INIT ${CMAKE_C_FLAGS})
set(CMAKE_CXX_FLAGS_INIT ${CMAKE_CXX_FLAGS})
set(CMAKE_SHARED_LINKER_FLAGS_INIT ${CMAKE_SHARED_LINKER_FLAGS})
unset(CMAKE_C_FLAGS)
unset(CMAKE_CXX_FLAGS)
unset(CMAKE_SHARED_LINKER_FLAGS)
