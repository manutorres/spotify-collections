import tekore as tk
from models import AlbumModel

spotify = tk.Spotify()

#conf = tk.config_from_file('spotify.cfg', return_refresh=True)
conf = tk.config_from_environment(return_refresh=True)
user_token = tk.refresh_user_token(*conf[:2], conf[3])
spotify.token = user_token


def get_saved_albums():
    album_names = []
    page = 0
    albums_per_page = 20
    while True:
        albums = spotify.saved_albums(limit=albums_per_page, offset=page * albums_per_page)
        album_names.extend([record.album.name for record in albums.items])
        if len(albums.items) < albums_per_page:
            break
        page += 1
    return album_names


def get_search_albums(query: str):
    albums, = spotify.search(query, types=('album',))
    album_names = [album.name for album in albums.items]
    return album_names


def get_album(album_id: str):
    full_album = spotify.album(album_id)
    artists = [artist.name for artist in full_album.artists]
    album = AlbumModel(
        spotify_id=album_id,
        name=full_album.name,
        artists=artists
    )
    return album
