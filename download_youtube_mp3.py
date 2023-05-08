import os
import re
import argparse
from pytube import YouTube


def is_validate_url(url):
    """
    Validates a YouTube video URL using regular expressions.
    """
    url_pattern = r'^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+'
    url_comment_pattern = r'^\/\/.+'

    if not url or re.match(url_comment_pattern, url):
        return False

    if not re.match(url_pattern, url):
        print(f'Invalid URL: {url}')
        return False

    return True


def download_audio(url, target_folder='downloads', bitrate=128):
    """
    Downloads the audio stream from a YouTube video.

    Args:
        url (str): The YouTube video URL.
        target_folder (str): The path to the target folder to save the audio file to. Default is 'downloads'.
        bitrate (int): The desired audio bitrate in kbps. Default is 128 kbps.
    """
    if not is_validate_url(url):
        return

    yt = YouTube(url)
    print(f"Downloading audio for {yt.title}...")

    audio_stream = yt.streams.get_audio_only()

    filename = os.path.splitext(audio_stream.default_filename)[0] + '.mp3'
    filename = os.path.join(target_folder, filename)

    os.system(f'ffmpeg -i "{audio_stream.url}" -b:a {bitrate}k "{filename}"')


def download_audio_urls(url_file='youtube_urls.txt', target_folder='downloads', bitrate=128):
    """
    Downloads the audio stream from multiple YouTube videos specified in a text file.

    Args:
        url_file (str): The path to the text file containing the YouTube video URLs. Default is 'youtube_urls.txt'.
        target_folder (str): The path to the target folder to save the audio files to. Default is 'downloads'.
        bitrate (int): The desired audio bitrate in kbps. Default is 128 kbps.
    """
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    if not os.path.exists(url_file):
        with open(url_file, 'w+') as f:
            pass  # do nothing, file is created
    
    with open(url_file, 'r') as f:
        urls = [line.strip() for line in f if is_validate_url(line.strip())]

    for url in urls:
        download_audio(url, target_folder, bitrate)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download audio from YouTube videos.')
    parser.add_argument('--bitrate', type=int, default=128, help='audio bitrate in kbps (default: 128 kbps)')
    parser.add_argument('--target_folder', type=str, default='downloads', help='target folder path (default: downloads)')
    parser.add_argument('--url_file', type=str, default='youtube_urls.txt', help='path to the file containing the YouTube video URLs (default: youtube_urls.txt)')
    args = parser.parse_args()

    download_audio_urls(args.url_file, args.target_folder, args.bitrate)
