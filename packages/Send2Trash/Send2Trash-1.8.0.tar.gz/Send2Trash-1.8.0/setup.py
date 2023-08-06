from setuptools import setup

CLASSIFIERS = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: BSD License",
    "Operating System :: MacOS :: MacOS X",
    "Operating System :: Microsoft :: Windows",
    "Operating System :: POSIX",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Topic :: Desktop Environment :: File Managers",
]

with open("README.rst", "rt") as f1, open("CHANGES.rst", "rt") as f2:
    LONG_DESCRIPTION = f1.read() + "\n\n" + f2.read()

setup(
    name="Send2Trash",
    version="1.8.0",
    author="Andrew Senetar",
    author_email="arsenetar@voltaicideas.net",
    packages=["send2trash"],
    scripts=[],
    test_suite="tests",
    url="https://github.com/arsenetar/send2trash",
    license="BSD License",
    description="Send file to trash natively under Mac OS X, Windows and Linux.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/x-rst",
    classifiers=CLASSIFIERS,
    extras_require={
        "win32": ['pywin32; sys_platform == "win32"'],
        "objc": ['pyobjc-framework-Cocoa; sys_platform == "darwin"'],
        "nativeLib": [
            'pywin32; sys_platform == "win32"',
            'pyobjc-framework-Cocoa; sys_platform == "darwin"',
        ],
    },
    project_urls={"Bug Reports": "https://github.com/arsenetar/send2trash/issues"},
    entry_points={"console_scripts": ["send2trash=send2trash.__main__:main"]},
)
