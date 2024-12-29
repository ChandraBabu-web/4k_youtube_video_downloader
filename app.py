import streamlit as st
import yt_dlp as youtube_dl

def download_video(url, option='highest_resolution'):
    try:
        # Default options for yt-dlp
        options = {
            'format': 'bestvideo+bestaudio/best',  # Default best video and audio
            'outtmpl': 'downloads/%(title)s.%(ext)s',  # Path to save the video
        }

        # Check if the user selects 4K
        if option == '4k':
            options['format'] = 'bestvideo[height=2160]+bestaudio/best[height=2160]/best'

        # You can also handle other cases like audio and lowest resolution if needed
        if option == 'audio':
            options['format'] = 'bestaudio/best'
        elif option == 'lowest_resolution':
            options['format'] = 'worstvideo+bestaudio/best'

        # Download the video with yt-dlp
        with youtube_dl.YoutubeDL(options) as ydl:
            ydl.download([url])

        st.success("Download complete!")

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

def main():
    st.title("YouTube Video Downloader (4K Supported)")

    url = st.text_input("Enter the YouTube video URL")
    
    # Dropdown for selecting download option
    option = st.selectbox(
        'Select type of download',
        ('audio', 'highest_resolution', 'lowest_resolution', '4k')
    )

    # Trigger the download action
    if url:
        if st.button("Download Video"):
            download_video(url, option)

        if st.button("View Video"):
            st.video(url)

if __name__ == "__main__":
    main()
