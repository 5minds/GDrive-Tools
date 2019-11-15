# GDrive Tools

## Goal of this Project

The automated managing of google drive documents is quite laborious.
This is because of the Google Drive API v3, which does not allow to pass
a directory path of a document that should be created.
Instead, documents are only ordered using the parents node id.

Since its more common for us to _think_ in directory trees, its
more convenient for us to specify a full path.

This Project offers a method to create and move documents to a real path
instead of just providing the parents node Id (as its needed by the
Google Drive Api).

## Usage

The usage of this library should be straight forward.
Firstly, you have to create a library client which only needs your
credentials. This can be archived like so:

```Python
import src.gdrive_tools as gt

# Read your Credentials. This is documented on the google drive api.
credentials = get_credentials()

# Create the api client and pass the read credentials.
googleDriveToolsClient = gt.GoogleDriveTools(credentials)
```

### Create a new Document

A new document can be created using the `createFile()` method. The created
document will be placed inside a directory with the given path. Any nonexisting
directories will be created.

_Directories which are placed in the drives trash folder will be ignored._

The following
parameters are needed:

* `sharedDriveName(str)`: Name of the shared drive, where the document
  should be created in.
* `destination(str)`: Full path, where the document should be moved to. The root
  is equivalent to the root directory of the shared drive with the given name.
  All directories are delimited by a simple slash (`/`).
* `documentName(str)`: Name of the Document that should be created.
* `fileType(int)`: Type of the document. Currently, the following types are
  supported:
    * `GoogleFiletypes.DOCUMENT`: Google Docs file
    * `GoogleFiletypes.SHEET`: Google Sheets file
    * `GoogleFiletypes.SLIDE`: Google Slides file


## Example

You can test the library using the given `example.py` script.

### Enable the Google Drive and Docs Api and Download the Client Configuration

In order the script to work you need to have a valid `credentials.json` file,
which contains your google drive credentials.
For the example, you only need to activate the Google Drive and Google Sheets
api with your account.

1. Navigate to https://developers.google.com/drive/api/v3/quickstart/python
2. Click on the _Enable the Drive Api_ Button
3. Navigate to https://developers.google.com/docs/api/quickstart/python
4. Click on the _Enable the Docs Api_ Button
5. Click on _Download Client Configuration_ Button
6. Move the downloaded `credentials.json` file to this directory.

### Install the Dependencies

There are two ways how to install the dependencies.

#### Using Pip

If you use pip natively, you can simply install the dependencies from
the `requirements.txt` file using `pip install -r requirements.txt`.

#### Using Pipenv

This project's dependencies can also be managed with Pipenv. To use Pipenv, make
sure its installed on your system (if not it can be done so by executing `pip install pipenv`).
Then you can install the dependencies using `pipenv install`.

To run the example script in the virtual environnement, created by pipenv, you can
run `pipenv run python example.py`.
