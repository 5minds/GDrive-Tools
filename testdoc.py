import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import src.gdrive_tools as gt

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/documents',
'https://www.googleapis.com/auth/drive']

def main():
  docService, drvService = createServices()
  googleDriveTools = gt.GDriveTools(drvService, docService)

  clipboardId = '0ALjbkdGck0cgUk9PVA'
  dest = ['Testi', 'Test']

  googleDriveTools.createFile(clipboardId, dest, 'bla', None)

def createServices():
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

  return docService, drvService

if __name__ == '__main__':
  main()
