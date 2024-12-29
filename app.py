import streamlit as st
import yt_dlp as youtube_dl
from moviepy.editor import VideoFileClip, AudioFileClip

def download_video(url, option='highest_resolution'):
    try:
        # Define download options
        options = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': 'downloads/%(title)s.%(ext)s',  # Path to save the video
            'noplaylist': True,  # Don't download playlists
        }

        # Check if the user selected 4K
        if option == '4k':
            options['format'] = 'bestvideo[height=2160]+bestaudio/best[height=2160]/best'
        
        # Other option choices: audio only, lowest resolution, etc.
        if option == 'audio':
            options['format'] = 'bestaudio/best'
        elif option == 'lowest_resolution':
            options['format'] = 'worstvideo+bestaudio/best'

        # Download video and audio separately using yt-dlp
        with youtube_dl.YoutubeDL(options) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_file = ydl.prepare_filename(info_dict).replace('.webm', '.mp4')  # You can handle the file extensions accordingly
            audio_file = ydl.prepare_filename(info_dict).replace('.mp4', '.webm')  # Handle audio format

        # Merge video and audio using moviepy
        video_clip = VideoFileClip(video_file)
        audio_clip = AudioFileClip(audio_file)

        # Set the audio of the video clip
        video_clip = video_clip.set_audio(audio_clip)

        # Output merged video
        output_file = 'downloads/merged_video.mp4'
        video_clip.write_videofile(output_file, codec='libx264', audio_codec='aac')

        st.success("Download and merge complete!")
        st.download_button("Download Merged Video", output_file)

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

def main():
    st.title("YouTube Video Downloader (4K Supported)")

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
