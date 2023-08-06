import sys
from setuptools import setup, find_packages
from pathlib import Path

CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 10)

if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write(
        """
==========================
Unsupported Python version
==========================
Python version >= 3.10 required. Please update your Python version.
""".format(
            *(REQUIRED_PYTHON + CURRENT_PYTHON)
        )
    )
    sys.exit(1)

requires = [
    "openpyxl>=3.0.10",
    "xlwt>=1.3.0",
    "pydantic>=1.9.0"
]

about = {}
here = Path(__file__).parent.resolve()

version_file = here / "easyio" / "__version__.py"
readme_file = here / "README.md"


exec(version_file.read_text('utf-8'), about)
readme = readme_file.read_text('utf-8')

setup(
    name=about["__title__"],
    version=about["__version__"],
    description=about["__description__"],
    long_description=readme,
    long_description_content_type="text/markdown",
    author=about["__author__"],
    author_email=about["__author_email__"],
    url=about["__url__"],
    packages=find_packages(),
    python_requires=">=3.10,<4",
    install_requires=requires,
    setup_requires=requires,
    license=about["__license__"],
    zip_safe=False,
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3 :: Only",
    ],
    project_urls={
        "Source": "https://github.com/iiicebearrr/easy-io",
    },
)
