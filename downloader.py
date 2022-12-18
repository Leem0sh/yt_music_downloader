# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

import json
import youtube_dl
import os
from dotenv import load_dotenv

load_dotenv()


bookmarks_path = os.environ.get("BOOKMARKS_PATH")
downloads_path = os.environ.get("DOWNLOADS_PATH")
bookmarks_name = os.environ.get("BOOKMARKS_NAME")

def download_audio(url: str) -> None:
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{downloads_path}/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])




if __name__ == '__main__':

    with open(bookmarks_path, "r") as f:
        bookmarks = f.read()
        json_data = json.loads(bookmarks)
        for item in json_data["roots"]["bookmark_bar"]["children"]:
            if item["type"] == "folder" and item["name"] == bookmarks_name:
                for child in item["children"]:
                    if child["type"] == "url":
                        download_audio(child["url"])
