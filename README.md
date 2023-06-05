# Audi YouTube Downloader

Audi YouTube Downloader is a Python script that allows you to download audio files from YouTube in a format compatible with Audi Multi Media Interface (MMI) systems. You can then listen to these tracks in your Audi car using SD/SDHC/MMC memory cards.

## Features

- Download audio files from YouTube and convert them to the proper format for Audi MMI systems.
- Specify a list of YouTube URLs in a text file and download all the corresponding audio files.
- Customize the audio bitrate for the downloaded files.
- Organize downloaded files in a target folder for easy access.

## Compatibility

This project takes into account the limitations of Audi MMI systems regarding track formats. It ensures that the downloaded audio files are in a format supported by Audi MMI systems. For more information on Audi MMI system limitations, refer to the following sources:

- [AudiWorld Forum: MMI 3G - Largest SD Card Size](https://www.audiworld.com/forums/q5-sq5-mki-8r-discussion-129/mmi-3g-largest-sd-card-size-2872958/#&gid=1&pid=1)

## Usage

1. Clone or download the repository to your local machine.

2. Install the required dependencies by running the following command:
```sh
pip install -r requirements.txt
```


3. Create a text file (`url_file.txt` by default) and add the YouTube video URLs you want to download, with each URL on a new line.

4. Run the script using the following command:
```sh
python main.py --target_folder <target_folder_path>
```


Optional arguments:
- `--bitrate`: Specify the audio bitrate in kbps (default: 320 kbps).
- `--channels`: Specify the number of audio channels (default: 2).
- `--sample_rate`: Specify the audio sample rate in Hz (default: 48000 Hz).
- `--url_file`: Specify the path to the file containing the YouTube video URLs (default: `url_file.txt`).
- `--target_folder`: Specify the path to the folder where the downloaded audio files will be saved (default: `./downloads`).

5. The script will download the audio files from the provided YouTube URLs and save them in the specified target folder. The downloaded files will be in a format compatible with Audi MMI systems.

## Notes

- The downloaded audio files will be in MP3 format, as it is supported by Audi MMI systems.
- The script uses the PyTube library for downloading YouTube videos and FFmpeg for converting the downloaded files to MP3 format.

Feel free to customize and modify the script according to your needs.

## License

This project is licensed under the [MIT License](LICENSE).
