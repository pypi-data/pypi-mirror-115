from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pytest-win32consoletitle',
    version='0.1.2',
    author='Maciej Nowak',
    url='https://github.com/Novakov/pytest_win32consoletitle',
    description='Pytest progress in console title (Win32 only)',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=('tests',)),
    # the following makes a plugin available to pytest
    entry_points={'pytest11': ['pytest_win32consoletitle = pytest_win32consoletitle.plugin']},
    # custom PyPI classifier for pytest plugins
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'Operating System :: Microsoft :: Windows',
    ]
)
