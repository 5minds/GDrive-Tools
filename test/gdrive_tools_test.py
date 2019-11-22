import pytest
import time

from gdrive_tools.gdrive_tools import GDriveTools
from gdrive_tools.google_filetypes import GoogleFiletypes
from gdrive_tools.google_auth import GoogleAuth


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/documents',
'https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/presentations']

@pytest.fixture(scope='session')
def gtoolsClient():
  auth = GoogleAuth(SCOPES)
  creds = auth.createCredentials()
  client = GDriveTools(creds)

  return client

@pytest.fixture(scope='session')
def allDirectoriesFromDrive(gtoolsClient: GDriveTools):
 files = gtoolsClient.googleDriveClient \
        .files() \
        .list(
          q="mimeType = 'application/vnd.google-apps.folder' and not trashed",
          fields='files(id, name, mimeType, parents)').execute()

 return files['files']

def test_create_document(gtoolsClient: GDriveTools):
  # Create a simple document using the GDrive tools
  destPath = 'new/document'
  docName = 'testdoc'
  destPathAsList = __getPathListForPath(destPath)
  docid = gtoolsClient.createFile(destPath, docName, GoogleFiletypes.DOCUMENT)

  # Give Google Drive some time to process these changes.
  time.sleep(0.5)

  # Test, if the document was created
  directories, files = __getAllDirectoriesAndFilesFromDrive(gtoolsClient)
  rootId = __getDriveRootId(gtoolsClient)
  dirTree = __buildDirectoryListForPath(directories, destPathAsList, rootId)

  createdDocumentParentId = gtoolsClient.googleDriveClient.files().get(fileId=docid, fields='parents').execute().get('parents')[0]

  # Check if the document was created in the correct subdirectory
  assert createdDocumentParentId == dirTree[-1].get('id'), 'The Created Document was not in the correct subdirectory'

  # Check, if the directory tree matches the input path:
  for curDirectory, curDirTreeEntry in zip(destPathAsList, dirTree):
    assert curDirectory == curDirTreeEntry.get('name')

def __getAllDirectoriesAndFilesFromDrive(gtoolsClient: GDriveTools):
   files = gtoolsClient.googleDriveClient \
        .files() \
        .list(q="not trashed", fields='files(id, name, mimeType, parents)').execute()

   return __orderDirectoriesAndFiles(files['files'])


def __orderDirectoriesAndFiles(filesToOrder):
    directories = []
    files = []

    for currentFile in filesToOrder:
      if currentFile['mimeType'] == 'application/vnd.google-apps.folder':
        directories.append(currentFile)
      else:
        files.append(currentFile)

    return directories, files

def __buildDirectoryListForPath(directoryList, targetPath, rootParentId):
    dirTree = []
    # Search the target in the root directory.
    # TODO: This should not actually be necessary here.
    # See, if this can be refactored.
    startDir = None
    for curDir in directoryList:
      if (curDir['name'] == targetPath[0] and rootParentId in curDir['parents']):
        startDir = curDir
        break

    # If the first directory could not be found,
    # we can return an empty list here since all directories
    # have to be created.
    if startDir is None:
      return []

    dirTree.append(startDir)
    lastId = startDir['id']

    # Recursively build the directory tree, containing all ids:
    for curTargetDir in targetPath:

      # Search for the directory whose parent is the last directory
      for cur in directoryList:
        if cur['name'] == curTargetDir and lastId in cur['parents']:
          lastId = cur['id']
          dirTree.append(cur)
          break

    return dirTree


def __getDriveRootId(gdriveToolsClient: GDriveTools):
  rootDrive = gdriveToolsClient.googleDriveClient.files().get(fileId='root', fields="id").execute()
  return rootDrive.get('id')

def __getPathListForPath(sourcePath):
  pathList = sourcePath.split('/')
  return pathList if pathList[0] != '' else pathList[1:]
