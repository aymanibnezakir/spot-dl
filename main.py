import os
import sys
import json

import argument_parser
import update_deps
import spotify
import downloader

CONFIG_FILE = os.path.join(os.environ.get("TEMP"), "spot_dl_data.json")


def get_this_path():
    if getattr(sys, 'frozen', False):
        # Running as compiled EXE
        return os.path.dirname(sys.executable)
    else:
        # Running as .py script
        return os.path.dirname(os.path.abspath(__file__))
    

THIS_PATH = get_this_path()
YTDLP_PATH = os.path.join(THIS_PATH, "bins", "yt-dlp.exe")
FFMPEG_PATH = os.path.join(THIS_PATH, "bins", "ffmpeg.exe")


def deps_check():
    deps = ["yt-dlp.exe", "ffmpeg.exe"]
    error = False
    
    for dep in deps:
        dep_path = os.path.join(THIS_PATH, "bins", dep)
        if not os.path.exists(dep_path):
            if not error: error = True
            print(dep + " was not found. Please make sure the path exists: " + dep_path)

    if not os.path.exists(THIS_PATH):
        print(THIS_PATH + " was not found.")
        if not error: error = True

    if error: sys.exit(1)


if __name__ == "__main__":
    deps_check()
    args = argument_parser.parse()
    # print(args)

    if args.sync: update_deps.update_all(ytdlp_path=YTDLP_PATH)

    if args.set_download_directory:
        data = {"download_location": args.set_download_directory}
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=True)

    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            settings = json.load(f)

        DOWNLOAD_DIR = settings['download_location']

    else:
        print("Please set the download path first. Use arg: '--set-download-directory'.")
        sys.exit(1)

    if args.show_download_directory:
        print(DOWNLOAD_DIR)
        print("To change, use arg: '--set-download-directory'.")

    if args.url:

        tracks = []
        playlists = []

        for url in args.url:
            if "track" in url:
                tracks.append(url)
            if "playlist" in  url:
                playlists.append(url)

        track_metadata, playlist_metadata = spotify.get_info_from_urls(track_urls=tracks, playlist_urls=playlists)

        if track_metadata: print("Downloading track(s)...")

        total_tracks = len(track_metadata)
        for i, (url, name_artist) in enumerate(track_metadata.items(), start=1):
            print(f"Downloading track ({i}/{total_tracks}): {url}")
            print(f"  Title: {name_artist[0]}")
            print(f"  Artist: {name_artist[1]}")
            downloader.download(song_name=name_artist[0], first_artist_name=name_artist[1], is_mp3=args.mp3, ytdlp_path=YTDLP_PATH, download_dir=DOWNLOAD_DIR)

        if playlist_metadata: print("Downloading playlist(s)...")

        total_playlists = len(playlist_metadata)

        for i, (playlist_url_and_name, song_and_artist_names) in enumerate(playlist_metadata.items(), start=1):

            playlist_url, playlist_name = playlist_url_and_name

            try:
                download_dir_for_playlist = os.path.join(DOWNLOAD_DIR, playlist_name.strip())
                if not os.path.exists(download_dir_for_playlist):
                    os.mkdir(download_dir_for_playlist)
            except:
                print(f"Failed to create folder for playlist:{playlist_name}.\nTracks will be downloaded in this directory: {DOWNLOAD_DIR}")
                download_dir_for_playlist = DOWNLOAD_DIR

            print(f"Downloading playlist ({i}/{total_playlists}): {playlist_name} [{playlist_url}]")

            song_in_playlist = len(song_and_artist_names)
            for j, song in enumerate(song_and_artist_names, start=1):
                song_title = song[0]
                song_artist = song[1]
                print(f"Downloading track ({j}/{song_in_playlist}): {song_title} - {song_artist}")
                downloader.download(song_name=song_title, first_artist_name=song_artist, is_mp3=args.mp3, ytdlp_path=YTDLP_PATH, download_dir=download_dir_for_playlist)