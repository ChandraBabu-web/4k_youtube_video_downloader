import streamlit as st
from pytube import YouTube

# Streamlit app title
st.title("YouTube 4K Video Downloader")

# Input box for the YouTube video URL
url = st.text_input("Enter the URL of the YouTube video:")

if url:
    try:
        # Create a YouTube object
        yt = YouTube(url)

        # Get the 4K stream (if available)
        stream = yt.streams.filter(res="2160p", progressive=True, file_extension="mp4").first()

        # Check if 4K stream is available
        if stream:
            st.write("Downloading 4K video...")

            # Show the video title
            st.write(f"Title: {yt.title}")

            # Download the video
            stream.download()

            st.success("Video downloaded successfully!")
        else:
            st.error("4K stream is not available for this video.")
    except Exception as e:
        st.error(f"Error: {e}")
