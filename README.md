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


Example:

```python
sharedDriveName = 'MySharedDrive'
path = 'target/directory'
documentName = 'documentToCreate'

googleDriveToolsClient\
  .createFile(sharedDriveName,
    path,
    documentName,
    GoogleFiletypes.DOCUMENT)
```



