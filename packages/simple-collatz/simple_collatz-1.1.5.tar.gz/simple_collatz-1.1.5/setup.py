import sys

from setuptools import find_packages, setup

assert sys.version_info >= (3, 9, 5), "simple_collatz requires Python 3.9.5+"
from pathlib import Path  # noqa E402

CURRENT_DIR = Path(__file__).parent
sys.path.insert(0, str(CURRENT_DIR))  # for setuptools.build_meta


def get_long_description() -> str:
    return (
        (CURRENT_DIR / "README.md").read_text(encoding="utf8")
        + "\n\n"
        + (CURRENT_DIR / "CHANGES.md").read_text(encoding="utf8")
    )


setup(
    name="simple_collatz",
    version="1.1.5",
    description="A simple collatz conjecture generator.",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Manas Mengle",
    url="https://github.com/appcreatorguy/collatz",
    project_urls={
        "Changelog": "https://github.com/appcreatorguy/collatz/blob/master/CHANGES.md"
    },
    license="MIT",
    py_modules=["_simple_collatz_version"],
    keywords="simple_collatz collatz discrete math number theory",
    packages=find_packages(),
    python_requires=">=3.9.5",
    zip_safe=False,
    install_requires=[
        "matplotlib>=3.4.2",
        "appdirs>=1.4.4",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Education",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Visualization",
    ],
    entry_points={"console_scripts": ["simple_collatz=simple_collatz:main"]},
)
