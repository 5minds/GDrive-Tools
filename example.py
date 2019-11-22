from time import sleep

import gdrive_tools.gdrive_tools as gt
from gdrive_tools.google_filetypes import GoogleFiletypes
from gdrive_tools.google_auth import GoogleAuth

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/documents', 'https://www.googleapis.com/auth/drive']

def main():
  auth = GoogleAuth(SCOPES)
  creds = auth.createCredentials()

  # Create the google drive tools client with your local credentials.
  googleDriveTools = gt.GDriveTools(creds)

  # Create a new Google Document named 'sample' at the path 'simple/test'
  destinationPath = 'simple/test'
  docname = 'sample'
  googleDriveTools.createFile(destinationPath, docname, GoogleFiletypes.DOCUMENT)

  input("""\
There should be a new "simple" folder in your google drive root directory. \
In this folder, you can find the folder named "test" that contains the created document "sample".
Hint: If you currently opened google drive in your browser, you may have to refresh the page to see the \
changes.

Press any key to continue...
""")

  # Move the created document to the 'new/test' directory.
  sourcePath = 'simple/test/sample'
  destinationPath = 'new/test'
  googleDriveTools.moveDocument(sourcePath, destinationPath)

  print("""\
Now you should also find a "new" folder in your google drive root directory. \
This folder also contains a "test" folder which now contains the document \
named "sample".
Hint: You may also have to refresh your browser. \
""")

if __name__ == '__main__':
  main()
