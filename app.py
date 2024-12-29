import streamlit as st
from pytube import YouTube
from pytube.exceptions import PytubeError

def main():
    path = st.text_input('Enter URL of any youtube video')
    option = st.selectbox(
        'Select type of download',
        ('audio', 'highest_resolution', 'lowest_resolution', '4k')
    )

    if path:
        try:
            video_object = YouTube(path)
            st.write("Title of Video: " + str(video_object.title))
            st.write("Number of Views: " + str(video_object.views))

            if option == 'audio':
                st.write("Downloading audio...")
                video_object.streams.get_audio_only().download()
                st.write("Audio download complete.")

            elif option == 'highest_resolution':
                st.write("Downloading highest resolution...")
                video_object.streams.get_highest_resolution().download()
                st.write("Download complete.")

            elif option == 'lowest_resolution':
                st.write("Downloading lowest resolution...")
                video_object.streams.get_lowest_resolution().download()
                st.write("Download complete.")

            elif option == '4k':
                # Select 4K resolution video stream (2160p)
                st.write("Downloading 4K resolution...")
                video_object.streams.filter(res="2160p", progressive=True).first().download()
                st.write("4K video download complete.")

        except PytubeError as e:
            st.error(f"Error: {str(e)}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")

    if st.button("View Video"):
        st.video(path)

if __name__ == '__main__':
    main()
