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
import gdrive_tools.gdrive_tools as gt
import gdrive_tools.google_auth as ga
from gdrive_tools.google_filetypes import GoogleFiletypes

SCOPES = [
  'https://www.googleapis.com/auth/drive',
  'https://www.googleapis.com/auth/documents',
  'https://www.googleapis.com/auth/spreadsheets',
  'https://www.googleapis.com/auth/presentations'
  ]

# Create a google auth object which wraps the authentication on the google
# drive api.
auth = ga.GoogleAuth(SCOPES)
credentials = auth.createCredentials()

# Create the api client and pass the read credentials.
googleDriveToolsClient = gt.GoogleDriveTools(credentials)
```

If the client object was created, you can use the offered methods.

### Create a new Document

A new document can be created using the `createFile()` method. The created
document will be placed inside a directory with the given path. Any nonexisting
directories will be created.

_Directories which are placed in the drives trash folder will be ignored._

The following
parameters are needed:

* `destination(str)`: Full path, where the document should be moved to.
  All directories are delimited by a simple slash (`/`).
  If the document should be created in a shared drive, the name of the shared
  drive should be provided first. (Its basically seen as the root directory.)
  Example:
  ```
  MySharedDrive/subdirectory/anotherSubdirectory
  ```

  If you want to create a new document on your local drive, the first
  entry is also the first sub folder. Example:
  ```
  subdirectory/anotherSubdirectory
  ```

* `documentName(str)`: Name of the Document that should be created.
* `fileType(int)`: Type of the document. Currently, the following types are
  supported:
    * `GoogleFiletypes.DOCUMENT`: Google Docs file
    * `GoogleFiletypes.SHEET`: Google Sheets file
    * `GoogleFiletypes.SLIDE`: Google Slides file


The method returns the id of the created document.

### Move a Document

A document can be moved from one directory to another, either inside your
local or a shared drive, using the `moveDocument()` method.

The following parameters are needed.

* `sourcePath(str)`: The full source path of the document that should be moved.
  Full path, where the document should be moved to.
  All directories are delimited by a simple slash (`/`). The last portion
  describes the name of the moved file.
  If the document should be created in a shared drive, the name of the shared
  drive should be provided first. (Its basically seen as the root directory.)
  Example:
  ```
  MySharedDrive/subdirectory/anotherSubdirectory/targetFilename
  ```

  If you want to create a new document on your local drive, the first
  entry is also the first sub folder. Example:
  ```
  subdirectory/anotherSubdirectory/targetFilename
  ```
* `destinationPath(str)`: The target path where the document should be
  moved to. The root point of this path points to the root directory of the
  shared drive with the name, defined by the `sourcePath` parameter.

The method returns the id of the moved document.

### Copy a Document

Its also possible to copy a document into another directory. This can
be archived by using the `copyDocument()` - Method.

The following Parameters are required:

* `sourcePath(str)`: The full source path of the document that should be copied.
  The syntax is equivalent to the syntax of the `moveDocument()` Method.
* `destinationPath(str)`: The path which defines where the copy of the source
  document should be created.

The method returns the id of the copied document.

### Fill a Sheet

If you want to fill an drive sheet, its possible with the `fillSheet()` Method.
Keep in mind that any existing data in the provided sheet will be overwritten.

The method takes the following parameters:

* `sheetId(str)`: The Id of the sheet which should be filled.
* `data(List[dict])` The data which should be inserted into the sheet as a list
  of JSON - Objects.
  The Columns are therefore defined by the keys of the given JSON Objects, whereas
  all JSON Objects in the passed list must have the same keys.
* `[sheetTableName(str)='']` The name of the table inside the given sheet, where the data should
  be inserted.
  If the table does not exists, a `ValueError` will be thrown.

### Read Data from a Sheet

With the `readSheet()` method you can read the data from a sheet. The method
will return a list of dictionaries which contains the sheets rows and columns.

The target sheet has to contain only a single table without extra cells. Its assumed
that the first row defines the names of the columns.
However, its possible to specify a custom range in the A1 notation, where the
table is placed.

The method takes the following parameters:
 * `sheetId(str)`: The id of the target sheet.
 * `sheetName(str)`: The name of the table/sheet which should be used.
 * `[a1Range(str)]`: A custom range which points to the data which should be read.
    Since the sheet name is already passed with the sheetName property, you can't
    also specify it here.
* `[placeholder(dict)]`: A dictionary which contains placeholder values for each
  column, which is not defined. A column is also considered as _not defined_, if
  the value is an empty string.

### Grant Permissions

You can grant Permissions to a given document by using the `grandApproval()` Method.

The method takes the following parameters:
* `sheetId(str)`: The Id of the document, which should be shared with a user.
* `email(str)`: The EMail address of the user, which should gain access to the document.
* `accessLevel(GoogleAccessLevel)`: The type of permission which should be grant to the
  user.
* `[grantType(GoogleGrantTypes)]`: You can set a custom grant type by using this property.
  _Please note that if you are using the grant type `DOMAIN`, the `email` parameter has to contain the name of the target domain._
* `[emailText(str)='']`: An optional text which should be embedded inside the
  notification email.

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
