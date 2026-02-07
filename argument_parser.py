import argparse
import os.path
import sys

def parse():

    parser = argparse.ArgumentParser(allow_abbrev=False)

    non_download_args = parser.add_argument_group()

    non_download_args.add_argument(
        "--sync",
        help="Updates all dependencies.",
        action="store_true",
        default=False
    )

    non_download_args.add_argument(
        "--show-download-directory",
        "--show-download-dir",
        help="Show the current download directory.",
        action="store_true"
    )

    non_download_args.add_argument(
        "--set-download-directory",
        "--set-download-dir",
        help="Set/change download directory."
    )

    download_args = parser.add_argument_group()

    download_args.add_argument(
        "--mp3",
        action="store_true",
        help="Convert to mp3 after download."
    )

    download_args.add_argument(
        "--url",
        help="Spotify track URL.",
        nargs="+"
    )

    download_args.add_argument(
        "--dir",
        help="Bypass saved download directory and use another for current session.",
    )

    args = parser.parse_args()

    download_used = any([
        args.mp3,
        args.url
    ])

    if download_used and not args.url:
        print("No URL provided.")
        sys.exit(1)

    if args.set_download_directory and not os.path.isdir(args.set_download_directory):
        print("error: Not a directory.")
        sys.exit(1)

    if args.set_download_directory and not os.path.exists(args.set_download_directory):
        print("error: Directory not found.")
        sys.exit(1)

    if args.url and "playlist" in args.url:
        print("Playlist feature has not been implemented yet. Please proceed with single tracks for now.")
        sys.exit(1)

    if args.url:
        for url in args.url:
            if not url.startswith("https://open.spotify.com/") or len(url) < 40:
                print(f"invalid url: {url}\nerror: The provided URL is not a valid Spotify track or playlist link. Expected format: https://open.spotify.com/...")
                sys.exit(1)

    return args

if __name__ == "__main__":
    parse()