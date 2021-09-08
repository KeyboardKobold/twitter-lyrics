#!/usr/bin/env bash
docker build -t twitter_lyrics .
docker run -it --rm --name running_twitter_lyrics --env-file config.env twitter_lyrics
