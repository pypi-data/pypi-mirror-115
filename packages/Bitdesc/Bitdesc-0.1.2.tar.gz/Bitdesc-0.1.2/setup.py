from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="Bitdesc",
    version='0.1.2',
    description="Bio-Inspired Texture Descriptor",
    py_modules=["ClassBit", "Channel_Split", "BiT", "Biodiversity", "Taxonomic"],
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["opencv-python", "Scipy", "Numpy", "Pillow"],
    extras_require = {
        "dev":[
            "pytest>=3.6",
        ],
    },
    find_packages = find_packages(),
    url="https://github.com/stevetmat/BioInspiredFDesc",
    author="Steve Ataky & Alessandro Koerich",
    author_email="steve.ataky@nca.ufma.br",
    keywords='texture descriptor invariant bio-inspired texture-classification',
    licence='BSD',
    include_package_data=True
)