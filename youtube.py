import webbrowser
import pprint
from youtubesearchpython import VideosSearch, PlaylistsSearch


"""
Returns the Youtube PLAYLIST link found for the given album name
"""
def get_album_link(album_name):
    query = album_name + "Full Album"
    pp = pprint.PrettyPrinter(indent=4)
    search_result = PlaylistsSearch(query, limit=1).result()["result"]
    pp.pprint(search_result)
    if not search_result:
        return None
    
    return search_result[0]["link"]



"""
Opens a Youtube URL in a new tab of the web browser
"""
def play_video(url: str):
    return webbrowser.open(url)