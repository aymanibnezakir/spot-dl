from spotify_scraper import SpotifyClient


def get_info_from_urls(track_urls: list, playlist_urls: list) -> tuple[dict[str, list], dict[tuple, list[list]]]:
    track_datas = {}
    playlist_datas = {}

    # Initialize the client
    client = SpotifyClient()

    for track_url in track_urls:
        if track_url in track_datas:
            continue

        track = client.get_track_info(track_url)
        track_data = [track.get('name', 'Unknown'), track.get('artists', [{}])[0].get('name', 'Unknown') if track.get('artists') else 'Unknown']
        # track_data = [title, artist]

        if track_data[0] == 'Unknown':
            print(f"Skipped {track_url}")

        track_datas[track_url] = track_data

    for playlist_url in playlist_urls:

        playlist = client.get_playlist_info(playlist_url)
        total_tracks = playlist.get('track_count', 'N/A')

        if total_tracks != 'N/A':
            if total_tracks > 100:
                print('warning: For very large playlists (>100 tracks), only the first 100 tracks may be returned.')

        key = (playlist_url, playlist['name'])
        value = [] # List[List] -> [[title, artist_name], ....]

        for item in playlist['tracks']:
            name = item.get('name', 'Unknown')

            if name == 'Unknown':
                continue

            artists_list_raw = item.get('artists', [])

            if artists_list_raw:
                artists_list = [
                    a.strip()
                    for a in artists_list_raw[0].get('name', '')
                    .replace('\xa0', ' ')
                    .split(',')
                ]
            else:
                artists_list = ["Unknown"]


            value.append([name, artists_list[0]])

        playlist_datas[key] = value

    # Always close when done
    client.close()

    return track_datas, playlist_datas