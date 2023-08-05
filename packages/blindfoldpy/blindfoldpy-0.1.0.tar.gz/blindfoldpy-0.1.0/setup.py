import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="blindfoldpy",
    version="0.1.0",
    author="iwishiwasaneagle",
    author_email="jh.ewers@gmail.com",
    description="Don't use this. Use the real blindfold. I'm just trying to spite the author who's a close friend of mine.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/iwishiwasaneagle/blindfold.py",
    packages=setuptools.find_packages(where="src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    package_dir={"": "src"},
    entry_points={
        "console_scripts": ['blindfoldpy=blindfoldpy.main:main'],
    }
)