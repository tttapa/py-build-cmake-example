import os
import re
from pathlib import Path
from subprocess import run
import subprocess as sp

project_dir = Path(__file__).parent.parent.parent
os.chdir(project_dir)

assert "PYODIDE_ROOT" in os.environ

# Determine the Clang version
result = run(["emcc", "-v"], stderr=sp.PIPE, text=True, check=True)
print(result.stderr)
m = re.search(r"clang version (\d+)", result.stderr)
if not m:
    raise RuntimeError("Failed to determine Emscripten emcc Clang version")
clang_version = m.group(1)

# We need a wrapper around the Pyodide toolchain file, because it is only set
# later during the actual build, we don't know its path yet during the pre-build
# stage. We also need to patch up some CMake variables set by Pyodide.
toolchain_file = project_dir / "scripts" / "ci" / "pyodide.toolchain.cmake"

# Compilers, tools and flags
compilers = {"c": "emcc", "cpp": "em++"}
binutils = {  # use the em-prefixed binutils programs
    f"CMAKE_{t.upper()}": f"em{t}" for t in ("ar", "nm", "ranlib", "strip")
}
no_binutils = {  # otherwise CMake sets these to /usr/bin/objcopy etc.
    f"CMAKE_{t.upper()}": "FALSE"
    for t in ("objcopy", "objdump", "readelf", "addr2line")
}
module_linker_flags = {  # https://github.com/conan-io/conan/issues/17539
    f"CMAKE_MODULE_LINKER_FLAGS{c}_INIT": f"${{CMAKE_SHARED_LINKER_FLAGS{c}_INIT}}"
    for c in ("", "_DEBUG", "_RELEASE", "_RELWITHDEBINFO")
}

profile = f"""\
[settings]
os=Emscripten
arch=wasm
compiler=clang
compiler.version={clang_version}
compiler.libcxx=libc++
build_type=Release

[conf]
tools.gnu:host_triplet=wasm32-unknown-emscripten
tools.cmake.cmaketoolchain:generator=Ninja Multi-Config
tools.build.cross_building:can_run=False
tools.build:skip_test=True
tools.cmake.cmaketoolchain:user_toolchain=+[{repr(toolchain_file.as_posix())}]
tools.cmake.cmaketoolchain:extra_variables*={repr(binutils)}
tools.cmake.cmaketoolchain:extra_variables*={repr(no_binutils)}
tools.cmake.cmaketoolchain:extra_variables*={repr(module_linker_flags)}
# https://github.com/pybind/pybind11/blob/v2.13.6/tools/pybind11Common.cmake#L78-L102
tools.cmake.cmaketoolchain:extra_variables*={{'_pybind11_no_exceptions': 'On'}}
tools.build:compiler_executables={repr(compilers)}

[buildenv]
CC=emcc
CXX=em++
AR=emar
NM=emnm
RANLIB=emranlib
STRIP=emstrip
"""

print(profile)
Path("cibw.profile").write_text(profile)

opts = dict(shell=True, check=True)
run("conan install . -pr:h ./cibw.profile --build=missing", **opts)
