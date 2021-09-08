import sys
import os
import threading
import tweepy
import random
import lyricsgenius


# todo only pull new songs once per 24h
def pick_song(genius_config):
    genius = lyricsgenius.Genius()
    genius.retries = 5
    genius.remove_section_headers = True  # Remove section headers (e.g. [Chorus]) from lyrics when searching
    genius.skip_non_songs = True  # Include hits thought to be non-songs (e.g. track lists)
    if "CONF_EXCLUDED_TERMS" in genius_config:
        genius.excluded_terms = genius_config["CONF_EXCLUDED_TERMS"]
    else:
        genius.excluded_terms = ["(Remixed)", "(Live)", "(Remix)", "(live)",
                                 "(Intro)"]
    artist = genius.search_artist(genius_config["CONF_ARTIST"])
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


def get_config():
    keys = {"AUTH": {}, "CONF": {}}

    # mandatory
    try:
        keys["AUTH"]["TWITTER_API_KEY"] = os.environ['TWITTER_API_KEY']
        keys["AUTH"]["TWITTER_API_SECRET"] = os.environ['TWITTER_API_SECRET']
        keys["AUTH"]["TWITTER_ACCESS_TOKEN"] = os.environ['TWITTER_ACCESS_TOKEN']
        keys["AUTH"]["TWITTER_ACCESS_TOKEN_SECRET"] = os.environ['TWITTER_ACCESS_TOKEN_SECRET']
        keys["CONF"]["CONF_ARTIST"] = os.environ['CONF_ARTIST']
    except KeyError as err:
        sys.exit(f"Given key not found - {err}")
    # optional
    if "CONF_EXCLUDED_TERMS" in os.environ:
        keys["CONF"]["CONF_EXCLUDED_TERMS"] = os.environ['CONF_EXCLUDED_TERMS'].split()
    return keys


def timer():
    tweet_lyrics(pick_lyrics(pick_song(config["CONF"])), config["AUTH"])
    threading.Timer(1800, timer).start()


if __name__ == '__main__':
    config = get_config()
    print(f"Running for - {config['CONF']['CONF_ARTIST']}")
    timer()

