"""
This is a small example which demonstrates, how a document can be
shared with a given user.
"""
from time import sleep

import gdrive_tools.gdrive_tools as gt
import gdrive_tools.google_auth as ga
from gdrive_tools.google_accesslevel import GoogleAccessLevel

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

  # The first thing we need is the id of the document which we want to share.
  documentId = '1eG50VUf1zKC2GsnzgZQ5z8VhgX7FtUDwgej-bvl0Tlo'

  # With a simple call to the grantApproval() method, we can share a document
  # with a given user.
  # We also want include some nice words in the notification message, which is send
  # by google to the given email address.
  googleDriveTools.grantApproval(documentId, 'testuser124444444444444445@gmail.com',
                                 GoogleAccessLevel.READ, emailText='Here is a nice document which you should read.')

if __name__ == '__main__':
  main()
