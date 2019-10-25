from pathlib import Path

class DocumentCreator():
  def __init__(self, googleDriveClient, googleDocsClient):
    self.__googleDriveClient = googleDriveClient
    self.__googleDocsClient = googleDocsClient

  def createFile(self,
    teamClipBoardId: str,
    destination, documentName: str, type):

    directoriesFromClipboard = self.__getAllDirectoriesFromClipboard(teamClipBoardId)
    directoryTreeForFile = self.__buildDirectoryListForPath(directoriesFromClipboard, destination, teamClipBoardId)

    targetDirectoryId = directoryTreeForFile[-1] if len(directoryTreeForFile) > 0 else teamClipBoardId
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

  def __getAllDirectoriesFromClipboard(self, clipboardId):
    files = self.__googleDriveClient \
      .files() \
      .list(
        q="mimeType = 'application/vnd.google-apps.folder'",
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

    createdDirectory = self.__googleDriveClient.files().create(body=metadata, fields='id').execute()
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
                                  fields='id, parents').execute()
