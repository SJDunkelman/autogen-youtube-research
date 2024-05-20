# AutoGen: YouTube research

## Set up
Install autogenstudio with a conda environment as shown (here)[https://autogen-studio.com/]
> git clone ___
> cd auto-gen-youtube-research
> $ conda activate autogenstudio
> $ autogenstudio ui
> Go to the localhost site given in the terminal for autogenstudio

You can then go to the Build tab and then Skills section. Add the skills

### Google Sheets
Go to Google Cloud Console
-> API & Services
-> "+ Create new service"
-> Search for Google Sheets API
-> Enable

-> Back to Services & API page
-> Click on API tab
-> Create API Key
-> Select JSON key
-> Open the downloaded .JSON file and copy the contents

When you copy the "upload_dict_to_google_sheet" function from skills/upload_to_gsheets.py file, make sure to paste this key into where it says "creds_json = "
There is an example commented out to show you, delete this when copying into autogen studio 

