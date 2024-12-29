import streamlit as st
import yt_dlp
import os
from pathlib import Path
import shutil

import warnings
warnings.filterwarnings("ignore", message="missing ScriptRunContext!")


# Function to download YouTube video
def download_youtube_video(url, resolution="best", output_path="downloads"):
    # Define download options based on resolution
    if resolution == "4K":
        format_option = "bestvideo[height=2160]+bestaudio/best[height=2160]"
    elif resolution == "1080p":
        format_option = "bestvideo[height=1080]+bestaudio/best[height=1080]"
    elif resolution == "720p":
        format_option = "bestvideo[height=720]+bestaudio/best[height=720]"
    else:
        format_option = "bestvideo+bestaudio/best"

    options = {
        "format": format_option,
        "outtmpl": f"{output_path}/%(title)s.%(ext)s"
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([url])

# Streamlit UI setup
st.title("YouTube Video Downloader (4K and Other Resolutions)")
st.write("Enter a YouTube video URL and select the desired resolution to download.")

# User input for YouTube URL
video_url = st.text_input("Enter YouTube Video URL")

# Resolution selection
resolution = st.selectbox("Select Resolution", ["4K", "1080p", "720p", "Best Available"])

# Create a download folder if it doesn't exist
download_dir = "downloads"
Path(download_dir).mkdir(parents=True, exist_ok=True)

# Action when the 'Download' button is clicked
if st.button("Download Video"):
    if video_url:
        with st.spinner("Downloading... Please wait."):
            try:
                download_youtube_video(video_url, resolution=resolution, output_path=download_dir)
                st.success(f"Download complete! The video has been saved in {download_dir}.")
                
                # Provide a download link
                video_title = video_url.split("v=")[-1]
                video_path = f"{download_dir}/{video_title}.mp4"

                if os.path.exists(video_path):
                    with open(video_path, "rb") as file:
                        st.download_button(
                            label="Download Video",
                            data=file,
                            file_name=f"{video_title}.mp4",
                            mime="video/mp4"
                        )
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a valid YouTube video URL.")

# Footer
st.write("Made with ❤️ by YourName")
