import asyncio
import os

import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth
from twikit import Client

client = Client(language="ja",user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36')
# ログイン情報を cookies.json から読み込む
client.load_cookies("cookies.json")

# .envファイルの読み込み
load_dotenv()

# Spotify APIの認証情報
SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")

# Spotify APIの認証
spotify = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope="user-read-currently-playing",
    )
)

# 変数の初期化
last_track_id = None

# Spotifyで現在再生中のトラックを取得
def get_current_track():
    current_track = spotify.current_user_playing_track()
    if current_track and current_track["is_playing"]:
        track_name = current_track["item"]["name"]
        artist_name = current_track["item"]["artists"][0]["name"]
        track_id = current_track["item"]["id"]
        track_url = current_track["item"]["external_urls"]["spotify"]
        print(f"現在再生中の曲: {track_name} - {artist_name}")
        return track_name, artist_name, track_id, track_url
    return None, None, None, None

# 現在再生中の曲をツイート
async def tweet_nowPlaying(track_name, artist_name, track_url):
    tweet = f"🎵Now Playing: {track_name} by {artist_name} #NowPlaying\n{track_url}"
    # tweet = f"{track_name} #NowPlaying\n{track_url}"
    try:
        await client.create_tweet(tweet)
        print(f"ツイートしました: {tweet}")
    except Exception as e:
        print(f"エラー: {e}")


async def main():
    while True:
        global last_track_id
        track_name, artist_name, track_id, track_url = get_current_track()
        if track_id and track_id != last_track_id:
            await tweet_nowPlaying(track_name, artist_name, track_url)
            last_track_id = track_id
        await asyncio.sleep(30)

if __name__ == "__main__":
  asyncio.run(main())
