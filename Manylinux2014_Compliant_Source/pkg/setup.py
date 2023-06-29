from setuptools import setup, Extension

import subprocess as sp
import pathlib as pl

import re

version_regex = re.compile(r"^project\(ir2vec VERSION (?P<version>[^)]+)\)$")
llvm_libs_regex = re.compile(
    r"^llvm_map_components_to_libnames\(llvm_libs (?P<libs>[^)]+)\)$"
)

LLVM_LIBS = []
VERSION = ""
DESCRIPTION = ""

with (pl.Path(__file__).parents[2] / "src" / "CMakeLists.txt").open() as f:
    for line in f:
        if not VERSION:
            vmatch = version_regex.match(line)  # Not using walrus because Python3.6
            if vmatch:
                VERSION = vmatch.group("version")
                continue
        if not LLVM_LIBS:
            libmatch = llvm_libs_regex.match(line)
            if libmatch:
                LLVM_LIBS = libmatch.group("libs").split()
                continue
        if VERSION and LLVM_LIBS:
            break

with (pl.Path(__file__).parent / "IR2Vec" / "README.md").open() as f:
    DESCRIPTION = f.read()


def get_llvm_files():
    out = sp.run(["llvm-config", "--libfiles"] + LLVM_LIBS, stdout=sp.PIPE)
    files = out.stdout.decode("utf8").split()
    return files


IR2Vec_core = Extension(
    "IR2Vec.core",
    sources=["IR2Vec/core.cpp"],
    include_dirs=["./IR2Vec"],
    libraries=["z"],
    extra_objects=["/usr/local/lib/libIR2Vec.a"] + get_llvm_files(),
    extra_compile_args=["-v"],
)

setup(
    name="IR2Vec",
    author="Shikhar Jain",
    author_email="cs22mtech02002@iith.ac.in",
    version=VERSION,
    description="given input .ll/.bc generates corresponding IR2Vec embeddings in a file or on stdout",
    long_description=DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/IITH-Compilers/IR2Vec",
    license="BSD 4-Clause",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: C++",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Compilers",
    ],
    ext_modules=[IR2Vec_core],
    packages=["IR2Vec"],
    package_data={"": ["seedEmbeddingVocab-300-llvm12.txt"]},
    include_package_data=True,
)
