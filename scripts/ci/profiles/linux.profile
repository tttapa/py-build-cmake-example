[conf]
tools.build:cflags+=["-fdiagnostics-color"]
tools.build:cxxflags+=["-fdiagnostics-color"]
tools.build:exelinkflags+=["-flto=auto", "-static-libstdc++", "-static-libgcc"]
tools.build:sharedlinkflags+=["-flto=auto", "-static-libstdc++", "-static-libgcc"]
tools.cmake.cmaketoolchain:generator=Ninja Multi-Config
