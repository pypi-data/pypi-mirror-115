from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='helloworld-nmoore',
    version='0.0.1',
    description='Print out the genereric hellow world statmet,\
     or add a name to it!',
    py_modules=["helloworld"],
    package_dir={'': 'src'},

    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],

    long_description = long_description,
    long_description_content_type="text/markdown",

    # requirements for package, this means you dont need a requirements.txt file
    # requirements.txt used for appls on machines you control, uses fixed verison numbers, generated with pip freeze > requirements.txt
    install_requires = [
        "blessings ~= 1.7", #terminal coloring package
    ],


    #extra require is used for option requirements, for example a dev version
    extras_require = { 
        "dev":[
            "pytest>=3.7",
        ],

    },

    url="https://github.com/xxxxx",
    author="Nathan Moore",
    author_email="nathanmichaelmoore@gmail.com",


)