import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tesseract-ocr-data",
    version="1.4",
    author="Suprime",
    license = 'MIT',
    author_email="suprime.sendings@gmail.com",
    description="tesseract-ocr data for projects using it without having to install it.",
    long_description= long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MOBSkuchen/tesseract-ocr-data",
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "tesseract_pack"},
    packages=setuptools.find_packages(where='tesseract_pack'),
    python_requires='>=3.7',
)