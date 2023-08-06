
from distutils.core import setup
from setuptools import find_packages
import broadreduce
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='broadreduce',
    packages=find_packages(),
    version=broadreduce.__version__,
    license='BSD-3-Clause',
    long_description=long_description,
    long_description_content_type='text/markdown',
    description = 'Spectra reduction pipeline for broad-slit spectroscopy (Tuned for Keck LRIS).',
    author="Harrison Souchereau",
    author_email='harrison.souchereau@yale.edu',
    url='https://github.com/HSouch/broadreduce',
    keywords='galaxies spectra spectroscopy',
    install_requires=[
        'numpy',
        'photutils',
        'astropy',
        'pebble',
        'tqdm',
        "scipy"
    ],
    scripts=["bin/slitfinder.py", "bin/z_widget.py"],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)