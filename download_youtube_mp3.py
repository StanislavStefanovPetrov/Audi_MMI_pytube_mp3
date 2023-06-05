import os
import re
import argparse
import eyed3
from pytube import YouTube
import ffmpeg

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

def remove_non_ascii(text):
    # Remove non-ASCII characters
    text = text.encode("ascii", "ignore").decode()

    # Remove non-alphanumeric characters except basic punctuation signs
    text = re.sub(r"[^a-zA-Z0-9\s.,!?()-]+", "", text)

    # Replace whitespace with dashes
    text = re.sub(r"\s+", " ", text.strip())

    return text

def download_audio(url, target_folder='downloads', bitrate=320):
    """
    Downloads the audio stream from a YouTube video.

    Args:
        url (str): The YouTube video URL.
        target_folder (str): The path to the target folder to save the audio file to. Default is 'downloads'.
        bitrate (int): The desired audio bitrate in kbps. Default is 320 kbps.
    """
    # Validate the YouTube video URL
    if not is_validate_url(url):
        return

    # Set the desired audio format options
    audio_format = {
        "format": "mp3",
        "audio_bitrate": f"{bitrate}k",
        "channels": 2,
        "sample_rate": 48000,
    }

    yt = YouTube(url)
    print(f"Downloading audio for {yt.title}...")

    audio_stream = yt.streams.filter(only_audio=True).first()

    # Download the video stream
    audio_stream.download()

    # Get the downloaded file path
    file_path = audio_stream.default_filename

    # Convert the downloaded file to MP3 using ffmpeg
    output_filename = os.path.join(target_folder, f"{remove_non_ascii(file_path).split('.')[0]}.mp3")      
    ffmpeg.input(file_path).output(output_filename, **audio_format).run(overwrite_output=True)

    # Remove the temporary video file
    os.remove(file_path)

    # Add metadata to the MP3 file
    audiofile = eyed3.load(output_filename)
    if audiofile is not None:
        audiofile.tag.artist = yt.author
        audiofile.tag.album = yt.title
        audiofile.tag.title = yt.title
        audiofile.tag.track_num = (1, 1)  # set track number to 1
        audiofile.tag.save()

    print(f"Downloaded audio for {yt.title}...")

def download_audio_urls(url_file='youtube_urls.txt', target_folder='downloads', bitrate=320):
    """
    Downloads the audio stream from multiple YouTube videos specified in a text file.

    Args:
        url_file (str): The path to the text file containing the YouTube video URLs. Default is 'youtube_urls.txt'.
        target_folder (str): The path to the target folder to save the audio files to. Default is 'downloads'.
        bitrate (int): The desired audio bitrate in kbps. Default is 320 kbps.
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
    parser.add_argument('--bitrate', type=int, default=320, help='audio bitrate in kbps (default: 320 kbps)')
    parser.add_argument('--target_folder', type=str, default='downloads', help='target folder path (default: downloads)')
    parser.add_argument('--url_file', type=str, default='youtube_urls.txt', help='path to the file containing the YouTube video URLs (default: youtube_urls.txt)')
    args = parser.parse_args()

    download_audio_urls(args.url_file, args.target_folder, args.bitrate)
