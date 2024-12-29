import streamlit as st
import yt_dlp as youtube_dl

def download_video(url, option='highest_resolution'):
    try:
        # Define options for yt-dlp based on the user's choice
        options = {
            'outtmpl': 'downloads/%(title)s.%(ext)s',  # Path to save the file
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

        # Download video/audio using yt-dlp
        with youtube_dl.YoutubeDL(options) as ydl:
            ydl.download([url])

        st.success("Download complete!")

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
