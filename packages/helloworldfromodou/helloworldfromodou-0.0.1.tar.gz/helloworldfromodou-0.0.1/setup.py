from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='helloworldfromodou',
    version='0.0.1',
    description='Say Hello world',
    url="https://github.com/Modiao/setup_pytest",
    author="Modou Diao",
    author_email="diaomodou06@gmail.com",
    py_modules=["helloworldfromodou"],
    package_dir={'': 'src'},
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU Affero General Public License v3",
    ],
    install_requires=[
        "blessings == 1.7", 
    ],
    extras_require = {
        "dev": [
            "pytest>=3.7",
            "check-manifest",
            "twine",
        ],
    },
     
)