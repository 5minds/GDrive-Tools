import os
import setuptools

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setuptools.setup(
  name="gdrive-tools",
  version="v1.1.0",
  author="Robin Palkovits",
  author_email="robin.palkovits@5minds.de",
  license="mit",
  license_file="LICENSE",
  description="A collection of usefull tools to interact with the google drive/google docs api.",
  long_description=read('README.md'),
  long_description_content_type="text/markdown",
  url="https://github.com/5minds/GDrive-Tools",
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
