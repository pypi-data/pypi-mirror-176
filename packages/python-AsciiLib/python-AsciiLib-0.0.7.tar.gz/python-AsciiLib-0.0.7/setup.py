from setuptools import setup, find_packages

VERSION = '0.0.7'
DESCRIPTION = 'An ascii art package'
with open('README.md') as fh:
    LONG_DESCRIPTION = fh.read()

setup(
    name="python-AsciiLib",
    url='https://github.com/HiMeAlex/AsciiLib-Package',
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author="Alexander J.",
    author_email="alexandergrahambell707@gmail.com",
    license='MIT',
    packages=find_packages(),
    install_requires=['opencv-python', 'numpy', 'pillow'],
    keywords='ascii',
    classifiers= [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3"
    ]
)