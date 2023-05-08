# Download audio from YouTube videos with pytube

Current code will download audio file in mp3 format from YouTube.
The code read a list from Youtube urls from `url_file.txt` (default: `./youtube_urls.txt`) and download all target `mp3` files into `target_folder` (default: `./downloads`).
The user can define `bitrate` in which the mp3 files to be record in (default: `128 kbps`).
