import sys
from setuptools import setup
from pathlib import Path

CURRENT_DIR = Path(__file__).parent
sys.path.insert(0, str(CURRENT_DIR))


def get_long_description() -> str:
    return (CURRENT_DIR / "README.md").read_text(encoding="utf8")


setup(
    name="lpip",
    version="1.0.7",
    description="Offline package manager for Python",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/alexbourg/LocalPIP",
    author="Alex BOURG",
    author_email="alex.bourg@outlook.com",
    license="MIT",
    keywords=["localpip", "lpip", "python",
              "offline", "package manager", "anaconda"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: Microsoft :: Windows",
    ],
    packages=["lpip"],
    install_requires=['requests', 'bs4', 'pypac'],
    entry_points={
        "console_scripts": [
            "localpip = lpip.__main__:main",
            "lpip = lpip.__main__:main",
        ],
    },
)
