"""
This example creates a document in a shared drive and moves it to another one.
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

  # At first, we want to specify the name of our shared drive, which
  # contains the file that we want to move to another shared drive.
  sourceSharedDriveName = 'GDriveTools_Test'

  # Now we need to specify the sourcePath of the document, which we
  # want to move. The path is described with with the usual syntax.
  # Remember to specify the name of the shared drive which contains the
  # document first.
  # The last portion of the path marks the document's name.
  sourcePath = f'{sourceSharedDriveName}/simple/test/sample'

  # Since we want to move our document to another shared drive, we also
  # have to specify its name.
  destinationSharedDriveName = 'GDriveTools_Test2'

  # In the next step, we have to specify the destination path. This is the path,
  # where the document should be moved to.
  # Remember how the name of the target shared drive is always specified first.
  # Also notice how we can actually change the name of the document.
  # The name of the moved document is always declared in the last section of the path.
  destinationPath = f'{destinationSharedDriveName}/moved/newDocumentTitle'

  # Now we can simply call the moveDocument() - method with the defined
  # arguments.
  googleDriveTools.moveDocument(sourcePath, destinationPath)

if __name__ == '__main__':
  main()

