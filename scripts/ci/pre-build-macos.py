import os
import re
import platform
from pathlib import Path
from subprocess import run

os.chdir(Path(__file__).parent.parent.parent)

archflags = os.getenv("ARCHFLAGS")
archs = ()
if archflags:
    archs = tuple(sorted(re.findall(r"-arch +(\S+)", archflags)))

print("ARCHFLAGS:", archs)
print("PLATFORM: ", platform.machine())
print("MACOSX_DEPLOYMENT_TARGET:", os.getenv("MACOSX_DEPLOYMENT_TARGET"))
print(flush=True)

if not archs:
    archs = (platform.machine(),)
deployment_target = os.getenv("MACOSX_DEPLOYMENT_TARGET", "11.0")
can_run = platform.machine() in archs
conan_arch = {
    ("x86_64",): "x86_64",
    ("arm64",): "armv8",
    ("arm64", "x86_64"): "armv8|x86_64",
}[archs]
conan_arch_custom = {
    ("x86_64",): "x86-64-v2",
    ("arm64",): "apple-m1",
    ("arm64", "x86_64"): "x86-64-v2-apple-m1",
}[archs]
cpu_flags = {
    ("x86_64",): ["-march=x86-64-v2"],
    ("arm64",): ["-mcpu=apple-m1"],
    ("arm64", "x86_64"): [
        "-Xarch_arm64",
        "-mcpu=apple-m1",
        "-Xarch_x86_64",
        "-march=x86-64-v2",
    ],
}[archs]

cmake_opts = f"'CMAKE_OSX_ARCHITECTURES': '{';'.join(archs)}', "
cmake_opts += f"'CMAKE_Fortran_FLAGS_INIT': '{' '.join(cpu_flags)}'"
native_profile = f"""\
include(default)
[settings]
arch={conan_arch}
os.version={deployment_target}
build_type=Release
[conf]
tools.build:skip_test=True
tools.cmake.cmaketoolchain:generator=Ninja Multi-Config
tools.build:cflags+={cpu_flags}
tools.build:cxxflags+={cpu_flags}
tools.cmake.cmaketoolchain:extra_variables*={{{cmake_opts}}}
"""
cross_profile = native_profile
cross_profile += f"""\
tools.build.cross_building:can_run={can_run}
tools.cmake.cmaketoolchain:system_name="Darwin"
"""

cross = not can_run
profile = cross_profile if cross else native_profile
Path("cibw.profile").write_text(profile)
print(profile)

opts = dict(shell=True, check=True)
run("conan install . -pr:h ./cibw.profile --build=missing", **opts)
