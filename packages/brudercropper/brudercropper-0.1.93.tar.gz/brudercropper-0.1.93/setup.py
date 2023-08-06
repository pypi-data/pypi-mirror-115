import setuptools

with open("README.md", "rb") as fh:
    long_description = fh.read()

setuptools.setup(
    name="brudercropper",
    version="0.1.93",
    author="Niggo",
    description="Croppt Zeug auf 62mm für Bruderlabeldrucker",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=[
        "imutils",
        "numpy",
        "opencv-python",
        "Pillow>=8",
        "pytesseract",
        "python-barcode"
    ],
    classifiers=[
        # "Development Status :: 3 - Alpha"
        "Programming Language :: Python :: 3",
        # "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
    entry_points={
        'console_scripts': [
            'brudercrop = brudercropper.__main__:main',
        ],
    }
)