import yt_dlp
import os


# -----------------------------------
# Playlist URL
# -----------------------------------

playlist_url = input("Enter YouTube playlist URL: ").strip()


# -----------------------------------
# Download folder
# -----------------------------------

download_folder = "downloads"

os.makedirs(download_folder, exist_ok=True)


# -----------------------------------
# yt-dlp options
# -----------------------------------

options = {

    # Best available video + audio
    # Falls back to a combined format if necessary
    "format": "bv*+ba/b",

    # File naming
    "outtmpl": os.path.join(
        download_folder,
        "%(playlist_index)02d - %(title)s.%(ext)s"
    ),

    # Merge video + audio
    "merge_output_format": "mp4",

    # -----------------------------------
    # Retry settings
    # -----------------------------------

    "retries": 20,
    "fragment_retries": 20,
    "file_access_retries": 10,

    # Continue partially downloaded files
    "continuedl": True,

    # Retry sleep
    "retry_sleep_functions": {
        "http": lambda n: min(10 * n, 60),
        "fragment": lambda n: min(10 * n, 60),
    },

    # -----------------------------------
    # Don't download already completed
    # -----------------------------------

    "download_archive": os.path.join(
        download_folder,
        "downloaded.txt"
    ),

    # -----------------------------------
    # Playlist settings
    # -----------------------------------

    "ignoreerrors": True,
    "yesplaylist": True,

    # -----------------------------------
    # Progress information
    # -----------------------------------

    "noprogress": False,

    # -----------------------------------
    # Keep temporary files until finished
    # -----------------------------------

    "nopart": False,

    # -----------------------------------
    # Avoid overwriting completed files
    # -----------------------------------

    "overwrites": False,
}


# -----------------------------------
# Start download
# -----------------------------------

print("\nStarting playlist download...\n")

try:

    with yt_dlp.YoutubeDL(options) as ydl:

        ydl.download([playlist_url])


except KeyboardInterrupt:

    print("\n\nDownload stopped by user.")
    print("Run the program again to continue.")


except Exception as e:

    print("\n\nAn error occurred:")
    print(e)


# -----------------------------------
# Finished
# -----------------------------------

print("\n-----------------------------------")
print("Download process finished.")
print(f"Files are located in: {download_folder}")
print("-----------------------------------")