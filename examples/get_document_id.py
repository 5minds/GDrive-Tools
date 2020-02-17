"""
This example returns the Id of a document in a given path.
"""

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

  # For the demonstation of the getDocumentId() method, we want to
  # create a file called 'sample' in the 'simple/test' directory on our
  # local drive first.
  destinationPath = 'simple/test'
  docname = 'sample'
  googleDriveTools.createFile(destinationPath, docname, GoogleFiletypes.DOCUMENT)

  # Now we want to read the content of the 'simple/test' directory.
  # Since this method expects the full path to the document, we need to
  # append the filename to the current path.
  destinationPath = f'{destinationPath}/{docname}'
  documentId = googleDriveTools.getDocumentId(destinationPath)
  print(f'The Id of the document stored in {destinationPath} is: {documentId}')

if __name__ == '__main__':
  main()
