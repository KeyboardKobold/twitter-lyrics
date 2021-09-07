import sys
import os
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


def tweet_lyrics(lyrics, keys):
    auth = tweepy.OAuthHandler(keys["TWITTER_API_KEY"], keys["TWITTER_API_SECRET"])
    auth.set_access_token(keys["TWITTER_ACCESS_TOKEN"], keys["TWITTER_ACCESS_TOKEN_SECRET"])
    api = tweepy.API(auth)
    api.update_status(lyrics)


def get_auth():
    keys = {}
    try:
        keys["TWITTER_API_KEY"] = os.environ['TWITTER_API_KEY']
        keys["TWITTER_API_SECRET"] = os.environ['TWITTER_API_SECRET']
        keys["TWITTER_ACCESS_TOKEN"] = os.environ['TWITTER_ACCESS_TOKEN']
        keys["TWITTER_ACCESS_TOKEN_SECRET"] = os.environ['TWITTER_ACCESS_TOKEN_SECRET']
    except KeyError as err:
        sys.exit(f"Given key not found - {err}")
    return keys


if __name__ == '__main__':
    tweet_lyrics(pick_lyrics(pick_song()), get_auth())

