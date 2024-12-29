import streamlit as st
import yt_dlp as youtube_dl

def download_video(url, option='highest_resolution'):
    try:
        options = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': 'downloads/%(title)s.%(ext)s',  # Path to save the video
        }

        # Check if the option is 4k, otherwise download in highest resolution
        if option == '4k':
            options['format'] = 'bestvideo[height=2160]+bestaudio/best[height=2160]/best'

        with youtube_dl.YoutubeDL(options) as ydl:
            ydl.download([url])

        st.success("Download complete!")

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

def main():
    st.title("YouTube 4K Video Downloader")
    
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
