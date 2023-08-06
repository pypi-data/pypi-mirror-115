import pathlib
import setuptools
from pybind11.setup_helpers import Pybind11Extension, build_ext
from pybind11 import get_cmake_dir

# The directory containing this file
HERE = pathlib.Path(__file__).parent
__version__ = "1.0.1"
# The text of the README file
README = (HERE / "README.md").read_text()

ext_modules = [
    Pybind11Extension(
        'kmp_utils',
        ['kmp_utils/kmp_utils.cpp'],
        define_macros = [('VERSION_INFO', __version__)]
    )
]

# This call to setup() does all the work
setuptools.setup(
    name="kmp_utils",
    version=__version__,
    description="Implementation of KMP algorithm and simple generalizations.",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Algorithms Path",
    author_email="support@algorithmspath.com",
    url='http://pypi.python.org/pypi/kmp_utils/',
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    ext_modules = ext_modules,
    cmdclass={'build_ext' : build_ext},
    # packages=setuptools.find_packages(),
    # package_data={'example' : ['kmp_utils/example.cpython-38-x86_64-linux-gnu.so']},
    include_package_data=True,
    install_requires=["pybind11"],
    python_requires='>=3'
)
