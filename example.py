import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from time import sleep

import src.gdrive_tools as gt
from src.google_filetypes import GoogleFiletypes

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/documents',
'https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/presentations']

def main():
  creds = getCredentials()

  # Create the google drive tools client with your local credentials.
  googleDriveTools = gt.GDriveTools(creds)

  # Create a new Google Document named 'sample' at the path 'simple/test'
  sharedDriveName = 'GDriveTools_Test'
  destinationPath = 'GDriveTools_Test/simple/test'
  docname = 'sample'
  googleDriveTools.createFile(destinationPath, docname, GoogleFiletypes.DOCUMENT)

  # Give Google Drive some time to process the changes
  sleep(1)

  # Move the created document to the 'new/test' directory.
  sourcePath = 'GDriveTools_Test/simple/test/sample'
  destinationPath = 'new/test'
  googleDriveTools.moveDocument(sourcePath, destinationPath)

def getCredentials():
  creds = None
  # The file token.pickle stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists('token.pickle'):
      with open('token.pickle', 'rb') as token:
          creds = pickle.load(token)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
      if creds and creds.expired and creds.refresh_token:
          creds.refresh(Request())
      else:
          flow = InstalledAppFlow.from_client_secrets_file(
              'credentials.json', SCOPES)
          creds = flow.run_local_server(port=0)
      # Save the credentials for the next run
      with open('token.pickle', 'wb') as token:
          pickle.dump(creds, token)

  docService = build('docs', 'v1', credentials=creds)
  drvService = build('drive', 'v3', credentials=creds)

  return creds

if __name__ == '__main__':
  main()
