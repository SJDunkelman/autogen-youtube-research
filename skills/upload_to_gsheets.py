import gspread
from google.oauth2.service_account import Credentials
import pandas as pd


def upload_dict_to_google_sheet(data_dict: dict, spreadsheet_id: str, sheet_name: str = 'Sheet1') -> None:
    """
    Upload a dictionary to a Google Sheet
    :param data_dict: dict, Dictionary to upload
    :param spreadsheet_id: str, Google Sheets ID
    :param sheet_name: str, Name of the sheet
    :return:
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

    if all(isinstance(value, (int, float, str)) for value in data_dict.values()):
        # Handling scalar values: turning them into a DataFrame with keys as one column and values as another
        data_to_upload = list(data_dict.items())
    else:
        # For non-scalar values: default behavior
        df = pd.DataFrame(data_dict)
        data_to_upload = [df.columns.values.tolist()] + df.values.tolist()

        # Upload data without headers
    sheet.update('A1', data_to_upload, value_input_option='RAW')
    print(
        f'Successfully uploaded data. Check your Google Sheet: https://docs.google.com/spreadsheets/d/{spreadsheet_id}')