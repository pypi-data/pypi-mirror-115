# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.
setup(
    name='pick3letters',
    version='1.0.0',
    description='Convert hex strings and magnet links to poetry or prose.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/seanlynch/pick3letters',  # Optional
    author='Sean R. Lynch',
    author_email='seanl@literati.org',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='bittorrent',
    packages=find_packages(),  # Required
    python_requires='>=3.6, <4',

    # executes the function `main` from this package when invoked:
    entry_points={  # Optional
        'console_scripts': [
            'pick3letters=pick3letters.pick3letters:main',
        ],
    },
)
