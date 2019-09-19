import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name="CADET",
    version="0.1",
    author="William Heymann",
    author_email="w.heymann@fz-juelich.de",
    description="CADET is a python interface to the CADET chromatography simulator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/modsim/CADET-Match",
    packages=setuptools.find_packages(),
    install_requires=[
          'addict',
          'numpy',
          'h5py'
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
) 
