import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="mplatform",
    version="0.9.9",
    author="Minh Phuong BUI",
    author_email="phuong.buiminh00@gmail.com",
    license="MIT",
    license_files="LICENSE",
    description="Quick code support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)