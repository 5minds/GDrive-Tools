import setuptools

setuptools.setup(
  name="gdrive-tools",
  version="0.0.1",
  author="Robin Palkovits",
  author_email="robin.palkovits@5minds.de",
  description="A collection of usefull tools to interact with the google drive/google docs api",
  packages=setuptools.find_packages(),
  classifiers=[
      "Programming Language :: Python :: 3",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
  ],
  python_requires='>=3.6',
)
