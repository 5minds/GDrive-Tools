from time import sleep

import src.gdrive_tools as gt
from src.google_filetypes import GoogleFiletypes
from src.google_auth import GoogleAuth

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/documents',
'https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/presentations']

def main():
  auth = GoogleAuth(SCOPES)
  creds = auth.createCredentials()

  # Create the google drive tools client with your local credentials.
  googleDriveTools = gt.GDriveTools(creds)

  # Create a new Google Document named 'sample' at the path 'simple/test'
  destinationPath = 'GDriveTools_Test/simple/test'
  docname = 'sample'
  googleDriveTools.createFile(destinationPath, docname, GoogleFiletypes.DOCUMENT)

  # Give Google Drive some time to process the changes
  sleep(1)

  # Move the created document to the 'new/test' directory.
  sourcePath = 'GDriveTools_Test/simple/test/sample'
  destinationPath = 'new/test'
  googleDriveTools.moveDocument(sourcePath, destinationPath)

if __name__ == '__main__':
  main()
