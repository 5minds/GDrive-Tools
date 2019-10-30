import setuptools

setuptools.setup(
  name="google-docs-library",
  version="0.0.1",
  author="Robin Palkovits",
  author_email="robin.palkovits@5minds.de",
  description="Lets the User Create New Documents in Nested Directories",
  packages=setuptools.find_packages(),
  classifiers=[
      "Programming Language :: Python :: 3",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
  ],
  python_requires='>=3.6',
)
