# How to play songs in Audi?

You can listen music in our Audi car via SD/SDHC/MMC memory cards.
Never the less there are some Audi Multi Media Interface (MMI) system limitations about tracks format.
This project provide you a way to download a set of youtube tracks in proper format.
Audi Multi Media Interface (MMI) Source information used:
https://www.audiworld.com/forums/q5-sq5-mki-8r-discussion-129/mmi-3g-largest-sd-card-size-2872958/#&gid=1&pid=1
https://static.nhtsa.gov/odi/tsbs/2014/MC-10124745-9999.pdf

## Download audio from YouTube videos with pytube

Current code will download audio file in mp3 format from YouTube.
The code read a list from Youtube urls from `url_file.txt` (default: `./youtube_urls.txt`) and download all target `mp3` files into `target_folder` (default: `./downloads`).
The user can define `bitrate` in which the mp3 files to be record in (default: `128 kbps`).
