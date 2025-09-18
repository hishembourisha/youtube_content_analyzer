import yt_dlp
import re
import streamlit as st
from utils.path_utils import OutputPaths, DOWNLOADED_VIDEO

print("IMPORTED VIDEO PATH", DOWNLOADED_VIDEO)

class YouTubeVideoDownloader:
    def __init__(self):
        OutputPaths.ensure_dirs()  # make sure the video dir exists

    def is_youtube_url(self, url):
        pattern = r"^(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+$"
        return re.match(pattern, url) is not None

    def download_video(self, url, output_path=DOWNLOADED_VIDEO):
        """
        Downloads a YouTube video to the given output_path.
        Defaults to outputs/video/downloaded_video.mp4.
        """
        print("OUTPUT_PATH", output_path)
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
            'outtmpl': output_path,  
            'merge_output_format': 'mp4',
            'noplaylist': True,
            'quiet': False
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            return output_path
        except Exception as e:
            st.error(f"Error during video download: {e}")
            return None


if __name__ == "__main__":
    video_url = input("Enter YouTube video URL: ")
    downloader = YouTubeVideoDownloader()
    if downloader.is_youtube_url(video_url):
        path = downloader.download_video(video_url)
        print(f"Video downloaded to: {path}")
    else:
        print("Invalid YouTube URL")
