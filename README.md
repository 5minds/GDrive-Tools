# GDrive Tools

## Goal of this Project

The automated managing of google drive documents is quite laborious.
This is because of the Google Drive API v3, which does not allow to pass
a directory path of a document that should be created.
Instead, documents are only ordered using the parents node id.

Since its more common for us to _think_ in directory trees, its
easier to specify a full path.

This Project offers methods to manage document by providing _real_ path
specifications rather then a child - parent relationship for each document.
(For example: Its way more convenient to specify a path by writing something
like _path/to/my/document_ than searching for the parent Id of the document).

## Usage

The usage of this library should be straight forward.

Firstly, you have to create a `GDriveToolsClient` - Object which only needs your
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

## Capabilities

With the GDrive tools library, you can do the following things:

### Create a new Document

A new document can be created using the `createFile()` method. The created
document will be placed inside a directory with the given path. Any nonexisting
directories will be created.

_Directories which are placed in the drives trash folder will be ignored._

The following
parameters are needed:

* `destination(str)`: Full path, where the document should be moved to.
  All directories are delimited by a simple slash (`/`).
  If the document should be created inside a shared drive, the name of the shared
  drive should be provided first. (Its basically seen as the root directory.)
  Example:
  ```
  MySharedDrive/subdirectory/anotherSubdirectory
  ```

  If you want to create a new document on your local drive, the first
  entry is also the first sub folder. For example:
  ```
  subdirectory/anotherSubdirectory
  ```

* `documentName(str)`: Name of the Document that should be created.
* `fileType(int)`: Type of the document. Currently, the following types are
  supported:
    * `GoogleFiletypes.DOCUMENT`: Google Docs file
    * `GoogleFiletypes.SHEET`: Google Sheets file
    * `GoogleFiletypes.SLIDE`: Google Slides file
* There are also different keyword arguments which can be used, to modify the
  created documents. The following ones are currently supported:
    * `sheetTableName(str): Specify a custom name which should be used for the first Sheet,
      when creating a new sheet.

The return value is the id of the created document.

### Move a Document

A document can be moved from one directory to another, either inside your
local, shared drive or between shared drives, using the `moveDocument()` method.

The following parameters are needed.

* `sourcePath(str)`: Full path, of the document, which should be moved.
  All directories are delimited by a simple slash (`/`).
  If the document should be moved inside or to a shared drive, the name of the shared
  drive should be provided first.
  Example:
  ```
  MySharedDrive/subdirectory/anotherSubdirectory/targetFilename
  ```

  If you want to create a new document on your local drive, the first
  entry is seen as the first subdirectory. Example:
  ```
  subdirectory/anotherSubdirectory/targetFilename
  ```
* `destinationPath(str)`: The target path where the document should be
  moved to. The described syntax of the `sourcePath` parameter also applies here.

The method returns the id of the moved document.

### Copy a Document

Its also possible to copy a document into another directory and/or to another
team drive. This can
be done by using the `copyDocument()` - Method.

The following Parameters are required:

* `sourcePath(str)`: The full source path of the document that should be copied.
  The syntax is equivalent to the syntax of the `moveDocument()` Method.
* `destinationPath(str)`: The path which defines where the copy of the source
  document should be created.

The method returns the id of the copied document.

### Fill a Sheet

If you want to fill a google documents sheet, you can use the `fillSheet()` Method.
**Keep in mind that any existing data inside the sheet will be overwritten.**

The method takes the following parameters:

* `sheetId(str)`: The Id of the sheet which should be filled.
* `data(List[dict])` The data which should be inserted into the sheet as a list
  of dictionaries.
  The Columns are therefore defined by the keys of the dictionaries, whereas
  all dictionaries must have the same keys.
* `[sheetTableName(str)='']` The name of the table inside the given sheet, where the data should
  be inserted.
  If the table does not exists, a `ValueError` will be thrown.

### Read Data from a Sheet

With the `readSheet()` method you can read the data from a sheet. The method
will return a list of dictionaries which contains the sheet's rows and columns.

The target sheet has to contain only a single table without extra cells. Its assumed
that the first row defines the names of the columns.
However, its possible to specify a custom range in the A1 notation. This range
defines, which data should be read.

The method takes the following parameters:
 * `sheetId(str)`: The id of the target sheet.
 * `sheetName(str)`: The name of the table/sheet which should be used.
 * `[a1Range(str)]`: A custom range which points to the data which should be read.
    Since the sheet name is already passed with the sheetName property, you can't
    also specify it here.
* `[placeholder(dict)]`: A dictionary which contains placeholder values for each
  column, which is not defined.
  _A column is also considered as "not defined" if the value is an empty string._

### Grant Permissions

You can grant Permissions to a given document by using the `grandApproval()` Method.

The method takes the following parameters:
* `sheetId(str)`: The Id of the document, that should be shared with a user.
* `email(str)`: The EMail address of the user, which should gain access to the document.
* `accessLevel(GoogleAccessLevel)`: The type of permission which should be grant to the
  user.
* `[grantType(GoogleGrantTypes)]`: You can set a custom grant type by using this property.
  _Please note that if you are using the grant type `DOMAIN`, the `email` parameter has to contain the name of the target domain._
* `[emailText(str)='']`: An optional text which should be embedded inside the
  email notification which is automatically send by google, if a user gained access to a document.

### Read all Files from a Directory

If you want to retrieve a list of all files in a given directory, you can use
the `readDirectory()` method. As the name suggests, this method returns a
list of all files which are included in this directory.


The return value of this method is a directory, which has the following keys:
  * `directory_id`: ID of the directory
  * `files`: List of files, found inside this directory.

Whereas each file - directory has the following properties:
  * `name`: Name of the file
  * `id`: ID of the file
  * `type`: filetype


The method only needs one parameter:
* `path(str)`: The path of the directory which should be read. The syntax is the
  same as in the `moveDocument()` or `copyDocument()` methods.

This method returns the dictionary, which is described above.

A _ValueError_ is thrown, if the given directory does
not exists.

### Return the Id of a Document

If you just want to know the Id of a document which is saved in a given path,
you can query it by using the `getDocumentId()` method.

This method only takes one parameter:

Args:
  * `path(str)`: The path to the document, whose Id should be
    returned.

Returns:
  The Id of the document, which is stored on the provided path, or an empty
  string, if the document does not exists.

## Example

You can test the library using the given `example.py` script.

### Enable the Google Drive and Docs Api and Download the Client Configuration

In order for the script to work, its required to have a valid `credentials.json` file.
The example script only needs an activated GoogleDrive and GoogleSheets api.

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

To run the example script in the virtual environnement which was created by pipenv, you can
run `pipenv run python example.py`.
