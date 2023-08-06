import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="clname",
    version="1.0.0",
    author="Stefan Lepperdinger",
    author_email="lepperdinger.stefan@gmail.com",
    description="Cleans filenames to make them shell-friendly",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lepperdinger/clname",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
    ],
    py_modules=['clname'],
    entry_points={'console_scripts': ['clname=clname:main']},
    python_requires=">=3.6",
)
