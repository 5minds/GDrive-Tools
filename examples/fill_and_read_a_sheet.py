"""
This example demonstrates, how a google sheet can be filled
with data from a dictionary.
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

  # Firstly, we want to create a new google sheet to work with.
  # Notice how we can obtain the id of the created sheet from the creatFile()
  # method.
  groceryListId = googleDriveTools.createFile('test', 'groceries', GoogleFiletypes.SHEET, firstSheetName='Groceries')

  # Give the Api some time to process our request.
  sleep(1)

  # Now we want to define some data, which we want to insert into our
  # created sheet.
  sheetData = [{
    'item': 'Banana',
    'amount': 2
  }, {
    'item': 'Apple',
    'amount': 4
  }]

  # After defining the data, we can fill our created sheet with it.
  # We only need to provide the id of the destination sheet.
  googleDriveTools.fillSheet(groceryListId, sheetData, sheetTableName='Groceries')

  # Again, give the api some time.
  sleep(1)

  # Now we want to read our groceries using the GDrive_Tools library.
  # Since our data is also stored in the 'Groceries' Sheet, we need to specify it.
  groceryList = googleDriveTools.readSheet(groceryListId, 'Groceries')

  # List all our groceries.
  for currentItem in groceryList:
    print(f"Item: {currentItem['item']}\tAmount: {currentItem['amount']}")

if __name__ == '__main__':
  main()
