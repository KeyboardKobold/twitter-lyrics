import os
import types
import tweepy
import random
import lyricsgenius


# todo only pull new songs once per 24h
def pick_song():
    genius = lyricsgenius.Genius()
    genius.retries = 5
    genius.remove_section_headers = True  # Remove section headers (e.g. [Chorus]) from lyrics when searching
    genius.skip_non_songs = True  # Include hits thought to be non-songs (e.g. track lists)
    genius.excluded_terms = ["(Remixed)", "(Live)", "(Remix)", "(live)", "(Intro)"]  # Exclude songs with these words in their title
    artist = genius.search_artist("Limp Bizkit")  # max_songs=3
    song = random.choice(artist.songs)
    return song.lyrics


def pick_lyrics(lyrics):  # todo retry if picked lines are identical
    lines = lyrics.split('\n')
    lines = [i for i in lines if i != ""]  # clean out empty lines

    random_num = random.randrange(0, len(lines)-1)
    tweet = lines[random_num] + "\n" + lines[random_num+1]
    # tweet = tweet.replace("\\", "")
    return tweet


def tweet_lyrics(lyrics, auth):
    auth = tweepy.OAuthHandler(auth.api_key, auth.api_secret)
    auth.set_access_token(auth.access_token, auth.access_token_secret)
    api = tweepy.API(auth)
    api.update_status(lyrics)


if __name__ == '__main__':
    twitter_auth = types.SimpleNamespace()
    try:
        twitter_auth.api_key = os.environ['TWITTER_API_KEY']
        twitter_auth.api_secret = os.environ['TWITTER_API_SECRET']
        twitter_auth.access_token = os.environ['TWITTER_ACCESS_TOKEN']
        twitter_auth.access_token_secret = os.environ['TWITTER_ACCESS_TOKEN_SECRET']
    except KeyError as err:
        print(f"Given key not found - {err}")

    tweet_lyrics(pick_lyrics(pick_song()), twitter_auth)

