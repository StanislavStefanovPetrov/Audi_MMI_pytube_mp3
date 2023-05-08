import os
import re
import argparse
from pytube import YouTube

def download_audio_from_youtube(url, target_folder='downloads', bitrate=128):
    """
    Downloads the audio stream from a YouTube video.

    Args:
        url (str): The YouTube video URL.
        target_folder (str): The path to the target folder to save the audio file to. Default is 'downloads'.
        bitrate (int): The desired audio bitrate in kbps. Default is 128 kbps.
    """
    # Validate the URL using regular expressions.
    url_pattern = r'^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+'
    url_comment_pattern = r'^\/\/.+'

    if not url or re.match(url_comment_pattern, url):
        return

    if not re.match(url_pattern, url):
        print(f'Invalid URL: {url}')
        return

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
    filename = os.path.join(target_folder, filename)

    # Convert the audio stream to an MP3 file using FFmpeg.
    os.system(f'ffmpeg -i "{audio_stream.url}" -b:a {bitrate}k "{filename}"')


def download_audio_from_youtube_urls(url_file, target_folder='downloads', bitrate=128):
    """
    Downloads the audio stream from multiple YouTube videos specified in a text file.

    Args:
        target_urls_file (str): The path to the text file containing the YouTube video URLs.
        target_folder (str): The path to the target folder to save the audio files to. Default is 'downloads'.
        bitrate (int): The desired audio bitrate in kbps. Default is 128 kbps.
    """
    # Check if the target folder exists and create it if it doesn't exist.
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    # Read the list of URLs from the text file.
    with open(url_file, 'r') as f:
        urls = [line.strip() for line in f]

    # Loop over each URL and download the audio stream.
    for url in urls:
        download_audio_from_youtube(url, target_folder, bitrate)

if __name__ == '__main__':
    # Parse command line arguments to get the desired audio bitrate and target folder path.
    parser = argparse.ArgumentParser(description='Download audio from YouTube videos.')
    # Get the desired audio bitrate (default is 128 kbps).
    parser.add_argument('--bitrate', type=int, default=128, help='audio bitrate in kbps')
    # Get the desired folder there files to be downloaded (default is ./downloads).
    parser.add_argument('--target_folder', type=str, default='downloads', help='target folder path (default: downloads)')
     # Get the desired folder there files to be downloaded (default is ./downloads).
    parser.add_argument('--target_urls_file', type=str, default='youtube_urls.txt', help='target txt file where you store youtube urls (default: youtube_urls.txt)')
    args = parser.parse_args()

    download_audio_from_youtube_urls(args.target_urls_file, args.target_folder, args.bitrate)