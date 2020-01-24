"""
This example creates a simple document inside a provided subdirectory.
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

  # The destinationPath variable stores the path to the target directory,
  # which will contain the created document.
  destinationPath = 'simple/test'

  # The name of the document is a dedicated parameter of the createFile
  # method. Because of this, we store the name in a dedicated variable.
  docname = 'sample'

  # Creates the document with the given name inside the passed path.
  # Since we want to create a simple GoogleDocument (aka a _Word Document_), we need
  # to specify it with the document type on the last parameter.
  googleDriveTools.createFile(destinationPath, docname, GoogleFiletypes.DOCUMENT)

if __name__ == '__main__':
  main()
