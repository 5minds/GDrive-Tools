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

  # For the demonstation of the readDirectory() method, we want to
  # create a file called 'sample' in the 'simple/test' directory on our
  # local drive first.
  destinationPath = 'simple/test'
  docname = 'sample'
  googleDriveTools.createFile(destinationPath, docname, GoogleFiletypes.DOCUMENT)

  # Now we want to read the content of the 'simple/test' directory.
  directoryContent = googleDriveTools.readDirectory(destinationPath)

  print(f"The directory has the following ID: {directoryContent['directory_id']}")
  print("The following files are currently stored inside the directory:\n")
  for currentFile in directoryContent['files']:
    print(f"Filename:\t{currentFile['name']}")
    print(f"File Id:\t{currentFile['id']}")
    print(f"Mime Type:\t{currentFile['type']}\n")

if __name__ == '__main__':
  main()
