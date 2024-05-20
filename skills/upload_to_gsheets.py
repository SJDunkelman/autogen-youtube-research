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
    # Inline service account credentials
    creds_json = {'type': 'service_account',
                  'project_id': 'gsheets-test-423314',
                  'private_key_id': '4050ff779f17931c857e5966093e504d9f13a45d',
                  'private_key': '-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCsRErW9h/R79qS\njcbGh/P2C7HuNnxdB3oceMjbwVJ0AOuTreizFbv9yFycdoyBrO6XlxEWJyu3R2nI\nn6aqdxM+yKlJofv0qpFcP2DdLwrzwsyrimLkUukCFcohYLtmiwlhKlLrVEwc/5tp\n/OyRq5p5Aus4nAZKdUDIqLZq3w5Xfj5tOM6c4sqdPlxmFoDsDXY8e+uJitHxPB3N\nLHrRM019L5Vp9zLYKVQVNdxxvjT8HkEbaUAHZvMW38LUUcLQbrhGZEAoQJ87SMKe\n619/X3uySz+tZVhq1GrlRcx0Pio0U7yHFyY8nsiOm79syeQ1g2teovcJvIukvXcu\nRxaoYfSHAgMBAAECggEACCyk3H/kiBUK6yZBtJZPz3D66hHd0Su4FmM2moE9zj8b\nN8vF1FGsIrztqT52TUBoyoz+KUlhIGQJ17kqji9gnI3voEOR7d8/Ttu7oD63Xi/P\nf+ztCB157Mr553q1d4ZbeboptEXnniOCX7onw6gbY7HJDIJ+SVsT4J9rKbWrF0SL\nYzURMKneOJ5mWtnfDxRCCU0wuVZzVEW6QRlzd86tULoaJh3pBo5BG1sdeEHnD+xx\nl0b3XXUNk4buV1rpNfdUDyXMIp/230v7QriM1/RUcAkj3YOaYYV9g4Tae5261tlZ\nnkV817u0Fn+NU0yHYM4XjBF+NWAOx6vPGNl6jIwqKQKBgQDYpGNezVjGsDydPSQy\n+LFV8q7bG8Bw7UqFjoO0Gx9BnJWtCB+TU0cXe1jbf2n0T8T1RCVq1gMso5rXxCDt\nijaqYxgNSyHdXLPwsn+b4AJPnolANi7fzfKYmokreNPmjYUTQvEOuZXQ+ks+0UcG\noyasTo7RrQL4BzzUX9ZKQCPmAwKBgQDLkBchOubVYCSy+shCOup7NGEkWoZ7RkC3\n9qqQZRCIKEpEv959q9IwVRLOvJdc/lUCM0BqpjB525KRSeAjNILkTRna445sUZHA\neQ+LRlzqnYYZ9y4bVdP3KIVPdaEfKQInhAgDNTvm5ihGU4GEJVtdbmCn/VepxQOc\n1kW2fxeCLQKBgA6MU4P9RDXrhdaFUZX+r2H3LxjVr0GmHbgETwHcRGgSjNaW0hAB\nqqeACAKNdt8KME7MKbsX7hSkU/SjXha1jmA40VerMPX9kLPcOMeN7nnMSqk+Oj2b\nRexLjGSX85rq7AHUH/3+JnpnJIBua1edwy4VBHA+LxHa4pHccbaAwihjAoGALWLP\nBWWwmdp51D398GZaaWXgUs6sNUgQnfOtS8x8xx7UkEeHP9XTY1tUeiuqQ92g7oCm\n2CB9pm3CXApwoujOVkCqhxc9ZgE50gQr5w2lIdpFT/zAlu+n9u9d6b18Uwo9pLnX\nX3+6/1xJloR/2ArMOCSoAEyIAx4eFBXiLTJg93ECgYAmVzVhl53QWKMSxbSP1VEa\ncEpd0afRuhq09fMbWpE7Zm0v85/TmO+OdWQbOIlmOyc9LQbZSLQqYGfph6GR5xAH\nUQuzFo+XeRbXQe9wy6VfbVgKNqIUXhu2Wh5tEUEDacm+4doZT7gD63e+MwTFjl8U\nGBYBbFBtFzbbxQr4y/yrNQ==\n-----END PRIVATE KEY-----\n',
                  'client_email': 'test-993@gsheets-test-423314.iam.gserviceaccount.com',
                  'client_id': '114660017083480479301',
                  'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
                  'token_uri': 'https://oauth2.googleapis.com/token',
                  'auth_provider_x509_cert_url': 'https://www.googleapis.com/oauth2/v1/certs',
                  'client_x509_cert_url': 'https://www.googleapis.com/robot/v1/metadata/x509/test-993%40gsheets-test-423314.iam.gserviceaccount.com',
                  'universe_domain': 'googleapis.com'}

    # Set up credentials and client
    scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    credentials = Credentials.from_service_account_info(creds_json, scopes=scopes)
    client = gspread.authorize(credentials)

    # Open the sheet
    sheet = client.open_by_key(spreadsheet_id).worksheet(sheet_name)

    # Create DataFrame from the dictionary
    df = pd.DataFrame(data_dict)

    # Convert DataFrame to list of lists
    data_to_upload = [df.columns.values.tolist()] + df.values.tolist()

    # Upload data
    sheet.update('A1', data_to_upload)
    print(
        f'Successfully uploaded data. Check your Google Sheet: https://docs.google.com/spreadsheets/d/{spreadsheet_id}')


    question = input('What would you like to ask of the image?')

