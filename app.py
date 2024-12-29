import streamlit as st
import yt_dlp as youtube_dl
import tempfile
import os

def download_video(url, option='highest_resolution'):
    try:
        # Define options for yt-dlp based on the user's choice
        options = {
            'format': 'bestvideo+bestaudio/best',  # Default to best quality video and audio
            'quiet': True,  # Suppress unnecessary output
        }

        # Set the format selection based on the option chosen
        if option == 'audio':
            options['format'] = 'bestaudio/best'  # Only download the best audio
        elif option == 'highest_resolution':
            options['format'] = 'bestvideo+bestaudio/best'  # Highest resolution video with audio
        elif option == 'lowest_resolution':
            options['format'] = 'worstvideo+bestaudio/worst'  # Lowest resolution video with audio
        elif option == '4k':
            options['format'] = 'bestvideo[height=2160]+bestaudio/best[height=2160]/best'  # 4K video

        # Create a temporary file to store the downloaded video
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_filename = tmp_file.name

        options['outtmpl'] = tmp_filename  # Set the temporary file path

        # Download video/audio using yt-dlp
        with youtube_dl.YoutubeDL(options) as ydl:
            ydl.download([url])

        # After download, give user the option to download the file directly
        with open(tmp_filename, "rb") as f:
            file_data = f.read()

        st.download_button(
            label="Download Video/Audio",
            data=file_data,
            file_name=f"{options['outtmpl'].split('/')[-1]}.mp4",  # Change the extension as needed
            mime="video/mp4"  # Adjust MIME type based on file type (audio or video)
        )

        # Clean up the temporary file
        os.remove(tmp_filename)

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

def main():
    st.title("YouTube Video Downloader")

    url = st.text_input("Enter the YouTube video URL")

    option = st.selectbox(
        'Select type of download',
        ('audio', 'highest_resolution', 'lowest_resolution', '4k')
    )

    if url:
        if st.button("Download Video"):
            download_video(url, option)

        if st.button("View Video"):
            st.video(url)

if __name__ == "__main__":
    main()
