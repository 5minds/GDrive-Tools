"""
This example creates and copies a document inside a shared drive.
"""

from time import sleep

import gdrive_tools.gdrive_tools as gt
import gdrive_tools.google_auth as ga
from gdrive_tools.google_filetypes import GoogleFiletypes

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/documents', 'https://www.googleapis.com/auth/drive']

def main():

  # Create the google auth wrapper, which wraps the authentication
  # process. You only need to specify the needed scopes here.
  auth = ga.GoogleAuth(SCOPES)

  # Obtain the credentials, after the authentication process finished.
  creds = auth.createCredentials()

  # Create the google drive tools client with your local credentials.
  googleDriveTools = gt.GDriveTools(creds)

  # In the first step, we want to create a new document, stored on
  # the 'simple/test' path.
  destinationPath = f'simple/test'
  docname = 'sample'
  googleDriveTools.createFile(destinationPath, docname, GoogleFiletypes.DOCUMENT)

  # Let the google drive api some time to process our request.
  sleep(0.5)

  # Now, we want to copy our created document to the 'copies/document/newName'
  # path.

  # At first, we want to specify the name of our shared drive, which
  # contains the file that we want to copy inside this shared drive.
  sharedDriveName = 'GDriveTools_Test'

  # Now we need to specify the sourcePath of the document, which we
  # want to copy. The path is described with with the usual syntax.
  # Remember to specify the name of the shared drive which contains the
  # document first.
  # The last portion of the path marks the document's name.
  sourcePath = f'{sharedDriveName}/simple/test/sample'

  # Now, we have to specify the destination path. This is the path,
  # where the document should be copied to.
  # Since we want to work on our shared drive with the given name, we need
  # to specify the name at the first part of the path definition.
  # Also notice how we can actually change the name of the document.
  # The name of the copied document is always declared in the last section of the path.
  destinationPath = f'{sharedDriveName}/copies/newDocumentTitle'

  # Now we can simply call the copyDocument() - method with the defined
  # arguments.
  googleDriveTools.copyDocument(sourcePath, destinationPath)

if __name__ == '__main__':
  main()
