
from distutils.core import setup
from setuptools import find_packages
import broadreduce

setup(
    name='broadreduce',
    packages=find_packages(),
    version=broadreduce.__version__,
    license='BSD-3-Clause',
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
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)