# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

import json
import youtube_dl
import os
from dotenv import load_dotenv

load_dotenv()


bookmarks_file_path = os.getenv("BOOKMARKS_FILE_PATH")
downloads_path = os.getenv("DOWNLOADS_PATH")
bookmarks_folder_name = os.getenv("BOOKMARKS_FOLDER_NAME")

ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': f'{downloads_path.removesuffix("/")}/%(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}



def download_audio(url: str) -> None:

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def main() -> None:

    with open(bookmarks_file_path, "r", encoding="utf-8") as f:
        json_data = json.loads(f.read())

    for item in json_data["roots"]["bookmark_bar"]["children"]:
        if not (item["type"] == "folder" and item["name"] == bookmarks_folder_name):
            continue
        for child in item["children"]:
            if child["type"] == "url":
                download_audio(child["url"])



if __name__ == '__main__':
    main()