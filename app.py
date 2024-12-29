import streamlit as st
import yt_dlp as youtube_dl
import tempfile
import os
import ffmpeg

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

        # Create a temporary directory to store the downloaded video/audio files
        with tempfile.TemporaryDirectory() as temp_dir:
            options['outtmpl'] = os.path.join(temp_dir, '%(id)s.%(ext)s')

            # Download video/audio using yt-dlp
            with youtube_dl.YoutubeDL(options) as ydl:
                ydl.download([url])

            # Get the downloaded files' paths
            downloaded_files = [os.path.join(temp_dir, f) for f in os.listdir(temp_dir) if f.endswith(('mp4', 'mkv', 'webm'))]

            # If two videos are downloaded, proceed to merge them
            if len(downloaded_files) >= 2:
                file1 = downloaded_files[0]
                file2 = downloaded_files[1]
                
                # Create a temporary file for the merged output
                output_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4').name
                
                # Perform the merging process with FFmpeg
                ffmpeg.input(file1).output(output_file, vcodec='copy', acodec='copy').run()

                # Optionally, you can apply further manipulations here using ffmpeg filters, like flipping, reversing, etc.
                in1 = ffmpeg.input(file1)
                in2 = ffmpeg.input(file2)
                v1 = in1.video.hflip()
                a1 = in1.audio
                v2 = in2.video.filter('reverse').filter('hue', s=0)
                a2 = in2.audio.filter('areverse').filter('aphaser')

                joined = ffmpeg.concat(v1, a1, v2, a2, v=1, a=1).node
                v3 = joined[0]
                a3 = joined[1].filter('volume', 0.8)

                ffmpeg.output(v3, a3, output_file).run()

                # Read the final output file and provide it for download
                with open(output_file, "rb") as f:
                    file_data = f.read()

                st.download_button(
                    label="Download Merged Video",
                    data=file_data,
                    file_name="merged_video.mp4",
                    mime="video/mp4"
                )

                # Clean up the temporary files
                os.remove(output_file)

            else:
                st.error("Could not download two videos. Please ensure the URL is correct.")

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")


def main():
    st.title("YouTube Video Downloader and Merging")

    url = st.text_input("Enter the YouTube video URL")

    option = st.selectbox(
        'Select type of download',
        ('audio', 'highest_resolution', 'lowest_resolution', '4k')
    )

    if url:
        if st.button("Download and Merge Videos"):
            download_video(url, option)

        if st.button("View Video"):
            st.video(url)


if __name__ == "__main__":
    main()
