import gspread
from google.oauth2.service_account import Credentials
import pandas as pd


def read_google_sheet_to_dataframe(spreadsheet_id: str, sheet_name: str = 'Sheet1') -> pd.DataFrame:
    """
    Read data from a Google Sheet into a pandas DataFrame.
    :param spreadsheet_id: str, Google Sheets ID
    :param sheet_name: str, Name of the sheet
    :return: pd.DataFrame
    """
    # Inline service account credentials REPLACE WITH YOUR OWN
    creds_json = {
        "type": "service_account",
        "project_id": "your-project-id",
        "private_key_id": "your-private-key-id",
        "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
        "client_email": "your-service-account-email@your-project-id.iam.gserviceaccount.com",
        "client_id": "your-client-id",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account-email%40your-project-id.iam.gserviceaccount.com"
    }

    # Set up credentials and client
    scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    credentials = Credentials.from_service_account_info(creds_json, scopes=scopes)
    client = gspread.authorize(credentials)

    # Open the sheet
    sheet = client.open_by_key(spreadsheet_id).worksheet(sheet_name)

    # Get all the records in the sheet
    data = sheet.get_all_records()  # Returns a list of dictionaries

    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(data)

    return df
