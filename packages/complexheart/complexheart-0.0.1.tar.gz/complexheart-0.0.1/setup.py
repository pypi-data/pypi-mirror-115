import setuptools

setuptools.setup(
    name="complexheart",
    version="0.0.1",
    author="Unay Santisteban",
    author_email='usantisteban@othercode.es',
    url="https://github.com/ComplexHeart/py-sdk",
    description="Provide a set of useful classes and tools to ease the adoption of Domain-Driven Design into your Python project.",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    keywords=['python', 'ddd', 'hexagonal architecture'],
    packages=setuptools.find_packages(exclude=("tests",)),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
    install_requires=[]
)
