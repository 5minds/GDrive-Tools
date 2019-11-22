from googleapiclient.discovery import build

from .google_filetypes import GoogleFiletypes

class GDriveTools():

  """
  Creates a new instance of the document creator. The identity is
  taken from the provided googleDrive and googleDocs client.

  Args:
    googleDriveClient (any):  Reference to the google drive service, which
                              should be used.

    googleDocsClient (any): Reference to the google document service, which
                              should be used.
  """
  def __init__(self, creds):
    self.__googleDriveClient = build('drive', 'v3', credentials=creds)
    self.__googleDocsClient = build('docs', 'v1', credentials=creds)
    self.__googleSheetsClient = build('sheets', 'v4', credentials=creds)
    self.__googleSlidesClient = build('slides', 'v1', credentials=creds)

  """
  Creates a new file at the given path in the team clipboard with the passed
  id.

  If the given path in the shared clipboard does not exists, the given directories
  will be created.

  Args:
    teamClipboardId (str):  The id of the clipboard, where the document should be
                            created.

    destination (str):      Target, where the new document should be placed.

    documentName (str):     Name of the new document.

    type (int):             Type Identifier which defines the document type that
                            should be created.

  Todo:
    * Parse the Destination from any given input string into a list of directories.
      Currently, it is only supported to provide a list of directories instead of
      a 'real' path as a string.

    * Support all different google docs types:
      At the current state, it is only possible to create google text documents.
      In the final version, it should be possible to create any type of google
      document.
  """
  def createFile(self,
    destination: str,
    documentName: str,
    fileType: GoogleFiletypes):

    # Convert the given Path into a List
    destinationList = self.__getPathListForPath(destination)

    # Try to obtain the id of the drive with the given name
    sharedDriveId = self.__getIdOfSharedDrive(destinationList[0]) if len(destinationList) > 0 else ''
    if sharedDriveId:
      destinationList = destinationList[1:]

    directoriesFromClipboard = self.__getAllDirectoriesFromClipboard(sharedDriveId)

    # If the target directory list is empty, the document should be created
    # inside the root directory.
    if len(destinationList) == 0:
      targetDirectoryId = sharedDriveId

    else:
      directoryTreeForFile = self.__buildDirectoryListForPath(directoriesFromClipboard, destinationList, sharedDriveId)
      targetDirectoryId = self.__searchForTargetDirectory(directoryTreeForFile, sharedDriveId, destinationList)

    # Create the Document
    createdDocumentId = self.__createFile(documentName, fileType)

    # After creation, we have to move the document to the target
    # directory. This is because there seems to be no way to directly attach
    # a newly created document to a parent.
    self.__moveDocumentToDirectory(createdDocumentId, targetDirectoryId)

  def moveDocument(self, sourcePath: str, targetPath: str):
    """
    Moves a document from the given source- to a destination path.

    Args:
      sharedDriveName(str): Name of the Shared drive
      sourcePath(str): The path of the document that should be moved.
      targetPath(str): The path where the document should be moved to.
    """
    sourcePathAsList, sourceFileName = self.__getPathAndFilename(sourcePath)
    targetDirectoryList = self.__getPathListForPath(targetPath)

    driveId, isSharedDrive  = self.__getDriveId(sourcePathAsList[0]) if len(sourcePathAsList) > 0 else ''

    if isSharedDrive:
      sourcePathAsList = sourcePathAsList[1:]

    everythingFromDrive = self.__getAllFilesOfDrive(driveId, isSharedDrive)
    directories, files = self.__orderDirectoriesAndFiles(everythingFromDrive)

    parentDirectoryId = self.__getParentDirectoryId(directories, sourcePathAsList, driveId)
    documentId = self.__findDocumentIdWithParentId(files, sourceFileName, parentDirectoryId)

    if not documentId:
      raise ValueError(f'Document "{sourcePath}" not found!')

    targetDirectoryTree = self.__buildDirectoryListForPath(directories, targetDirectoryList, driveId)
    targetDirectoryId = self.__searchForTargetDirectory(targetDirectoryTree, driveId, targetDirectoryList)

    self.__moveDocumentToDirectory(documentId, targetDirectoryId)

  @property
  def googleDriveClient(self):
    return self.__googleDriveClient

  @property
  def googleDocsClient(self):
    return self.__googleDocsClient

  @property
  def googleSheetsClient(self):
    return self.__googleSheetsClient

  @property
  def googleSlidesClient(self):
    return self.__googleSlidesClient

  def __getDriveId(self, driveName):
    driveId = self.__getIdOfSharedDrive(driveName)

    # If the drive id was not found in the list of shared drives, the id of the local
    # drive will be returned.
    isSharedDrive = driveId != ''
    if not isSharedDrive:
      driveId = self.__getDriveRootId()

    return driveId, isSharedDrive


  def __getIdOfSharedDrive(self, driveName):
    idForDrive = ''
    drives = self.__googleDriveClient.drives()\
      .list(fields='drives')\
      .execute()\
      .get('drives')

    for currentDrive in drives:
      if currentDrive['name'] == driveName:
        idForDrive = currentDrive['id']
        break

    return idForDrive

  def __getDriveRootId(self):
    rootDrive = self.__googleDriveClient.files().get(fileId='root', fields="id").execute()
    return rootDrive.get('id')

  def __getAllDirectoriesFromClipboard(self, clipboardId):
    files = []
    if clipboardId:
      files = self.__googleDriveClient \
        .files() \
        .list(
          q="mimeType = 'application/vnd.google-apps.folder' and not trashed",
          corpora='drive',
          supportsAllDrives=True,
          driveId=clipboardId,
          includeItemsFromAllDrives=True,
          fields='files(id, name, mimeType, parents)').execute()

    else:
      files = self.__googleDriveClient \
        .files() \
        .list(
          q="mimeType = 'application/vnd.google-apps.folder' and not trashed",
          fields='files(id, name, mimeType, parents)').execute()

    return files['files']

  def __getAllFilesOfDrive(self, driveId, useSharedDrive):
    files = []

    if useSharedDrive:
      files = self.__googleDriveClient \
        .files() \
        .list(
          q="not trashed",
          corpora='drive',
          supportsAllDrives=True,
          driveId=driveId,
          includeItemsFromAllDrives=True,
          fields='files(id, name, mimeType, parents)').execute()

    else:
        files = self.__googleDriveClient \
        .files() \
        .list(q="not trashed", fields='files(id, name, mimeType, parents)').execute()

    return files['files']

  def __orderDirectoriesAndFiles(self, filesToOrder):
    directories = []
    files = []

    for currentFile in filesToOrder:
      if currentFile['mimeType'] == 'application/vnd.google-apps.folder':
        directories.append(currentFile)
      else:
        files.append(currentFile)

    return directories, files

  def __buildDirectoryListForPath(self, directoryList, targetPath, rootParentId):
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

  def __searchForTargetDirectory(self, directoryTree, driveId, destinationPath):
    targetDirectoryId = directoryTree[-1].get('id') if len(directoryTree) > 0 else driveId

    if len(directoryTree) < len(destinationPath):
      existingDirectoryNames = [curDir['name'] for curDir in directoryTree]
      missingDirectoryNames = [curDir for curDir in destinationPath if curDir not in existingDirectoryNames]

      targetDirectoryId = self.__createMissingDirectories(missingDirectoryNames, targetDirectoryId)

    return targetDirectoryId

  def __createMissingDirectories(self, missingDirectories, firstParentId):
    lastDirectoryId = firstParentId
    for currentDirectory in missingDirectories:
      lastDirectoryId = self.__createDirectory(currentDirectory, lastDirectoryId)

    return lastDirectoryId

  def __createDirectory(self, directoryName, parentId):
    parents = [parentId] if parentId else []
    metadata = {
      'name': directoryName,
      'mimeType': 'application/vnd.google-apps.folder',
      'parents': parents
    }

    createdDirectory = self.__googleDriveClient.files().create(body=metadata, supportsTeamDrives=True, fields='id').execute()
    return createdDirectory.get('id')


  def __createFile(self, name, filetype):
    createdFileId = ''

    if filetype == GoogleFiletypes.DOCUMENT:
      createdFileId = self.__createDocument(name)

    elif filetype == GoogleFiletypes.SHEET:
      createdFileId = self.__createSheet(name)

    elif filetype == GoogleFiletypes.SLIDE:
      createdFileId = self.__createSlide(name)

    else:
      raise ValueError('The Given Filetype is not valid!')

    return createdFileId

  def __createDocument(self, documentName):
    requestBody = {
      'title': documentName
    }
    createdDocument = self.__googleDocsClient.documents().create(body=requestBody, fields='documentId').execute()

    return createdDocument.get('documentId')

  def __createSheet(self, sheetName):
    requestBody = {
      'properties': {
        'title': sheetName
      }
    }

    createdSpreadsheetId = self.__googleSheetsClient.spreadsheets()\
      .create(body=requestBody, fields='spreadsheetId').execute()

    return createdSpreadsheetId.get('spreadsheetId')

  def __createSlide(self, slideName):
    requestBody = {
      'title': slideName
    }

    presentation = self.__googleSlidesClient.presentations() \
        .create(body=requestBody).execute()

    return presentation.get('presentationId')

  def __findDocumentIdWithParentId(self, listOfDocuments, documentName, parentId):
    documentId = ''
    for currentDocument in listOfDocuments:
      currentDocumentHasTargetName = currentDocument['name'] == documentName
      currentDocumentHasGivenParent = parentId in currentDocument['parents']
      if currentDocumentHasTargetName and currentDocumentHasGivenParent:
        documentId = currentDocument['id']
        break

    return documentId

  def __getParentDirectoryId(self, directories, path, driveId):
    parentDirectoryId = ''
    if len(path) == 0:
      return driveId

    else:
      srcDirectoryTree = self.__buildDirectoryListForPath(directories, path, driveId)
      parentDirectoryId = srcDirectoryTree[-1].get('id') if len(srcDirectoryTree) > 0 else ''

    return parentDirectoryId

  def __moveDocumentToDirectory(self, documentIdToMove, targetDirectoryId):
    fetchedDocument = self.__googleDriveClient.files().get(supportsAllDrives=True, fileId=documentIdToMove, fields='parents').execute()
    previous_parents = ",".join(fetchedDocument.get('parents'))
    self.__googleDriveClient.files().update(fileId=documentIdToMove,
                                  addParents=targetDirectoryId,
                                  removeParents=previous_parents,
                                  supportsAllDrives=True,
                                  fields='id, parents').execute()

  def __getPathListForPath(self, sourcePath):
    pathList = sourcePath.split('/')
    return pathList if pathList[0] != '' else pathList[1:]

  def __getPathAndFilename(self, pathAsString):
    fullPath = self.__getPathListForPath(pathAsString)

    if len(fullPath) == 1:
      return [], fullPath[0]

    return fullPath[:-1], fullPath[-1]
