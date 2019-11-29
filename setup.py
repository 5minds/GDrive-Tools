import setuptools

setuptools.setup(
  name="gdrive-tools",
  version="v1.0.0",
  author="Robin Palkovits",
  author_email="robin.palkovits@5minds.de",
  description="A collection of usefull tools to interact with the google drive/google docs api",
  packages=setuptools.find_packages(),
  classifiers=[
      "Programming Language :: Python :: 3",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
  ],
  install_requires=['google-api-python-client',
    'google-auth-httplib2',
    'google-auth-oauthlib'],
  python_requires='>=3.6',
)
