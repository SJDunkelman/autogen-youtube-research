# AutoGen: YouTube research

## Set up
### Getting Autogenstudio running
Install autogenstudio with a conda environment as shown [here](https://autogen-studio.com/)
1. git clone ___
2. cd auto-gen-youtube-research
3. $ conda activate autogenstudio
4. $ export OPENAI_API_KEY=sk-...
5. $ autogenstudio ui
6. Go to the localhost site given in the terminal for autogenstudio

### Adding the YouTube research skills
You can then go to the Build tab and then Skills section. Add the skills you want from the /skills directory:
- youtube_stats: Get the channel stats from a youtube account username. This also returns the channel ID which is needed to get recent videos
- youtube_videos: Get the title and URL for most recent videos from a channel. Uses the channel_id from youtube_stats.
- download_video: Download the audio for a youtube video which can then be transcribed
- youtube_transcription: Transcribe the audio from a youtube video using a local version of Whisper (MUST ALSO INCLUDE download_video skill)
- transcribe_api: Transcribe the audio from a youtube video using an API for Whisper (MUST ALSO INCLUDE download_video skill)

Note: If you run into memory errors when running Whisper locally (it may say "exit code 137") then use the API version in transcribe_api. Make sure you also provide an API key using "export WHISPER_API_KEY=..." before opening up autogenstudio.


## Google Sheets integration
Go to Google Cloud Console
-> Create a new project
-> In your project, go to “APIs & Services” > “Dashboard”
-> Click “+ ENABLE APIS AND SERVICES”
-> Search for “Google Sheets API” and enable it
-> In “APIs & Services”, go to “Credentials”
-> Click “Create Credentials” > “Service account”
-> Fill in the fields and click “Create”
-> Assign the service account the role "Editor" so that it has permissions to access Google Sheets
-> Go to the service account, and under “Keys”, click “Add Key” > “Create new key” > “JSON”
-> Open the downloaded .JSON file and copy the contents

In the JSON you will see a field called "client_email". You must go to the spreadsheet you wish to upload to and share to this email with permissions to edit.

The upload_dict_to_google_sheet skill in upload_to_gsheets.py takes spreadsheet_id as an argument. You can get this from the URL of the spreadsheet from the middle of the URL:
https://docs.google.com/spreadsheets/d/<COPY THIS ID>/edit?=...

When you copy the "upload_dict_to_google_sheet" function from skills/upload_to_gsheets.py file, make sure to paste this key into where it says "creds_json = "
There is an example commented out to show you, delete this when copying into autogen studio.

## Troubleshooting / FAQ

Some notes of why something might not be working:
- The skill must be saved with the same name as the function in the code e.g. for skills/youtube_stats.py the skill must be saved as "get_channel_stats"
- When you make a change to a skill you must then delete and re-add it for the agent in your existing workflows AS WELL as delete and re-add it for the agent template
- When testing in the playground you must create a new session with your workflow, changes will not update to existing sessions
