import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

class GoogleAuth():
  def __init__(self, scopes, credentialsPath='credentials.json', tokenPath=".", tokenFileName="token.pickle"):
    self.__scopes = scopes
    self.__credentialsPath = credentialsPath
    self.__tokenPath = tokenPath
    self.__tokenFileName = tokenFileName

  def createCredentials(self):
    creds = None

    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    tokenPath = f'{self.__tokenPath}/{self.__tokenFileName}'
    if os.path.exists(tokenPath):
      with open(tokenPath, 'rb') as token:
        creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
      if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
      else:
        flow = InstalledAppFlow.from_client_secrets_file(self.__credentialsPath, self.__scopes)
        creds = flow.run_local_server(port=0)

      # Save the credentials for the next run
      with open(tokenPath, 'wb') as token:
        pickle.dump(creds, token)

    return creds
