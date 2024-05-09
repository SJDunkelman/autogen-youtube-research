import autogen
from ast import literal_eval
from dotenv import load_dotenv
import os

import requests
import json
from skills.youtube_transcription import download_youtube_audio

load_dotenv()

"""
Agent setup
"""

config_list_llama3 = literal_eval(open("config_llama3.json", "r").read())
llm_config_llama3 = {"config_list": config_list_llama3}

config_list_codellama = literal_eval(open("config_codellama.json", "r").read())
llm_config_codellama = {"config_list": config_list_codellama}

assistant = autogen.AssistantAgent(
    name="Assistant",
    llm_config=llm_config_llama3
)

coder = autogen.AssistantAgent(
    name="Coder",
    llm_config=llm_config_codellama
)

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={"work_dir": "web"},
    llm_config=llm_config_llama3,
    system_message="""Reply TERMINATE if the task has been solved at full satisfaction.
Otherwise, reply CONTINUE, or the reason why the task is not solved yet."""
)

"""
Skills
"""


def transcribe_youtube_link(youtube_url: str) -> str:
    api_url = "https://transcribe.whisperapi.com"
    headers = {
        "Authorization": f"Bearer {os.getenv('WHISPER_API_KEY')}",
    }

    file_name = download_youtube_audio(youtube_url)

    files = {'file': open(file_name, 'rb')}
    data = {
        "fileType": "mp3",
        "task": "transcribe",
        "language": "en"
    }
    response = requests.post(api_url, headers=headers, files=files, data=data)
    response = json.loads(response.text)
    return response['text']


task = """
Write a python script to output numbers 1 to 100 and then the user_proxy agent should run the script
"""

user_proxy.initiate_chat(coder, message=task)
