import os.path
import sys
import subprocess
from ytmusicapi import YTMusic


def fetch_song_link(artist, song_name) -> str | None:
    ytmusic = YTMusic() # no login needed for search (anonymous)

    if artist == 'Unknown': song_query = f"{song_name}"
    else: song_query = f"{artist} - {song_name}"

    results = ytmusic.search(song_query, filter="songs", limit=3)

    if not results:
        print("error: Download Failed for unknown reason.")
        return None
    else:
        # Usually the very first result is the official/best match
        top = results[0]
        music_url = f"https://music.youtube.com/watch?v={top['videoId']}"

        return music_url

def download(song_name, first_artist_name, is_mp3, ytdlp_path, download_dir) -> bool:

    result = fetch_song_link(artist=first_artist_name, song_name=song_name)

    if not result:
        return False

    if first_artist_name == 'Unknown':
        download_path = os.path.join(download_dir, f"{song_name}.%(ext)s")
    else:
        download_path = os.path.join(download_dir, f"{song_name} - {first_artist_name}.%(ext)s")

    if is_mp3:
        cmd = [
            ytdlp_path,
            "-f",
            "bestaudio",
            "-o",
            download_path,
            "-x",
            "--audio-format",
            "mp3",
            result,
            "--no-warnings"
        ]
    else:
        cmd = [
            ytdlp_path,
            "-f",
            "bestaudio",
            "-o",
            download_path,
            result,
            "--no-warnings"
        ]

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for line in process.stdout:
        if "[download]" in line and "%" in line and not "100%" in line:
            print(f"  {line.strip()}", end="\r", flush=True)
        if "100%" in line:
            print(f"  {line.strip()}", flush=True)
        if "Forbidden" in line:
            print("error: Download forbidden. Updating yt-dlp might help...")
            process.terminate()
            sys.exit(1)

    process.wait()
    return True
