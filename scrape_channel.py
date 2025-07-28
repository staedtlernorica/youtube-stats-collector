from googleapiclient.discovery import build
import os
# from dotenv import load_dotenv
# load_dotenv()  # Load variables from .env into environment
# Access the variables
# api_key = os.getenv("TEST_API_KEY")
api_key = 'AIzaSyDuYrBH-f9PNlnM9MJHaC-Or5skoBpTGCw'

youtube = build('youtube', 'v3', developerKey = api_key)


def get_uploads_id(channel_id = ""):

    #https://stackoverflow.com/a/27872244/6030118
    #get channel's uploads playlist
    channel_info = youtube.channels().list(
    part ="contentDetails",
    id = channel_id).execute()

    uploads_id = channel_info["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    # return channel_info
    return uploads_id