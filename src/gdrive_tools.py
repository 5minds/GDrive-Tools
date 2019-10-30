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
  def __init__(self, googleDriveClient, googleDocsClient):
    self.__googleDriveClient = googleDriveClient
    self.__googleDocsClient = googleDocsClient

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
    sharedDriveName: str,
    destination,
    documentName: str, type):

    # Try to obtain the id of the drive with the given name
    sharedDriveId = self.__getIdOfSharedDrive(sharedDriveName)
    directoriesFromClipboard = self.__getAllDirectoriesFromClipboard(sharedDriveId)

    directoryTreeForFile = self.__buildDirectoryListForPath(directoriesFromClipboard, destination, sharedDriveId)

    targetDirectoryId = directoryTreeForFile[-1].get('id') if len(directoryTreeForFile) > 0 else sharedDriveId
    if len(directoryTreeForFile) < len(destination):
      existingDirectoryNames = [curDir['name'] for curDir in directoryTreeForFile]
      missingDirectoryNames = [curDir for curDir in destination if curDir not in existingDirectoryNames]

      targetDirectoryId = self.__createMissingDirectories(missingDirectoryNames, targetDirectoryId)

    # Create the Document
    createdDocumentId = self.__createDocument(documentName)

    # After creation, we have to move the document to the target
    # directory. This is because there seems to be no way to directly attach
    # a newly created document to a parent.
    self.__moveDocumentToDirectory(createdDocumentId, targetDirectoryId)

  def __getIdOfSharedDrive(self, driveName):
    drives = self.__googleDriveClient.drives()\
      .list(fields='drives')\
      .execute()\
      .get('drives')

    idForDrive = ""

    for currentDrive in drives:
      if currentDrive['name'] == driveName:
        idForDrive = currentDrive['id']
        break

    if not idForDrive:
      raise ValueError(f'Could not find a drive with name "{driveName}"')

    return idForDrive

  def __getAllDirectoriesFromClipboard(self, clipboardId):
    files = self.__googleDriveClient \
      .files() \
      .list(
        q="mimeType = 'application/vnd.google-apps.folder' and not trashed",
        corpora='drive',
        supportsAllDrives=True,
        driveId=clipboardId,
        includeItemsFromAllDrives=True,
        fields='files(id, name, mimeType, parents)').execute()

    return files['files']

  def __buildDirectoryListForPath(self, directoryList, targetPath, baseId):
    dirTree = []
    # Search the target in the root directory.
    # TODO: This should not actually be necessary here.
    # See, if this can be refactored.
    startDir = None
    for curDir in directoryList:
      if (curDir['name'] == targetPath[0] and baseId in curDir['parents']):
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

  def __createMissingDirectories(self, missingDirectories, firstParentId):
    lastDirectoryId = firstParentId
    for currentDirectory in missingDirectories:
      lastDirectoryId = self.__createDirectory(currentDirectory, lastDirectoryId)

    return lastDirectoryId

  def __createDirectory(self, directoryName, parentId):
    metadata = {
      'name': directoryName,
      'mimeType': 'application/vnd.google-apps.folder',
      'parents': [parentId]
    }

    createdDirectory = self.__googleDriveClient.files().create(body=metadata, supportsTeamDrives=True, fields='id').execute()
    return createdDirectory.get('id')


  def __createDocument(self, documentName):
    requestBody = {
      'title': documentName
    }
    createdDocument = self.__googleDocsClient.documents().create(body=requestBody, fields='documentId').execute()

    return createdDocument.get('documentId')

  def __moveDocumentToDirectory(self, documentIdToMove, targetDirectoryId):
    fetchedDocument = self.__googleDriveClient.files().get(fileId=documentIdToMove, fields='parents').execute()
    previous_parents = ",".join(fetchedDocument.get('parents'))
    self.__googleDriveClient.files().update(fileId=documentIdToMove,
                                  addParents=targetDirectoryId,
                                  removeParents=previous_parents,
                                  supportsAllDrives=True,
                                  fields='id, parents').execute()
