import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
        name="mutation_load",
        version="1.0.3",
        author="Timo_Järvinen",
        author_email="neville160@gmail.com",
        description="VCF permutation tool",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/jarvint12/mutation_load",
        packages=setuptools.find_packages(),
        classifiers=(
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: BSD License",
            "Operating System :: POSIX :: Linux",
        ),
)

