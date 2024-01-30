# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
#

import os
from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain


class FBX2glTFConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    requires = (
        ("boost/1.78.0"),
        ("libiconv/1.17"),
        ("zlib/1.2.11"),
        ("libxml2/2.9.12"),
        ("fmt/5.3.0"),
    )
    generators = "CMakeDeps"

    def configure(self):
        if (
            self.settings.compiler == "gcc"
            and self.settings.compiler.libcxx == "libstdc++"
        ):
            raise Exception(
                "Rerun 'conan install' with argument: '-s compiler.libcxx=libstdc++11'"
            )
        if self.settings.os.subsystem == "catalyst":
            if not hasattr(self.settings, "os.subsystem.ios_version"):
                self.output.warn("os.subsystem.ios_version is not defined. Assuming a default value.")
                self.settings.os.subsystem.ios_version = "13.0"

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["FBXSDK_SDKS"] = os.getenv("FBXSDK_SDKS", "sdk")
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
