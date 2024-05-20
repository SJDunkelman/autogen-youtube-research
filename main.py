import autogen
from ast import literal_eval
from dotenv import load_dotenv
import os
from typing import Annotated

from config import PROJECT_ROOT_DIR
import requests
import json
from skills.youtube_transcription import download_youtube_audio, chunk_audio

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

summarisation_agent = autogen.ConversableAgent(
    "summariser",
    system_message="Your task is to summarise transcriptions of YouTube videos to give a very concise description of the content.",
    llm_config=llm_config_llama3,
    code_execution_config=False,  # Turn off code execution, by default it is off.
    function_map=None,  # No registered functions, by default it is None.
    human_input_mode="NEVER",  # Never ask for human input.
)

# concierge = autogen.ConversableAgent(
#     "concierge",
#     system_message="Your task is to get the URL of the video the user wants to transcribe.",
#     llm_config=llm_config_llama3,
#     human_input_mode="ALWAYS",
# )

# coder = autogen.AssistantAgent(
#     name="Coder",
#     llm_config=llm_config_codellama
# )

# user_proxy = autogen.UserProxyAgent(
#     name="user_proxy",
#     human_input_mode="NEVER",
#     max_consecutive_auto_reply=10,
#     is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
#     code_execution_config={"work_dir": "web"},
#     llm_config=llm_config_llama3,
#     system_message="""Reply TERMINATE if the task has been solved at full satisfaction.
# Otherwise, reply CONTINUE, or the reason why the task is not solved yet."""
# )

user_proxy = autogen.ConversableAgent(
    name="User",
    is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
    human_input_mode="ALWAYS",
)

"""
Skills
"""


def transcribe_youtube_link(youtube_url: Annotated[str, "The YouTube URL"]) -> str:
    api_url = "https://transcribe.whisperapi.com"
    headers = {
        "Authorization": f"Bearer {os.getenv('WHISPER_API_KEY')}",
    }

    file_name = download_youtube_audio(youtube_url)
    # chunks = chunk_audio(file_name)

    files = {'file': open(PROJECT_ROOT_DIR / "input" / file_name, 'rb')}
    data = {
        "fileType": "mp3",
        "task": "transcribe",
        "language": "en"
    }
    response = requests.post(api_url, headers=headers, files=files, data=data)
    response = json.loads(response.text)
    transcription = response['text']

    with open(PROJECT_ROOT_DIR / "output" / file_name, 'w') as f:
        f.write(transcription)
    return transcription


assistant.register_for_llm(name="transcribe_youtube_link", description="Get the transcription for a YouTube video via the link")(transcribe_youtube_link)

user_proxy.register_for_execution(name="transcribe_youtube_link")(transcribe_youtube_link)

if __name__ == "__main__":
    youtube_channel = input("Enter the YouTube channel URL: ")
    user_proxy.initiate_chat(assistant, message=f"The task is to research the following YouTube channel: {youtube_channel}")
