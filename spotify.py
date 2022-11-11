import tekore as tk


spotify = tk.Spotify()

#conf = tk.config_from_file('spotify.cfg', return_refresh=True)
conf = tk.config_from_environment(return_refresh=True)
user_token = tk.refresh_user_token(*conf[:2], conf[3])
spotify.token = user_token


def saved_records():
    records = spotify.saved_albums(limit=20)
    record_names = [record.album.name for record in records.items]
    return record_names

