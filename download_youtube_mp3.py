import os
import re
import argparse
from pytube import YouTube

# Define the path to the text file containing the YouTube video URLs.
url_file = 'download_youtube_mp3_urls.txt'

# Regular expression pattern for matching YouTube video URLs.
url_pattern = r'^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+'

# Regular expression pattern for matching new lines and comments.
url_comment_pattern = r'^\/\/.+'

# Parse command line arguments to get the desired audio bitrate and target folder path.
parser = argparse.ArgumentParser(description='Download audio from YouTube videos.')
# Get the desired audio bitrate (default is 128 kbps).
parser.add_argument('--bitrate', type=int, default=128, help='audio bitrate in kbps')
# Get the desired folder there files to be downloaded (default is ./downloads).
parser.add_argument('--target_folder', type=str, default='downloads', help='target folder path (default: downloads)')
args = parser.parse_args()

# Check if the target folder exists and create it if it doesn't exist.
if not os.path.exists(args.target_folder):
    os.makedirs(args.target_folder)

# Read the list of URLs from the text file.
with open(url_file, 'r') as f:
    urls = [line.strip() for line in f]

# Loop over each URL and download the audio stream.
for url in urls:

    # Validate the URL using regular expressions.
    if not url or re.match(url_comment_pattern, url):
        continue

    if not re.match(url_pattern, url):
        print(f'Invalid URL: {url}')
        continue

    # Create a new YouTube object and set the video URL.
    yt = YouTube(url)
    print(f"Downloading audio for {yt.title}...")

    # Get the audio stream with the highest bitrate (usually the one with the best quality).
    audio_stream = yt.streams.get_audio_only()

    # Get the default file name for the audio stream.
    filename = audio_stream.default_filename

    # Remove the video extension from the filename and replace it with .mp3.
    filename = os.path.splitext(filename)[0] + '.mp3'

    # Add the target folder path to the filename.
    filename = os.path.join(args.target_folder, filename)

    # Convert the audio stream to an MP3 file using FFmpeg.
    os.system(f'ffmpeg -i "{audio_stream.url}" -b:a {args.bitrate}k "{filename}"')
